# Lung Cancer Knowledge Graph - SPARQL & Cypher Queries

This document provides equivalent queries in both SPARQL (for Protégé/SPARQL endpoints) and Cypher (for Neo4j with neosemantics).

## Setup

### SPARQL (Protégé or Apache Jena Fuseki)
```sparql
PREFIX : <http://lungkg.org/ontology#>
PREFIX res: <http://lungkg.org/resource/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
```

### Cypher (Neo4j)
After importing with n10s, use namespace prefix `ns0__` for ontology properties.

---

## Query 1: List All Patients

### SPARQL
```sparql
PREFIX : <http://lungkg.org/ontology#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?patient ?label ?age ?sex
WHERE {
  ?patient a :Patient ;
           rdfs:label ?label ;
           :age ?age ;
           :sex ?sex .
}
ORDER BY ?age
```

### Cypher
```cypher
MATCH (p:ns0__Patient)
RETURN p.ns0__patientId AS PatientID,
       p.rdfs__label AS Patient,
       p.ns0__age AS Age,
       p.ns0__sex AS Sex
ORDER BY p.ns0__age
```

---

## Query 2: Patients with Stage IV Cancer

### SPARQL
```sparql
PREFIX : <http://lungkg.org/ontology#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?patientLabel ?age ?stage
WHERE {
  ?patient a :Patient ;
           rdfs:label ?patientLabel ;
           :age ?age ;
           :hasStage ?stageNode .
  
  ?stageNode :name ?stage .
  
  FILTER(?stage = "IV")
}
ORDER BY ?age
```

### Cypher
```cypher
MATCH (p:ns0__Patient)-[:ns0__hasStage]->(s:ns0__Stage)
WHERE s.ns0__name = "IV"
RETURN p.rdfs__label AS Patient,
       p.ns0__age AS Age,
       s.rdfs__label AS Stage
ORDER BY p.ns0__age
```

---

## Query 3: Patients with Their Treatments and Drugs

### SPARQL
```sparql
PREFIX : <http://lungkg.org/ontology#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?patientLabel ?therapyLabel ?drugLabel
WHERE {
  ?patient a :Patient ;
           rdfs:label ?patientLabel ;
           :receivedTherapy ?therapy .
  
  ?therapy rdfs:label ?therapyLabel ;
           :usesDrug ?drug .
  
  ?drug rdfs:label ?drugLabel .
}
ORDER BY ?patientLabel
```

### Cypher
```cypher
MATCH (p:ns0__Patient)-[:ns0__receivedTherapy]->(t:ns0__Therapy)-[:ns0__usesDrug]->(d:ns0__Drug)
RETURN p.rdfs__label AS Patient,
       t.rdfs__label AS Therapy,
       d.rdfs__label AS Drug
ORDER BY p.rdfs__label
```

---

## Query 4: Biomarker Testing Results by Gene

### SPARQL
```sparql
PREFIX : <http://lungkg.org/ontology#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?patientLabel ?biomarkerLabel
WHERE {
  ?patient a :Patient ;
           rdfs:label ?patientLabel ;
           :testedForBiomarker ?biomarker .
  
  ?biomarker rdfs:label ?biomarkerLabel .
}
ORDER BY ?biomarkerLabel ?patientLabel
```

### Cypher
```cypher
MATCH (p:ns0__Patient)-[:ns0__testedForBiomarker]->(b:ns0__Biomarker)
RETURN b.rdfs__label AS Biomarker,
       collect(p.rdfs__label) AS Patients,
       count(p) AS PatientCount
ORDER BY PatientCount DESC
```

---

## Query 5: Group Patients by Biomarker

### SPARQL
```sparql
PREFIX : <http://lungkg.org/ontology#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?biomarkerLabel (COUNT(?patient) AS ?patientCount)
WHERE {
  ?patient a :Patient ;
           :testedForBiomarker ?biomarker .
  
  ?biomarker rdfs:label ?biomarkerLabel .
}
GROUP BY ?biomarkerLabel
ORDER BY DESC(?patientCount)
```

