LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/lavishlyinspired/GraphDBExperiments/refs/heads/main/VER1/Lungcancerinfo.csv' AS row
CREATE (a:Article { uri: row.uri})
SET a.title = row.title, a.body = row.body, a.datetime = datetime(row.date);

CREATE CONSTRAINT article_uri IF NOT EXISTS
FOR (a:Article) REQUIRE a.uri IS UNIQUE;

CALL n10s.graphconfig.init({
  handleVocabUris: "IGNORE",
  applyNeo4jNaming: true,
  keepLangTag: false
});


# Create indexes for NLP/text matching (important for speed)
CREATE FULLTEXT INDEX articleBodyIndex
FOR (a:Article)
ON EACH [a.body];


#CALL apoc.export.json.all("graph.json", {})


:param key => "YOUR_GCP_API_KEY_HERE";

Step 1 — deterministic disease link
MATCH (a:Article),(lc:LungCancer)
MERGE (a)-[:ABOUT]->(lc);

Step 2 — FIXED NLP query


CALL apoc.periodic.iterate(

"MATCH (a:Article)
 WHERE a.processed IS NULL
 RETURN a",

"
CALL apoc.nlp.gcp.entities.stream([item in $_batch | item.a], {
   nodeProperty: 'body',
   key: $key
})
YIELD node, value

SET node.processed = true

WITH node, value
UNWIND value.entities AS entity

WITH node, entity

// ---------- PATIENT ----------
OPTIONAL MATCH (p:Patient)
WHERE toLower(entity.name) CONTAINS toLower(p.name)

FOREACH (_ IN CASE WHEN p IS NOT NULL THEN [1] ELSE [] END |
  MERGE (node)-[:ABOUT]->(p)
)

WITH node, entity   // REQUIRED

// ---------- DISEASE ----------
OPTIONAL MATCH (d:LungCancer)
WHERE toLower(entity.name) CONTAINS toLower(d.name)

FOREACH (_ IN CASE WHEN d IS NOT NULL THEN [1] ELSE [] END |
  MERGE (node)-[:ABOUT]->(d)
)

WITH node, entity   // REQUIRED

// ---------- CONCEPTS ----------
OPTIONAL MATCH (c)
WHERE (c:Symptom OR c:Treatment OR c:Hospital OR c:CancerType)
  AND toLower(entity.name) CONTAINS toLower(c.name)

FOREACH (_ IN CASE WHEN c IS NOT NULL THEN [1] ELSE [] END |
  MERGE (node)-[:REFERS_TO]->(c)
)
",

{batchSize:10, batchMode:'BATCH_SINGLE', params:{key:$key}}

);



Link Articles → Ontology concepts (simple keyword approach) If you want deterministic linking without NLP:

Example:

MATCH (a:Article), (c:Class {name:'LungCancer'})
WHERE toLower(a.body) CONTAINS 'lung cancer'
MERGE (a)-[:REFERS_TO]->(c);


#Full Path Semantic Exploration (Bloom style)
MATCH path =
(p:Patient {name:"John"})
-[:hasDiagnosis|hasSymptom|receivesTreatment*1..2]-()
<-[:ABOUT|REFERS_TO*1..2]-(a:Article)
RETURN path;

#Similar Articles Based on Same CancerType
MATCH (a:Article)-[:ABOUT]->(lc:LungCancer)
-[:hasType]->(ct:CancerType)
<-[:hasType]-(otherLc:LungCancer)
<-[:ABOUT]-(other:Article)
WHERE a.uri = "https://pmc.ncbi.nlm.nih.gov/articles/PMC9392234/"
RETURN DISTINCT other.title;


#Find articles similar to a given article based on shared disease or symptoms:
MATCH (a:Article {uri:"https://pmc.ncbi.nlm.nih.gov/articles/PMC9392234/"})
-[:ABOUT|REFERS_TO]->(concept)
<-[:ABOUT|REFERS_TO]-(other:Article)
WHERE a <> other
RETURN DISTINCT other.title;


#Articles about Stage III NSCLC
MATCH (ct:CancerType {name:"NSCLC"})
<-[:hasType]-(lc:LungCancer)
-[:hasStage]->(s:Stage {name:"StageIII"})
<-[:hasStage]-(lc)
<-[:ABOUT]-(a:Article)
RETURN DISTINCT a.title;


#Articles about patients treated with Chemo  
MATCH (t:Treatment {name:"Chemo"})
<-[:receivesTreatment]-(p:Patient)
-[:hasDiagnosis]->(lc:LungCancer)
<-[:ABOUT]-(a:Article)
RETURN DISTINCT a.title;



#Articles on NSCLC (subcategory of LungCancer)
MATCH path =
(ct:CancerType {name:"NSCLC"})
<-[:hasType]-(lc:LungCancer)
<-[:ABOUT]-(a:Article)
RETURN a.title, [x IN nodes(path) | coalesce(x.name,"")];


“NSCLC AND StageIII”

MATCH (a:Article)
WHERE EXISTS {
  MATCH (a)-[:ABOUT]->(:LungCancer)-[:hasType]->(:CancerType {name:"NSCLC"})
}
AND EXISTS {
  MATCH (a)-[:ABOUT]->(:LungCancer)-[:hasStage]->(:Stage {name:"StageIII"})
}
RETURN a.title;

#Find articles that talk about same things
MATCH (a:Article {uri:"https://pmc.ncbi.nlm.nih.gov/articles/PMC9392234/"})
-[:ABOUT|REFERS_TO]->(concept)
WHERE NOT concept:Class
MATCH (other:Article)-[:ABOUT|REFERS_TO]->(concept)
WHERE other <> a

WITH other, collect(DISTINCT concept.name) AS sharedConcepts

RETURN other.title,
       size(sharedConcepts) AS similarityScore,
       sharedConcepts
ORDER BY similarityScore DESC;








