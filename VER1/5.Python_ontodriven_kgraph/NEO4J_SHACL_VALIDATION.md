# Neo4j SHACL Validation Queries

This document shows how to perform SHACL validation directly in Neo4j using neosemantics (n10s).

## Prerequisites

1. Neo4j with neosemantics (n10s) plugin installed
2. Knowledge graph already loaded (see commands file)
3. n10s configured with `handleVocabUris: "MAP"`

---

## 1. Load SHACL Shapes into Neo4j

### Import SHACL shapes from file

```cypher
// Import SHACL shapes
CALL n10s.validation.shacl.import.fetch(
  "file:///H:/akash/git/CoherencePLM/version26/experiments/GraphDBExperiments/VER1/5.Python_ontodriven_kgraph/ttl_shacl_data/lung_cancer_shacl_shapes.ttl",
  "Turtle"
);
```

### OR: Import inline subset for quick testing

```cypher
CALL n10s.validation.shacl.import.inline('
@prefix : <http://lungkg.org/ontology#> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix neo4j: <neo4j://graph.schema#> .

:PatientShape a sh:NodeShape ;
  sh:targetClass neo4j:ns0__Patient ;
  
  sh:property [
    sh:path neo4j:ns0__patientId ;
    sh:datatype xsd:string ;
    sh:minCount 1 ;
    sh:severity sh:Violation ;
    sh:message "Patient must have a patientId" ;
  ] ;
  
  sh:property [
    sh:path neo4j:ns0__age ;
    sh:datatype xsd:integer ;
    sh:minInclusive 0 ;
    sh:maxInclusive 120 ;
    sh:severity sh:Violation ;
    sh:message "Patient age must be between 0 and 120" ;
  ] ;
  
  sh:property [
    sh:path neo4j:rdfs__label ;
    sh:minCount 1 ;
    sh:severity sh:Warning ;
    sh:message "Patient should have a label" ;
  ] .

:TherapyShape a sh:NodeShape ;
  sh:targetClass neo4j:ns0__Therapy ;
  
  sh:property [
    sh:path neo4j:ns0__usesDrug ;
    sh:class neo4j:ns0__Drug ;
    sh:minCount 1 ;
    sh:severity sh:Violation ;
    sh:message "Therapy must use at least one drug" ;
  ] .

', 'Turtle');
```

---

## 2. List Active SHACL Shapes

```cypher
// List all loaded shapes
CALL n10s.validation.shacl.listShapes()
YIELD target, propertyOrRelationshipPath, param, value
RETURN target, propertyOrRelationshipPath, param, value
ORDER BY target;
```

```cypher
// List shapes for specific class
CALL n10s.validation.shacl.listShapes()
YIELD target, propertyOrRelationshipPath, param, value
WHERE target = 'ns0__Patient'
RETURN propertyOrRelationshipPath, param, value;
```

---

## 3. Validate the Knowledge Graph

### Basic validation

```cypher
// Validate entire graph
CALL n10s.validation.shacl.validate()
YIELD focusNode, nodeType, shapeId, propertyShape, 
      offendingValue, resultPath, severity, resultMessage
RETURN focusNode, nodeType, resultMessage, severity
LIMIT 50;
```

### Validation summary by severity

```cypher
// Count issues by severity
CALL n10s.validation.shacl.validate()
YIELD severity
RETURN n10s.rdf.getIRILocalName(severity) as Severity, 
       count(*) AS Count
ORDER BY Count DESC;
```

### Detailed validation report

```cypher
CALL n10s.validation.shacl.validate()
YIELD focusNode, nodeType, shapeId, propertyShape,
      offendingValue, resultPath, severity, resultMessage
WHERE severity = 'http://www.w3.org/ns/shacl#Violation'
RETURN 
    n10s.rdf.getIRILocalName(focusNode) AS Node,
    nodeType AS NodeType,
    resultMessage AS Error,
    offendingValue AS InvalidValue,
    resultPath AS Property
LIMIT 100;
```

---

## 4. Test Validation by Breaking Constraints

### Remove patient age (should trigger violation)

```cypher
// Find a patient and remove age
MATCH (p:ns0__Patient)
WITH p LIMIT 1
REMOVE p.ns0__age
RETURN p.ns0__patientId AS ModifiedPatient;

// Validate - should show violation
CALL n10s.validation.shacl.validate()
YIELD focusNode, resultMessage, severity
WHERE severity CONTAINS 'Violation'
RETURN focusNode, resultMessage
LIMIT 10;

// Fix it
MATCH (p:ns0__Patient)
WHERE p.ns0__age IS NULL
SET p.ns0__age = 65
RETURN p.ns0__patientId AS Fixed;
```

### Set invalid age (should trigger violation)

```cypher
// Set age to invalid value
MATCH (p:ns0__Patient)
WITH p LIMIT 1
SET p.ns0__age = 150  // > 120 max
RETURN p.ns0__patientId AS ModifiedPatient;

// Validate
CALL n10s.validation.shacl.validate()
YIELD focusNode, resultMessage, offendingValue
WHERE resultMessage CONTAINS 'age'
RETURN focusNode, resultMessage, offendingValue;

// Fix it
MATCH (p:ns0__Patient)
WHERE p.ns0__age > 120
SET p.ns0__age = 65
RETURN count(p) AS Fixed;
```

