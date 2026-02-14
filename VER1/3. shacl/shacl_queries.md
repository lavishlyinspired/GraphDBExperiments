:param shacl => "
@prefix lc: <http://example.org/lungCancer#> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix neo4j: <neo4j://graph.schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

lc:PatientShape a sh:NodeShape ;
  sh:targetClass neo4j:Patient ;

  sh:property [
    sh:path neo4j:name ;
    sh:datatype xsd:string ;
    sh:minCount 1 ;
    sh:severity sh:Violation ;
    sh:message \"Patient must have a name\" ;
  ] ;

  sh:property [
    sh:path neo4j:age ;
    sh:datatype xsd:integer ;
    sh:minInclusive 0 ;
    sh:maxInclusive 120 ;
    sh:minCount 1 ;
    sh:severity sh:Violation ;
    sh:message \"Age must be an integer between 0 and 120\" ;
  ] ;

  sh:property [
    sh:path neo4j:diagnosedWith ;
    sh:class neo4j:Disease ;
    sh:minCount 1 ;
    sh:severity sh:Violation ;
    sh:message \"Patient must be diagnosed with a Disease\" ;
  ] ;

  sh:property [
    sh:path neo4j:hasTumor ;
    sh:class neo4j:Tumor ;
    sh:minCount 1 ;
    sh:severity sh:Warning ;
    sh:message \"Patient should have at least one Tumor recorded\" ;
  ] .

lc:LungCancerShape a sh:NodeShape ;
  sh:targetClass neo4j:LungCancer ;

  sh:property [
    sh:path neo4j:hasStage ;
    sh:class neo4j:Stage ;
    sh:minCount 1 ;
    sh:severity sh:Violation ;
    sh:message \"LungCancer must have a Stage assigned\" ;
  ] .

lc:TherapyShape a sh:NodeShape ;
  sh:targetClass neo4j:Therapy ;

  sh:property [
    sh:path neo4j:usesDrug ;
    sh:class neo4j:Drug ;
    sh:minCount 1 ;
    sh:severity sh:Violation ;
    sh:message \"Therapy must use at least one Drug\" ;
  ] .
";

CALL n10s.validation.shacl.import.inline($shacl, "Turtle");

CALL n10s.validation.shacl.listShapes()
YIELD target, propertyOrRelationshipPath
RETURN target, propertyOrRelationshipPath;


CALL n10s.validation.shacl.validate()
YIELD focusNode, nodeType, resultMessage, severity
RETURN focusNode, nodeType, resultMessage, severity;
