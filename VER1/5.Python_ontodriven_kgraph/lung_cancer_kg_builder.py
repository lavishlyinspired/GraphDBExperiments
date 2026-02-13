"""
Lung Cancer Decision Support Knowledge Graph Builder
---------------------------------------------------
Builds instance triples using the lung cancer ontology.

Inputs (CSV):
    lung_patients.csv
    lung_mutations.csv
    lung_treatments.csv

Ontology:
    lung_cancer_kg_schema.ttl

Outputs:
    lung_cancer_instances.ttl
"""

import pandas as pd
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, XSD


############################################
# Config
############################################

ONTOLOGY_FILE = "lung_cancer_kg_schema.ttl"
OUTPUT_FILE = "lung_cancer_instances.ttl"

PATIENT_FILE = "lung_patients.csv"
MUTATION_FILE = "lung_mutations.csv"
TREATMENT_FILE = "lung_treatments.csv"

BASE = Namespace("http://lungkg.org/resource/")
ONT = Namespace("http://lungkg.org/ontology#")


############################################
# Initialize graph
############################################

g = Graph()

print("Loading ontology...")
g.parse(ONTOLOGY_FILE, format="turtle")

g.bind("res", BASE)
g.bind("ont", ONT)


############################################
# Helpers
############################################

def uri(cls, id_):
    return URIRef(BASE[f"{cls}_{id_}"])


############################################
# Load data
############################################

patients = pd.read_csv(PATIENT_FILE)
mutations = pd.read_csv(MUTATION_FILE)
treatments = pd.read_csv(TREATMENT_FILE)


############################################
# Add Patients + Tumors
############################################

print("Adding patients...")

for _, row in patients.iterrows():

    p = uri("Patient", row.patient_id)
    tumor = uri("Tumor", row.patient_id)

    g.add((p, RDF.type, ONT.Patient))
    g.add((tumor, RDF.type, ONT.Tumor))

    g.add((p, ONT.patientId, Literal(str(row.patient_id))))
    g.add((p, ONT.age, Literal(int(row.age), datatype=XSD.integer)))
    g.add((p, ONT.sex, Literal(row.sex)))
    g.add((p, ONT.smokingPackYears, Literal(float(row.smoking_pack_years))))

    g.add((p, ONT.hasTumor, tumor))

    stage = uri("Stage", row.stage)
    g.add((stage, RDF.type, ONT.Stage))
    g.add((stage, ONT.stageName, Literal(row.stage)))

    g.add((tumor, ONT.hasStage, stage))


############################################
# Add Genomic Mutations
############################################

print("Adding mutations...")

for _, row in mutations.iterrows():

    p = uri("Patient", row.patient_id)
    biomarker = uri("Biomarker", row.gene)
    mutation = uri("Mutation", f"{row.gene}_{row.mutation}")
    gene = uri("Gene", row.gene)

    g.add((biomarker, RDF.type, ONT.Biomarker))
    g.add((mutation, RDF.type, ONT.Mutation))
    g.add((gene, RDF.type, ONT.Gene))

    g.add((biomarker, ONT.hasGene, gene))
    g.add((biomarker, ONT.hasMutation, mutation))

    g.add((p, ONT.testedForBiomarker, biomarker))


############################################
# Add Treatments + Outcomes
############################################

print("Adding treatments...")

for _, row in treatments.iterrows():

    p = uri("Patient", row.patient_id)
    therapy = uri("Therapy", f"{row.patient_id}_{row.drug}")
    drug = uri("Drug", row.drug)
    outcome = uri("Outcome", f"{row.patient_id}_{row.response}")

    g.add((therapy, RDF.type, ONT.Therapy))
    g.add((drug, RDF.type, ONT.Drug))
    g.add((outcome, RDF.type, ONT.Outcome))

    g.add((drug, ONT.drugName, Literal(row.drug)))
    g.add((outcome, ONT.responseType, Literal(row.response)))

    g.add((therapy, ONT.usesDrug, drug))

    g.add((p, ONT.receivedTherapy, therapy))
    g.add((p, ONT.hasOutcome, outcome))


############################################
# Save graph
############################################

print("Serializing graph...")
g.serialize(OUTPUT_FILE, format="turtle")

print(f"Done. Saved → {OUTPUT_FILE}")
print(f"Triples count: {len(g)}")


############################################
# Example DSS SPARQL Queries
############################################

def query_egfr_positive():
    print("\nPatients with EGFR mutation:")

    q = """
    PREFIX ont: <http://lungkg.org/ontology#>

    SELECT ?p
    WHERE {
        ?p ont:testedForBiomarker ?b .
        ?b ont:hasGene ?g .
        ?g ont:geneName "EGFR" .
    }
    """

    for row in g.query(q):
        print(row)


if __name__ == "__main__":
    print("KG build complete.")