---

## 5. Validate Specific Nodes

### Validate specific patient

```cypher
// Validate only Patient P001
MATCH (p:ns0__Patient {ns0__patientId: "P001"})
CALL n10s.validation.shacl.validateNode(p, {})
YIELD focusNode, resultMessage, severity
RETURN focusNode, resultMessage, severity;
```

### Validate all patients

```cypher
MATCH (p:ns0__Patient)
CALL n10s.validation.shacl.validateNode(p, {})
YIELD focusNode, resultMessage, severity
WHERE severity CONTAINS 'Violation'
RETURN p.ns0__patientId AS Patient, resultMessage
LIMIT 20;
```

---

## 6. Advanced: Custom Validation Queries

### Find patients without biomarker tests (should be tested if Stage IV)

```cypher
MATCH (p:ns0__Patient)-[:ns0__hasStage]->(s:ns0__Stage)
WHERE s.ns0__name = "IV"
  AND NOT exists((p)-[:ns0__testedForBiomarker]->())
RETURN p.ns0__patientId AS Patient,
       p.rdfs__label AS Label,
       "Stage IV patient missing biomarker testing" AS Issue;
```

### Find therapies without drugs (violates TherapyShape)

```cypher
MATCH (t:ns0__Therapy)
WHERE NOT exists((t)-[:ns0__usesDrug]->())
RETURN t.rdfs__label AS Therapy,
       "Therapy must use at least one drug" AS Issue;
```

### Find patients without outcomes after receiving therapy

```cypher
MATCH (p:ns0__Patient)-[:ns0__receivedTherapy]->()
WHERE NOT exists((p)-[:ns0__hasOutcome]->())
RETURN p.ns0__patientId AS Patient,
       p.rdfs__label AS Label,
       "Patient received therapy but has no outcome recorded" AS Issue;
```

---

## 7. Remove SHACL Shapes

```cypher
// Remove all SHACL shapes
CALL n10s.validation.shacl.drop();

// Verify shapes are removed
CALL n10s.validation.shacl.listShapes()
YIELD target
RETURN count(target) AS RemainingShapes;
```

---

## 8. Validation Workflow

### Complete validation workflow

```cypher
// 1. Import shapes
CALL n10s.validation.shacl.import.fetch(
  "file:///H:/akash/git/CoherencePLM/version26/experiments/GraphDBExperiments/VER1/5.Python_ontodriven_kgraph/ttl_shacl_data/lung_cancer_shacl_shapes.ttl",
  "Turtle"
);

// 2. Check what was loaded
CALL n10s.validation.shacl.listShapes()
YIELD target
RETURN DISTINCT target;

// 3. Validate graph
CALL n10s.validation.shacl.validate()
YIELD severity, resultMessage
RETURN n10s.rdf.getIRILocalName(severity) AS Severity,
       resultMessage AS Message,
       count(*) AS Count
GROUP BY severity, resultMessage
ORDER BY Severity, Count DESC;

// 4. Get detailed violations
CALL n10s.validation.shacl.validate()
YIELD focusNode, nodeType, resultMessage, offendingValue, severity
WHERE severity = 'http://www.w3.org/ns/shacl#Violation'
RETURN 
    n10s.rdf.getIRILocalName(focusNode) AS Node,
    nodeType,
    resultMessage,
    offendingValue
LIMIT 50;
```

---

## 9. Export Validation Report

```cypher
// Export validation results to CSV
CALL n10s.validation.shacl.validate()
YIELD focusNode, nodeType, resultMessage, severity
WITH collect({
    node: n10s.rdf.getIRILocalName(focusNode),
    type: nodeType,
    message: resultMessage,
    severity: n10s.rdf.getIRILocalName(severity)
}) AS validationResults
CALL apoc.export.json.data(
    [],
    [],
    "shacl_validation_report.json",
    {data: validationResults}
)
YIELD file, nodes, relationships
RETURN file, nodes, relationships;
```

---

## 10. Continuous Validation

### Create trigger to validate on data change (requires APOC)

```cypher
// Note: This is pseudocode - actual implementation may vary
// Validate after data modifications
CALL apoc.trigger.add(
  'validatePatient',
  'CALL n10s.validation.shacl.validateNode($createdNode, {})
   YIELD resultMessage, severity
   WHERE severity CONTAINS "Violation"
   WITH collect(resultMessage) as violations
   WHERE size(violations) > 0
   CALL apoc.log.error("SHACL Validation Failed: " + violations[0])
   RETURN violations',
  {phase: 'after'}
);
```

---

## Notes

- SHACL validation in Neo4j requires the **neosemantics (n10s)** plugin
- Shapes use `neo4j://graph.schema#` namespace for Neo4j node labels and properties
- Convert ontology namespaces to Neo4j format: `ont:Patient` → `neo4j:ns0__Patient`
- Severity levels: `sh:Violation` (must fix), `sh:Warning` (should fix), `sh:Info` (optional)
- Validation can be resource-intensive on large graphs
