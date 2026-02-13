import pandas as pd
import json
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF

BASE = Namespace("http://lungkg.org/resource/")
ONT  = Namespace("http://lungkg.org/ontology#")

ONTOLOGY = "ttl_shacl_data/lung_cancer_kg_schema.ttl"
MAPPING  = "mapping_config.json"

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

config = json.load(open(MAPPING))

for section in config.values():

    df = pd.read_csv(section["file"])

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

g.serialize("lung_cancer_instances.ttl")

with open("auto_generated.cypher","w") as f:
    f.write("\n".join(cypher_lines))

print("✓ RDF saved")
print("✓ Cypher saved")
