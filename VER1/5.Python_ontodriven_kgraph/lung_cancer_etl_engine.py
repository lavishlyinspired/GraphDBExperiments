import pandas as pd
import json
from pathlib import Path
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF

BASE = Namespace("http://lungkg.org/resource/")
ONT  = Namespace("http://lungkg.org/ontology#")

# Get the directory where this script is located
SCRIPT_DIR = Path(__file__).parent

ONTOLOGY = SCRIPT_DIR / "ttl_shacl_data" / "lung_cancer_kg_schema.ttl"
MAPPING  = SCRIPT_DIR / "ttl_shacl_data" / "mapping_config.json"

g = Graph()
g.parse(ONTOLOGY)

g.bind("ont", ONT)
g.bind("res", BASE)


########################################
# Helpers
########################################

def make_uri(template, row):
    return URIRef(BASE[template.format(**row)])

cypher_lines = []


########################################
# Engine
########################################

config = json.load(open(MAPPING, 'r'))

for section in config.values():

    # Resolve CSV file path relative to script directory
    csv_path = SCRIPT_DIR / section["file"]
    df = pd.read_csv(csv_path)

    for _, r in df.iterrows():
        row = r.to_dict()

        subj = make_uri(section["subject"], row)

        # type
        if "type" in section:
            g.add((subj, RDF.type, ONT[section["type"]]))
            cypher_lines.append(
                f"MERGE (n:{section['type']} {{id:'{subj.split('/')[-1]}'}})"
            )

        # datatype properties
        for prop, col in section.get("datatype_props", {}).items():
            g.add((subj, ONT[prop], Literal(row[col])))
            cypher_lines.append(
                f"SET n.{prop}='{row[col]}'"
            )

        # object links
        for prop, tmpl in section.get("object_links", {}).items():
            obj = make_uri(tmpl, row)
            g.add((subj, ONT[prop], obj))

            label = tmpl.split("_")[0]
            cypher_lines.append(
                f"MERGE (o:{label} {{id:'{obj.split('/')[-1]}'}})"
            )
            cypher_lines.append(
                f"MERGE (n)-[:{prop.upper()}]->(o)"
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