### Cypher
```cypher
MATCH (p:ns0__Patient)-[:ns0__testedForBiomarker]->(b:ns0__Biomarker)
RETURN b.rdfs__label AS Biomarker,
       count(p) AS PatientCount
ORDER BY PatientCount DESC
```

---

## Query 6: Treatment Outcomes

### SPARQL
```sparql
PREFIX : <http://lungkg.org/ontology#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?patientLabel ?therapyLabel ?outcomeLabel
WHERE {
  ?patient a :Patient ;
           rdfs:label ?patientLabel ;
           :receivedTherapy ?therapy ;
           :hasOutcome ?outcome .
  
  ?therapy rdfs:label ?therapyLabel .
  ?outcome rdfs:label ?outcomeLabel .
}
ORDER BY ?patientLabel
```

### Cypher
```cypher
MATCH (p:ns0__Patient)-[:ns0__receivedTherapy]->(t:ns0__Therapy),
      (p)-[:ns0__hasOutcome]->(o:ns0__Outcome)
RETURN p.rdfs__label AS Patient,
       t.rdfs__label AS Therapy,
       o.rdfs__label AS Outcome
ORDER BY p.rdfs__label
```

---

## Query 7: Complex - EGFR Positive patients with Targeted Therapy

### SPARQL
```sparql
PREFIX : <http://lungkg.org/ontology#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?patientLabel ?age ?drugLabel ?outcomeLabel
WHERE {
  ?patient a :Patient ;
           rdfs:label ?patientLabel ;
           :age ?age ;
           :testedForBiomarker ?biomarker ;
           :receivedTherapy ?therapy ;
           :hasOutcome ?outcome .
  
  ?biomarker rdfs:label ?biomarkerLabel .
  FILTER(CONTAINS(?biomarkerLabel, "EGFR"))
  
  ?therapy :usesDrug ?drug .
  ?drug rdfs:label ?drugLabel .
  
  ?outcome rdfs:label ?outcomeLabel .
}
ORDER BY ?age
```

### Cypher
```cypher
MATCH (p:ns0__Patient)-[:ns0__testedForBiomarker]->(b:ns0__Biomarker),
      (p)-[:ns0__receivedTherapy]->(t:ns0__Therapy)-[:ns0__usesDrug]->(d:ns0__Drug),
      (p)-[:ns0__hasOutcome]->(o:ns0__Outcome)
WHERE b.rdfs__label CONTAINS "EGFR"
RETURN p.rdfs__label AS Patient,
       p.ns0__age AS Age,
       d.rdfs__label AS Drug,
       o.rdfs__label AS Outcome
ORDER BY p.ns0__age
```

---

## Query 8: Histogram of Patients by Stage

### SPARQL
```sparql
PREFIX : <http://lungkg.org/ontology#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?stageName (COUNT(?patient) AS ?count)
WHERE {
  ?patient a :Patient ;
           :hasStage ?stage .
  
  ?stage :name ?stageName .
}
GROUP BY ?stageName
ORDER BY ?stageName
```

### Cypher
```cypher
MATCH (p:ns0__Patient)-[:ns0__hasStage]->(s:ns0__Stage)
RETURN s.ns0__name AS Stage,
       count(p) AS PatientCount
ORDER BY s.ns0__name
```

---

## Query 9: Patients with Histology Type

### SPARQL
```sparql
PREFIX : <http://lungkg.org/ontology#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?patientLabel ?histologyLabel ?stageLabel
WHERE {
  ?patient a :Patient ;
           rdfs:label ?patientLabel ;
           :hasHistology ?histology ;
           :hasStage ?stage .
  
  ?histology rdfs:label ?histologyLabel .
  ?stage rdfs:label ?stageLabel .
}
ORDER BY ?histologyLabel ?patientLabel
```

### Cypher
```cypher
MATCH (p:ns0__Patient)-[:ns0__hasHistology]->(h:ns0__Histology),
      (p)-[:ns0__hasStage]->(s:ns0__Stage)
RETURN h.rdfs__label AS Histology,
       p.rdfs__label AS Patient,
       s.rdfs__label AS Stage
ORDER BY h.rdfs__label, p.rdfs__label
```

---

## Query 10: Complete Patient Graph (1-hop neighborhood)

