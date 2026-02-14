Load a subset of SHACL shapes (inline – quick test)

call n10s.validation.shacl.import.inline('

@prefix lc: <http://example.org/lungCancer#> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix neo4j: <neo4j://graph.schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

#################################################
# Patient rules
#################################################

lc:PatientShape a sh:NodeShape ;
  sh:targetClass neo4j:Patient ;

  sh:property [
    sh:path neo4j:name ;
    sh:datatype xsd:string ;
    sh:minCount 1 ;
    sh:severity sh:Violation ;
    sh:message "Patient must have a name" ;
  ] ;

  sh:property [
    sh:path neo4j:age ;
    sh:datatype xsd:integer ;
    sh:minInclusive 0 ;
    sh:maxInclusive 120 ;
    sh:minCount 1 ;
  ] ;

  sh:property [
    sh:path neo4j:hasDiagnosis ;
    sh:minCount 1 ;
    sh:severity sh:Violation ;
  ] .

#################################################
# Lung cancer rules
#################################################

lc:LungCancerShape a sh:NodeShape ;
  sh:targetClass neo4j:LungCancer ;

  sh:property [
    sh:path neo4j:hasStage ;
    sh:minCount 1 ;
    sh:severity sh:Violation ;
  ] ;

  sh:property [
    sh:path neo4j:hasType ;
    sh:minCount 1 ;
  ] .

','Turtle')

Validate the graph
call n10s.validation.shacl.validate()

Break the graph manually (test violation)
match (p:Patient)
with p limit 1
remove p.name
return p

Validate again (should show violations)
call n10s.validation.shacl.validate()




List shapes active for Patient
call n10s.validation.shacl.listShapes()
yield target, propertyOrRelationshipPath, param, value
where target = 'Patient'
return *

Full validation with details
call n10s.validation.shacl.validate()
yield focusNode, nodeType, shapeId, propertyShape,
      offendingValue, resultPath, severity, resultMessage
return *

Aggregate by severity
call n10s.validation.shacl.validate()
yield severity
return n10s.rdf.getIRILocalName(severity) as severity, count(*)

add again
match (p:Patient)
with p limit 1
set p.name = "John"
return p


<!-- 
Based on  imported graph:

John has name + age → passes

hasDiagnosis → required

hasStage + hasType on LC1 → required

Treatment + Article completeness checked

 -->

Load full file into Neo4j

Place file locally (or GitHub raw URL) then:

call n10s.validation.shacl.import.fetch(
"file:///lungcancer-shacl.ttl",
"Turtle")


or

call n10s.validation.shacl.import.fetch(
"https://yourrepo/lungcancer-shacl.ttl",
"Turtle")