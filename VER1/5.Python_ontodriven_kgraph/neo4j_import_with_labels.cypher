// Neo4j Import with Neosemantics (n10s) - Proper Label Configuration
// Run these commands in Neo4j Browser or Cypher Shell

// Step 1: Install n10s plugin if not already installed
// (Download from: https://github.com/neo4j-labs/neosemantics/releases)

// Step 2: Create a uniqueness constraint (recommended)
CREATE CONSTRAINT n10s_unique_uri IF NOT EXISTS
FOR (r:Resource) REQUIRE r.uri IS UNIQUE;

// Step 3: Initialize n10s with proper configuration for label display
CALL n10s.graphconfig.init({
  handleVocabUris: "MAP",
  handleMultival: "ARRAY",
  keepLangTag: true,
  handleRDFTypes: "LABELS",  // This ensures classes become Neo4j labels
  multivalPropList: [],
  keepCustomDataTypes: false,
  customDataTypePNames: [],
  applyNeo4jNaming: true      // Converts CamelCase to readable labels
});

// Step 4: Import the ontology/schema
CALL n10s.rdf.import.fetch(
  "file:///H:/akash/git/CoherencePLM/version26/experiments/GraphDBExperiments/VER1/5.Python_ontodriven_kgraph/ttl_shacl_data/lung_cancer_kg_schema.ttl",
  "Turtle",
  {
    headerParams: {},
    commitSize: 500,
    languageFilter: "en"
  }
);

// Step 5: Import the instance data
CALL n10s.rdf.import.fetch(
  "file:///H:/akash/git/CoherencePLM/version26/experiments/GraphDBExperiments/VER1/5.Python_ontodriven_kgraph/ouput/lung_cancer_instances_out.ttl",
  "Turtle",
  {
    headerParams: {},
    commitSize: 500,
    languageFilter: "en"
  }
);

// Step 6: Verify the import - Check labels are present
MATCH (n)
RETURN DISTINCT labels(n) AS NodeLabels, count(n) AS Count
ORDER BY Count DESC;

// Step 7: Check that rdfs:label properties are displayed
MATCH (n)
WHERE n.rdfs__label IS NOT NULL
RETURN n.rdfs__label AS Label, labels(n) AS Type
LIMIT 20;

// Alternative Step 3-5: If file:/// URLs don't work, use inline import
// First, serve the TTL files via HTTP or use n10s.rdf.import.inline with the actual TTL content

// Troubleshooting: If labels still don't show
// Check n10s configuration:
CALL n10s.graphconfig.show();

// Re-initialize with different settings if needed:
// CALL n10s.graphconfig.drop();
// Then run Step 3 again
