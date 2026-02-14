# Lung Cancer Knowledge Graph - Ontology-Driven ETL with SHACL & SPARQL

A comprehensive knowledge graph solution for lung cancer clinical data with:
- ✅ Ontology-driven data modeling
- ✅ Python ETL engine
- ✅ SHACL validation (Python & Neo4j)
- ✅ SPARQL querying
- ✅ Neo4j integration with neosemantics
- ✅ Automated Cypher generation

## 📁 Project Structure

```
5.Python_ontodriven_kgraph/
├── ttl_shacl_data/
│   ├── lung_cancer_kg_schema.ttl          # OWL ontology schema
│   ├── lung_cancer_shacl_shapes.ttl       # SHACL validation shapes
│   ├── mapping_config.json                # CSV-to-RDF mapping configuration
│   ├── lung_patients.csv                  # Patient data
│   ├── lung_mutations.csv                 # Biomarker test data
│   └── lung_treatments.csv                # Treatment data
│
├── ouput/
│   ├── lung_cancer_instances_out.ttl      # Generated RDF instances
│   ├── auto_generated.cypher              # Generated Cypher queries
│   └── shacl_validation_report.txt        # Validation report
│
├── lung_cancer_etl_engine.py              # Main ETL script
├── validate_shacl.py                      # SHACL validation script
├── run_sparql_queries.py                  # SPARQL query executor
├── neo4j_import_labels.py                 # Neo4j import script
│
├── commands                                # Quick reference commands
├── SPARQL_CYPHER_QUERIES.md               # Query examples
├── NEO4J_SHACL_VALIDATION.md              # Neo4j SHACL guide
└── README.md                              # This file
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install rdflib pandas pyshacl
```

### 2. Generate RDF Data

```bash
python lung_cancer_etl_engine.py
```

Generates:
- `ouput/lung_cancer_instances_out.ttl` - RDF knowledge graph
- `ouput/auto_generated.cypher` - Cypher import script

### 3. Validate Data Quality

```bash
python validate_shacl.py
```

Checks:
- ✅ Data completeness
- ✅ Constraint compliance
- ✅ Relationship integrity
- ✅ Data type validation

### 4. Query with SPARQL

```bash
python run_sparql_queries.py
```

Runs example queries demonstrating:
- Patient filtering
- Treatment outcomes
- Biomarker analysis
- Stage distribution

### 5. Import to Neo4j

See `commands` file or run:

```cypher
// Initialize neosemantics
CALL n10s.graphconfig.init({
  handleVocabUris: "MAP",
  handleRDFTypes: "LABELS",
  applyNeo4jNaming: true
});

// Import data
CALL n10s.rdf.import.fetch("file:///path/to/lung_cancer_instances_out.ttl", "Turtle");
```

## 📊 What Makes This Different?

### Integrated from Folders 1 & 3

This implementation combines capabilities from:

#### From Folder 1 (sparql_neo4j):
- **SPARQL querying** alongside Cypher
- **Equivalent query examples** in both languages
- **Side-by-side comparisons** for learning

#### From Folder 3 (shacl):
- **SHACL validation** for data quality
- **Constraint validation** in Python
- **Neo4j SHACL integration** with n10s
- **Automated testing** of data integrity

### Plus New Capabilities:
- ✨ **Ontology-driven design** with formal OWL ontology
- ✨ **Automated ETL** from CSV to RDF
- ✨ **Label generation** for all entities
- ✨ **Proper rdf:type** for all nodes
- ✨ **Relationship creation** that actually works in Neo4j!

## 🏗️ Architecture

```
CSV Data → ETL Engine → RDF/TTL → Validation → Neo4j
   ↓                       ↓           ↓          ↓
Mapping              Ontology      SHACL    Neosemantics
Config               Schema        Shapes   (n10s)
                        ↓             ↓
                   (Protégé)     Validation
                    SPARQL        Reports
```

## 📝 Key Features

### 1. Ontology Schema (`lung_cancer_kg_schema.ttl`)

Defines:
- **Classes**: Patient, Tumor, Stage, Histology, Biomarker, Therapy, Drug, Outcome, Gene, Mutation, Test
- **13 Object Properties**: 
  1. diagnosedWith (Patient → Disease)
  2. hasTumor (Patient → Tumor)
  3. hasStage (Tumor/Patient → Stage)
  4. hasHistology (Tumor/Patient → Histology)
  5. underwentTest (Patient → Test)
  6. testedForBiomarker (Patient → Biomarker)
  7. hasGene (Biomarker → Gene)
  8. hasMutation (Biomarker → Mutation)
  9. receivedTherapy (Patient → Therapy)
  10. usesDrug (Therapy → Drug)
  11. hasOutcome (Patient → Outcome)
  12. recommends (Guideline → Therapy)
  13. triggers (ClinicalRule → Therapy)
