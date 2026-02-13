from pyshacl import validate
from rdflib import Graph

DATA = "lung_cancer_instances.ttl"
SHAPES = "lungcancer-shacl.ttl"

data_graph = Graph().parse(DATA)
shapes_graph = Graph().parse(SHAPES)

conforms, results_graph, results_text = validate(
    data_graph,
    shacl_graph=shapes_graph,
    inference="rdfs",
)

print("Conforms:", conforms)
print(results_text)
