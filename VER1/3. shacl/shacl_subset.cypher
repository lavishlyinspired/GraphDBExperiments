:param shacl => "
@prefix lc: <http://example.org/lungCancer#> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix neo4j: <neo4j://graph.schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

lc:PatientShape a sh:NodeShape ;
  sh:targetClass neo4j:Patient ;
  sh:property [
    sh:path neo4j:name ;
    sh:minCount 1 ;
  ] ;
  sh:property [
    sh:path neo4j:age ;
    sh:datatype xsd:integer ;
  ] .

lc:LungCancerShape a sh:NodeShape ;
  sh:targetClass neo4j:LungCancer ;
  sh:property [
    sh:path neo4j:hasStage ;
    sh:minCount 1 ;
  ] .
";

CALL n10s.validation.shacl.import.inline($shacl, "Turtle");

match (p:Patient)
with p limit 1
remove p.name
return p
