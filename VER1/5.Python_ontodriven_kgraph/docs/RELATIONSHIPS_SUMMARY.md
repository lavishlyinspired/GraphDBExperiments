# Complete Relationship Mapping - Lung Cancer Knowledge Graph

## ✅ All 13 Required Relationships

### 1. **usesDrug** 
- **Domain**: Therapy
- **Range**: Drug
- **Generated in instances**: ✅ Yes
- **Source**: lung_treatments.csv via therapies mapping
- **Example**: `res:Therapy_P001_Osimertinib ont:usesDrug res:Drug_Osimertinib`

### 2. **hasStage**
- **Domain**: Tumor, Patient
- **Range**: Stage
- **Generated in instances**: ✅ Yes
- **Source**: lung_patients.csv via patients and tumors mapping
- **Example**: 
  - `res:Patient_P001 ont:hasStage res:Stage_IV`
  - `res:Tumor_P001 ont:hasStage res:Stage_IV`

### 3. **recommends**
- **Domain**: Guideline
- **Range**: Therapy
- **Generated in instances**: ⚠️ Schema only (static example)
- **Source**: lung_cancer_kg_schema.ttl
- **Example**: `ont:EGFR_Guideline ont:recommends ont:EGFR_Targeted_Therapy`
- **Note**: Pre-defined in schema for guideline-based reasoning; not generated from CSV data

### 4. **hasMutation**
- **Domain**: Biomarker
- **Range**: Mutation
- **Generated in instances**: ✅ Yes
- **Source**: lung_mutations.csv via biomarkers mapping
- **Example**: `res:Biomarker_EGFR ont:hasMutation res:Mutation_L858R`

### 5. **hasGene**
- **Domain**: Biomarker
- **Range**: Gene
- **Generated in instances**: ✅ Yes
- **Source**: lung_mutations.csv via biomarkers mapping
- **Example**: `res:Biomarker_EGFR ont:hasGene res:Gene_EGFR`

### 6. **hasHistology**
- **Domain**: Tumor, Patient
- **Range**: Histology
- **Generated in instances**: ✅ Yes
- **Source**: lung_patients.csv via patients and tumors mapping
- **Example**: 
  - `res:Patient_P001 ont:hasHistology res:Histology_Adenocarcinoma`
  - `res:Tumor_P001 ont:hasHistology res:Histology_Adenocarcinoma`

### 7. **underwentTest**
- **Domain**: Patient
- **Range**: Test (GenomicTest)
- **Generated in instances**: ✅ Yes
- **Source**: lung_mutations.csv via mutations mapping (inferred: patients with biomarker data underwent testing)
- **Example**: `res:Patient_P001 ont:underwentTest res:GenomicTest_P001`

### 8. **hasTumor**
- **Domain**: Patient
- **Range**: Tumor
- **Generated in instances**: ✅ Yes
- **Source**: lung_patients.csv via patients mapping
- **Example**: `res:Patient_P001 ont:hasTumor res:Tumor_P001`

### 9. **triggers**
- **Domain**: ClinicalRule
- **Range**: Therapy
- **Generated in instances**: ⚠️ Schema only (not used)
- **Source**: lung_cancer_kg_schema.ttl
- **Note**: Defined in schema for clinical decision rules; no rules currently defined in data

### 10. **hasOutcome**
- **Domain**: Patient
- **Range**: Outcome
- **Generated in instances**: ✅ Yes
- **Source**: lung_treatments.csv via treatments mapping
- **Example**: `res:Patient_P001 ont:hasOutcome res:Outcome_P001_Partial_Response`

### 11. **testedForBiomarker**
- **Domain**: Patient
- **Range**: Biomarker
- **Generated in instances**: ✅ Yes
- **Source**: lung_mutations.csv via mutations mapping
- **Example**: `res:Patient_P001 ont:testedForBiomarker res:Biomarker_EGFR`

### 12. **diagnosedWith**
- **Domain**: Patient
- **Range**: Disease (LungCancer)
- **Generated in instances**: ✅ Yes
- **Source**: lung_patients.csv via patients mapping (all patients diagnosed with LungCancer)
- **Example**: `res:Patient_P001 ont:diagnosedWith ont:LungCancer`

### 13. **receivedTherapy**
- **Domain**: Patient
- **Range**: Therapy
- **Generated in instances**: ✅ Yes
- **Source**: lung_treatments.csv via treatments mapping
- **Example**: `res:Patient_P001 ont:receivedTherapy res:Therapy_P001_Osimertinib`