### SPARQL
```sparql
PREFIX : <http://lungkg.org/ontology#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX res: <http://lungkg.org/resource/>

CONSTRUCT {
  ?patient ?p ?o .
  ?o rdfs:label ?oLabel .
}
WHERE {
  BIND(res:Patient_P001 AS ?patient)
  
  ?patient ?p ?o .
  
  OPTIONAL { ?o rdfs:label ?oLabel }
}
```

### Cypher
```cypher
MATCH path = (p:ns0__Patient {ns0__patientId: "P001"})-[*1]->(connected)
RETURN path
```

---

## Query 11: Advanced - Find Similar Patients

### SPARQL
```sparql
PREFIX : <http://lungkg.org/ontology#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

# Find patients with same stage and histology
SELECT ?patient1Label ?patient2Label ?stageLabel ?histologyLabel
WHERE {
  ?patient1 a :Patient ;
            rdfs:label ?patient1Label ;
            :hasStage ?stage ;
            :hasHistology ?histology .
  
  ?patient2 a :Patient ;
            rdfs:label ?patient2Label ;
            :hasStage ?stage ;
            :hasHistology ?histology .
  
  ?stage rdfs:label ?stageLabel .
  ?histology rdfs:label ?histologyLabel .
  
  FILTER(?patient1 != ?patient2)
  FILTER(STR(?patient1) < STR(?patient2))  # Avoid duplicates
}
ORDER BY ?stageLabel ?histologyLabel
```

### Cypher
```cypher
MATCH (p1:ns0__Patient)-[:ns0__hasStage]->(s:ns0__Stage),
      (p1)-[:ns0__hasHistology]->(h:ns0__Histology),
      (p2:ns0__Patient)-[:ns0__hasStage]->(s),
      (p2)-[:ns0__hasHistology]->(h)
WHERE id(p1) < id(p2)
RETURN p1.rdfs__label AS Patient1,
       p2.rdfs__label AS Patient2,
       s.rdfs__label AS Stage,
       h.rdfs__label AS Histology
ORDER BY s.rdfs__label, h.rdfs__label
```

---

## Query 12: Reasoning - Infer High-Risk Patients

### SPARQL
```sparql
PREFIX : <http://lungkg.org/ontology#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

# High risk: Stage IV + smoking history
SELECT ?patientLabel ?age ?smokingPackYears ?stageLabel
WHERE {
  ?patient a :Patient ;
           rdfs:label ?patientLabel ;
           :age ?age ;
           :smokingPackYears ?smokingPackYears ;
           :hasStage ?stage .
  
  ?stage :name "IV" ;
         rdfs:label ?stageLabel .
  
  FILTER(?smokingPackYears > 20)
}
ORDER BY DESC(?smokingPackYears)
```

### Cypher
```cypher
MATCH (p:ns0__Patient)-[:ns0__hasStage]->(s:ns0__Stage)
WHERE s.ns0__name = "IV"
  AND p.ns0__smokingPackYears > 20
RETURN p.rdfs__label AS Patient,
       p.ns0__age AS Age,
       p.ns0__smokingPackYears AS PackYears,
       s.rdfs__label AS Stage
ORDER BY p.ns0__smokingPackYears DESC
```

---

## Running SPARQL Queries

### In Protégé:
1. Load lung_cancer_kg_schema.ttl
2. Load lung_cancer_instances_out.ttl
3. Go to Window → Tabs → SPARQL Query
4. Paste query and execute

### In Apache Jena Fuseki:
```bash
# Start Fuseki server
fuseki-server --file=lung_cancer_instances_out.ttl /lungkg

# Query via REST API
curl -X POST http://localhost:3030/lungkg/sparql \
  -H "Content-Type: application/sparql-query" \
  --data-binary @query.sparql
```

### In Python with rdflib:
```python
from rdflib import Graph

g = Graph()
g.parse("ouput/lung_cancer_instances_out.ttl")

query = """
PREFIX : <http://lungkg.org/ontology#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?patient ?label WHERE {
  ?patient a :Patient ;
           rdfs:label ?label .
}
"""

for row in g.query(query):
    print(f"{row.patient} - {row.label}")
```
