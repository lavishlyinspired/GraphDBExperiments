"""
Neo4j Import Script with Neosemantics (n10s)
This script imports the lung cancer knowledge graph into Neo4j with proper label handling
"""
from neo4j import GraphDatabase
from pathlib import Path

# Neo4j connection details
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "your_password_here"  # UPDATE THIS

SCRIPT_DIR = Path(__file__).parent

class Neo4jImporter:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
    
    def close(self):
        self.driver.close()
    
    def init_n10s(self):
        """Initialize neosemantics with proper configuration"""
        with self.driver.session() as session:
            # Create constraint
            session.run("""
                CREATE CONSTRAINT n10s_unique_uri IF NOT EXISTS
                FOR (r:Resource) REQUIRE r.uri IS UNIQUE
            """)
            print("✓ Created uniqueness constraint")
            
            # Initialize n10s configuration
            result = session.run("""
                CALL n10s.graphconfig.init({
                    handleVocabUris: "MAP",
                    handleMultival: "ARRAY",
                    keepLangTag: true,
                    handleRDFTypes: "LABELS",
                    multivalPropList: [],
                    keepCustomDataTypes: false,
                    customDataTypePNames: [],
                    applyNeo4jNaming: true
                })
            """)
            print("✓ Initialized n10s configuration")
            print(f"  Config: {result.single()}")
    
    def import_rdf_file(self, file_path, description="RDF"):
        """Import an RDF/Turtle file into Neo4j"""
        with self.driver.session() as session:
            # Convert Windows path to file:// URI format
            file_uri = file_path.as_uri()
            
            print(f"\nImporting {description} from: {file_uri}")
            
            result = session.run("""
                CALL n10s.rdf.import.fetch(
                    $fileUri,
                    "Turtle",
                    {
                        headerParams: {},
                        commitSize: 500,
                        languageFilter: "en"
                    }
                )
            """, fileUri=file_uri)
            
            summary = result.single()
            print(f"✓ {description} imported successfully")
            print(f"  Triples: {summary}")
    
    def verify_labels(self):
        """Verify that labels are properly imported"""
        with self.driver.session() as session:
            # Check node labels
            result = session.run("""
                MATCH (n)
                RETURN DISTINCT labels(n) AS NodeLabels, count(n) AS Count
                ORDER BY Count DESC
            """)
            
            print("\n=== Node Labels Distribution ===")
            for record in result:
                print(f"  {record['NodeLabels']}: {record['Count']} nodes")
            
            # Check rdfs:label properties
            result = session.run("""
                MATCH (n)
                WHERE n.rdfs__label IS NOT NULL
                RETURN n.rdfs__label AS Label, labels(n) AS Type
                LIMIT 10
            """)
            
            print("\n=== Sample Labels (rdfs:label) ===")
            for record in result:
                print(f"  {record['Label']} ({record['Type']})")
    
    def show_sample_data(self):
        """Display sample patient data"""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (p:ns0__Patient)
                RETURN p.rdfs__label AS PatientLabel, 
                       p.ns0__age AS Age,
                       p.ns0__sex AS Sex
                LIMIT 5
            """)
            
            print("\n=== Sample Patient Data ===")
            for record in result:
                print(f"  {record['PatientLabel']} - Age: {record['Age']}, Sex: {record['Sex']}")


def main():
    print("=== Neo4j Knowledge Graph Import ===\n")
    
    # File paths
    schema_file = SCRIPT_DIR / "ttl_shacl_data" / "lung_cancer_kg_schema.ttl"
    instances_file = SCRIPT_DIR / "ouput" / "lung_cancer_instances_out.ttl"
    
    # Verify files exist
    if not schema_file.exists():
        print(f"ERROR: Schema file not found: {schema_file}")
        return
    
    if not instances_file.exists():
        print(f"ERROR: Instances file not found: {instances_file}")
        return
    
    # Import into Neo4j
    importer = Neo4jImporter(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
    
    try:
        # Initialize n10s
        importer.init_n10s()
        
        # Import schema/ontology
        importer.import_rdf_file(schema_file, "Ontology Schema")
        
        # Import instance data
        importer.import_rdf_file(instances_file, "Instance Data")
        
        # Verify results
        importer.verify_labels()
        importer.show_sample_data()
        
        print("\n✓ Import completed successfully!")
        print("\nNote: In Neo4j Browser, nodes will show their rdfs:label property")
        print("      You can customize display by clicking node types in the sidebar")
        
    except Exception as e:
        print(f"\n✗ Error during import: {e}")
        print("\nTroubleshooting:")
        print("  1. Ensure Neo4j is running")
        print("  2. Verify n10s plugin is installed")
        print("  3. Check NEO4J_PASSWORD is correct")
        print("  4. Ensure file paths are accessible to Neo4j")
        
    finally:
        importer.close()


if __name__ == "__main__":
    main()