---

## 📊 Summary Statistics

| Status | Count | Relationships |
|--------|-------|---------------|
| ✅ Generated from data | 11 | usesDrug, hasStage, hasMutation, hasGene, hasHistology, underwentTest, hasTumor, hasOutcome, testedForBiomarker, diagnosedWith, receivedTherapy |
| ⚠️ Schema only | 2 | recommends, triggers |
| **Total** | **13** | **All relationships defined** |

---

## 🔍 Neo4j Verification Queries

### Check All Relationship Types
```cypher
CALL db.relationshipTypes() YIELD relationshipType
WHERE relationshipType STARTS WITH 'ns0__'
RETURN relationshipType
ORDER BY relationshipType;
```

### Expected Results (13 relationships)
```
ns0__diagnosedWith
ns0__hasGene
ns0__hasHistology
ns0__hasMutation
ns0__hasOutcome
ns0__hasStage
ns0__hasTumor
ns0__receivedTherapy
ns0__recommends
ns0__testedForBiomarker
ns0__triggers
ns0__underwentTest
ns0__usesDrug
```

### Count Each Relationship Type
```cypher
MATCH ()-[r]->()
WHERE type(r) STARTS WITH 'ns0__'
RETURN type(r) AS RelationshipType, count(r) AS Count
ORDER BY Count DESC;
```

### Sample Relationship Paths
```cypher
// Patient → Therapy → Drug
MATCH (p:ns0__Patient)-[:ns0__receivedTherapy]->(t:ns0__Therapy)-[:ns0__usesDrug]->(d:ns0__Drug)
RETURN p.rdfs__label, t.rdfs__label, d.rdfs__label
LIMIT 5;

// Patient → Biomarker → Gene + Mutation
MATCH (p:ns0__Patient)-[:ns0__testedForBiomarker]->(b:ns0__Biomarker)
      -[:ns0__hasGene]->(g:ns0__Gene)
MATCH (b)-[:ns0__hasMutation]->(m:ns0__Mutation)
RETURN p.rdfs__label, b.rdfs__label, g.rdfs__label, m.rdfs__label
LIMIT 5;

// Patient → Tumor → Stage + Histology
MATCH (p:ns0__Patient)-[:ns0__hasTumor]->(t:ns0__Tumor)
      -[:ns0__hasStage]->(s:ns0__Stage)
MATCH (t)-[:ns0__hasHistology]->(h:ns0__Histology)
RETURN p.rdfs__label, t.rdfs__label, s.rdfs__label, h.rdfs__label
LIMIT 5;
```

---

## 📂 Mapping Configuration

### Current mapping_config.json sections:

1. **patients**: Creates Patient entities with relationships to Tumor, Stage, Histology, LungCancer, Therapy, Outcome, Biomarker, GenomicTest
2. **tumors**: Creates Tumor entities with relationships to Stage and Histology
3. **mutations**: Links Patients to Biomarkers and GenomicTests
4. **biomarkers**: Creates Biomarker entities with relationships to Genes and Mutations
5. **genomic_tests**: Creates GenomicTest entities
6. **treatments**: Links Patients to Therapies and Outcomes
7. **therapies**: Creates Therapy entities with relationships to Drugs

---

## ✅ Validation Checklist

- [x] All 13 relationships defined in schema (lung_cancer_kg_schema.ttl)
- [x] 11 relationships actively generated from CSV data
- [x] 2 relationships available for guideline/rule-based reasoning
- [x] Each relationship has rdfs:label for human readability
- [x] Each relationship has rdfs:comment for documentation
- [x] All entities connected by relationships have rdf:type
- [x] All entities have rdfs:label for Neo4j visualization
- [x] ETL handles both template-based and fixed class references
- [x] Neo4j import configured with handleVocabUris: "MAP"

---

## 🚀 Next Steps

1. **Import to Neo4j**: Follow [commands](commands) file for complete import workflow
2. **Verify Relationships**: Run Neo4j verification queries above
3. **SHACL Validation**: Run `python validate_shacl.py` to validate relationship integrity
4. **SPARQL Queries**: Run `python run_sparql_queries.py` to query relationships

---

**Generated**: February 14, 2026  
**Data Source**: lung_patients.csv, lung_mutations.csv, lung_treatments.csv  
**Ontology**: lung_cancer_kg_schema.ttl  
**Instances**: lung_cancer_instances_out.ttl