- **Datatype Properties**: age, sex, smokingPackYears, patientId
- **rdfs:label** on all classes and properties for human readability

### 2. SHACL Shapes (`lung_cancer_shacl_shapes.ttl`)

Validates:
- **Patient constraints**: Must have ID, age (0-120), sex (M/F/Other)
- **Stage constraints**: Valid cancer stages (I-IV and sub-stages)
- **Therapy constraints**: Must use at least one drug
- **Relationship constraints**: Patients with therapy should have outcomes
- **Label requirements**: All entities should have rdfs:label

### 3. ETL Engine (`lung_cancer_etl_engine.py`)

Features:
- Reads CSV data based on JSON mapping configuration
- Generates RDF triples with proper types and labels
- Creates object properties for relationships
- Outputs both TTL and Cypher formats
- Automatic label generation for Neo4j visualization

### 4. SPARQL Queries (`run_sparql_queries.py`)

Examples:
- List all patients with demographics
- Filter by cancer stage
- Treatment and drug combinations
- Biomarker test analysis
- High-risk patient identification
- Similar patient matching

### 5. SHACL Validation (`validate_shacl.py`)

Validates:
- **Violations** (must fix): Missing required fields, invalid ranges
- **Warnings** (should fix): Missing optional fields, best practices
- **Info** (optional): Recommendations for data quality

## 📚 Documentation

- **`commands`**: Quick reference for all operations
- **`SPARQL_CYPHER_QUERIES.md`**: Side-by-side query examples
- **`NEO4J_SHACL_VALIDATION.md`**: Neo4j SHACL validation guide

## 🔍 Example Queries

### SPARQL Query
```sparql
PREFIX : <http://lungkg.org/ontology#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?patientLabel ?drugLabel
WHERE {
  ?patient a :Patient ;
           rdfs:label ?patientLabel ;
           :receivedTherapy ?therapy .
  ?therapy :usesDrug ?drug .
  ?drug rdfs:label ?drugLabel .
}
```

### Equivalent Cypher Query
```cypher
MATCH (p:ns0__Patient)-[:ns0__receivedTherapy]->(t:ns0__Therapy)-[:ns0__usesDrug]->(d:ns0__Drug)
RETURN p.rdfs__label AS Patient,
       d.rdfs__label AS Drug
```

## ✅ Data Quality Checks

### Python SHACL Validation
```bash
python validate_shacl.py
```

Output:
```
✅ VALIDATION PASSED - All constraints satisfied!

📊 Results:
  🔴 Violations: 0
  ⚠️  Warnings:   0
  ℹ️  Info:       8
```

### Neo4j SHACL Validation
```cypher
CALL n10s.validation.shacl.validate()
YIELD severity, resultMessage
RETURN severity, count(*) AS Count
```

## 🎯 Use Cases

1. **Clinical Research**: Analyze treatment outcomes by biomarker
2. **Treatment Planning**: Find patients with similar profiles
3. **Data Quality**: Ensure completeness and correctness
4. **Knowledge Discovery**: SPARQL pattern matching
5. **Graph Visualization**: Neo4j Browser with proper labels
6. **Interoperability**: Standard RDF/OWL for data exchange

## 🔧 Troubleshooting

### Relationships Not Showing in Neo4j?

**Problem**: Using `handleVocabUris: "IGNORE"`

**Solution**:
```cypher
CALL n10s.graphconfig.drop();

CALL n10s.graphconfig.init({
  handleVocabUris: "MAP",  // ✅ Must be MAP!
  handleRDFTypes: "LABELS",
  applyNeo4jNaming: true
});
```

### No Labels in Neo4j?

**Problem**: Missing `rdfs:label` in RDF

**Solution**: Already fixed! Run `python lung_cancer_etl_engine.py` - it now adds labels to all entities.

### SHACL Validation Fails?

**Problem**: Missing required fields or invalid data

**Solution**: Check `ouput/shacl_validation_report.txt` for details and fix source CSV data.

## 📖 Learn More

- **OWL Ontologies**: [W3C OWL Guide](https://www.w3.org/TR/owl2-primer/)
- **SHACL Validation**: [W3C SHACL Spec](https://www.w3.org/TR/shacl/)
- **SPARQL Queries**: [W3C SPARQL Tutorial](https://www.w3.org/TR/sparql11-query/)
- **Neosemantics**: [n10s Documentation](https://neo4j.com/labs/neosemantics/)

## 🤝 Contributing

This is an integrated solution combining:
- Ontology-driven modeling
- SPARQL querying (from folder 1)  
- SHACL validation (from folder 3)
- Python automation
- Neo4j integration

## 📄 License

Educational and research purposes.

---

**Need help?** Check the `commands` file for quick reference or the markdown docs for detailed examples!
