
## queries_cypher_sparql1 Quick sanity check:

MATCH (n) RETURN labels(n), count(*) ORDER BY count(*) DESC;

🧠 Step 1 — Surface implicit semantics (manual query first)

Example:
A Patient is someone who hasDiagnosis → LungCancer

Query
MATCH (p)-[:hasDiagnosis]->(:LungCancer)
RETURN DISTINCT p.hasName AS patientName

Enrich graph manually (classic way)
MATCH (p)-[:hasDiagnosis]->(:LungCancer)
SET p:CancerPatient


But again… this meaning is only in your head + Cypher.

Let’s make it explicit.

 Step 2 —  (define ontology in-graph)

We describe semantics as metadata.

Define categories + relationships
CancerPatient

MERGE (from:_Category {name:"CancerPatient"})
MERGE (to:_Category {name:"LungCancer"})
MERGE (from)<-[:_from]-(r:_Relationship {name:"hasDiagnosis"})-[:_to]->(to);


Meaning:

if X —hasDiagnosis→ Y
then X is CancerPatient, Y is LungCancer

TreatedPatient
MERGE (from:_Category {name:"TreatedPatient"})
MERGE (to:_Category {name:"Treatment"})
MERGE (from)<-[:_from]-(r:_Relationship {name:"receivesTreatment"})-[:_to]->(to);

SymptomaticPatient
MERGE (from:_Category {name:"SymptomaticPatient"})
MERGE (to:_Category {name:"Symptom"})
MERGE (from)<-[:_from]-(r:_Relationship {name:"hasSymptom"})-[:_to]->(to);

🧠 Step 3 — META query (see inferred meaning)
MATCH (from:_Category)<-[:_from]-(r:_Relationship)-[:_to]->(to:_Category)
MATCH (x)-[rel]->(y)
WHERE type(rel) = r.name
RETURN x, " is a " + from.name, y, " is a " + to.name;


You should see results like:

John is a CancerPatient
LC1 is a LungCancer
John is a TreatedPatient
John is a SymptomaticPatient

🧠 Step 4 — Micro-inferencing engine (materialize labels)

Same generic script, no hardcoding:

MATCH (from:_Category)<-[:_from]-(r:_Relationship)-[:_to]->(to:_Category)
MATCH (x)-[rel]->(y)
WHERE type(rel) = r.name
CALL apoc.create.addLabels(x,[from.name]) YIELD node AS xs
CALL apoc.create.addLabels(y,[to.name]) YIELD node AS ys
RETURN count(xs) + count(ys) + " nodes updated";


Now:

MATCH (p:CancerPatient) RETURN p;


works instantly.

🧠 Step 5 — Automate with trigger (recommended)
CALL apoc.trigger.add(
'microinferencer',
'
MATCH (from:_Category)<-[:_from]-(r:_Relationship)-[:_to]->(to:_Category)
MATCH (x)-[rel]->(y)
WHERE rel IN $createdRelationships AND type(rel) = r.name
CALL apoc.create.addLabels(x,[from.name]) YIELD node
CALL apoc.create.addLabels(y,[to.name]) YIELD node
RETURN count(*)
',
{phase:"before"});

🧠 Step 6 — Test it live
MERGE (p:Patient {name:"Alice", age:55})
MERGE (c:LungCancer {name:"LC2"})
MERGE (p)-[:hasDiagnosis]->(c)


Immediately:

MATCH (p:CancerPatient) RETURN p.name;


👉 Alice appears automatically.

No manual labeling needed.

🧠 Step 7 — Using OWL ontology instead (n10s reasoning)

Instead of hand-building _Category, you can load an OWL ontology.

Config (same as movie demo)
CREATE CONSTRAINT n10s_unique_uri
FOR (r:Resource) REQUIRE r.uri IS UNIQUE;

CALL n10s.graphconfig.init({
  handleVocabUris:"IGNORE",
  classLabel:"_Category",
  objectPropertyLabel:"_Relationship",
  domainRel:"_from",
  rangeRel:"_to",
  force:true
});

LungCancer OWL (inline)

Use parameter method (safe):

:param onto => "
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix lc: <http://example.org/lungCancer#> .

lc:Patient a owl:Class .
lc:CancerPatient a owl:Class .
lc:CancerPatient rdfs:subClassOf lc:Patient .

lc:hasDiagnosis a owl:ObjectProperty ;
  rdfs:domain lc:CancerPatient ;
  rdfs:range lc:LungCancer .

lc:receivesTreatment a owl:ObjectProperty ;
  rdfs:domain lc:Patient ;
  rdfs:range lc:Treatment .
";

CALL n10s.onto.import.inline($onto,"Turtle");

Query with on-the-fly inference

No labels required:

CALL n10s.inference.nodesLabelled("CancerPatient");