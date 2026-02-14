import pandas as pd
import json
import hashlib
from pathlib import Path
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, XSD
from nlp_processor import EntityExtractor, process_article_text

BASE = Namespace("http://lungkg.org/resource/")
ONT  = Namespace("http://lungkg.org/ontology#")

# Get the directory where this script is located
SCRIPT_DIR = Path(__file__).parent

MAPPING  = SCRIPT_DIR / "ttl_shacl_data" / "mapping_config.json"

# Create a new graph for instances only (don't parse schema)
g = Graph()
g.bind("ont", ONT)
g.bind("res", BASE)


########################################
# Helpers
########################################

def make_uri(template, row):
    return URIRef(BASE[template.format(**row)])

def make_label(uri_str):
    """Generate human-readable label from URI"""
    # Extract the last part after the last / or #
    local_name = uri_str.split('/')[-1].split('#')[-1]
    # Replace underscores with spaces and make it readable
    label = local_name.replace('_', ' ')
    return label

def get_entity_label(type_name, row, template):
    """Generate a meaningful label for an entity based on its type and data"""
    # For patients, use patient ID
    if type_name == "Patient":
        return f"Patient {row.get('patient_id', '')}"
    # For other entities, try to extract a meaningful identifier from template
    else:
        # Use the template to create a readable label
        filled = template.format(**row)
        return make_label(filled)

cypher_lines = []

# Initialize NLP entity extractor
entity_extractor = None  # Will be initialized after processing


########################################
# Engine
########################################

config = json.load(open(MAPPING, 'r'))

# Initialize entity extractor for NLP processing
entity_extractor = EntityExtractor(g, ONT, BASE)

for section_name, section in config.items():

    # Resolve CSV file path relative to script directory
    csv_path = SCRIPT_DIR / section["file"]
    df = pd.read_csv(csv_path)

    for _, r in df.iterrows():
        row = r.to_dict()

        subj = make_uri(section["subject"], row)

        # type
        if "type" in section:
            g.add((subj, RDF.type, ONT[section["type"]]))
            
            # Add rdfs:label for the subject
            subj_label = get_entity_label(section["type"], row, section["subject"])
            g.add((subj, RDFS.label, Literal(subj_label)))
            
            cypher_lines.append(
                f"MERGE (n:{section['type']} {{id:'{subj.split('/')[-1]}'}})"
            )
            cypher_lines.append(
                f"SET n.label='{subj_label}'"
            )

        # datatype properties
        for prop, col in section.get("datatype_props", {}).items():
            value = row[col]
            # Handle date types
            if prop == "publicationDate":
                g.add((subj, ONT[prop], Literal(value, datatype=XSD.date)))
            else:
                g.add((subj, ONT[prop], Literal(value)))
            cypher_lines.append(
                f"SET n.{prop}='{value}'"
            )

        # object links
        for prop, tmpl in section.get("object_links", {}).items():
            # Check if template has variables (contains {})
            if "{" in tmpl:
                # Template with variables: "Drug_{drug}"
                obj = make_uri(tmpl, row)
                # Extract object type from template (e.g., "Drug" from "Drug_{drug}")
                obj_type = tmpl.split("_")[0]
            else:
                # Fixed class reference: "LungCancer"
                obj = ONT[tmpl]  # Create URI in ontology namespace
                obj_type = tmpl
            
            g.add((subj, ONT[prop], obj))
            
            # Add rdf:type for the linked object (CRITICAL for Neo4j!)
            g.add((obj, RDF.type, ONT[obj_type]))
            
            # Add rdfs:label for linked objects
            obj_label = make_label(str(obj))
            g.add((obj, RDFS.label, Literal(obj_label)))

            # Get URI fragment for Cypher ID
            obj_id = str(obj).split('/')[-1].split('#')[-1]
            
            cypher_lines.append(
                f"MERGE (o:{obj_type} {{id:'{obj_id}'}})"
            )
            cypher_lines.append(
                f"SET o.label='{obj_label}'"
            )
            cypher_lines.append(
                f"MERGE (n)-[:{prop.upper()}]->(o)"
            )
        
        # NLP entity extraction for articles
        if section.get("nlp_extraction", False) and "body" in row:
            article_body = row["body"]
            if pd.notna(article_body) and len(str(article_body)) > 50:
                # Extract entities from article text
                entities = entity_extractor.extract_entities(str(article_body))
                
                # Create triples for extracted entities
                entity_triples = entity_extractor.create_entity_triples(subj, entities)
                for triple in entity_triples:
                    g.add(triple)
                
                # Add cypher for entity linking
                for concept_type, entity_list in entities.items():
                    for entity_text, canonical_name in entity_list:
                        entity_id = f"{concept_type}_{canonical_name}"
                        cypher_lines.append(
                            f"MERGE (e:{concept_type} {{id:'{entity_id}'}})"
                        )
                        cypher_lines.append(
                            f"SET e.label='{concept_type} {canonical_name}'"
                        )
                        cypher_lines.append(
                            f"MERGE (n)-[:REFERS_TO]->(e)"
                        )


########################################
# Save outputs
########################################

# Create output directory if it doesn't exist
OUTPUT_DIR = SCRIPT_DIR / "ouput"
OUTPUT_DIR.mkdir(exist_ok=True)

g.serialize(OUTPUT_DIR / "lung_cancer_instances_out.ttl")

with open(OUTPUT_DIR / "auto_generated.cypher", "w") as f:
    f.write("\n".join(cypher_lines))

print("✓ RDF saved")
print("✓ Cypher saved")
