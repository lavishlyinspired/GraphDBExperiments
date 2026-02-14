"""
SPARQL Query Executor for Lung Cancer Knowledge Graph

This script allows you to run SPARQL queries against the lung cancer RDF data.
"""

from rdflib import Graph, Namespace
from pathlib import Path
import sys

# Get the directory where this script is located
SCRIPT_DIR = Path(__file__).parent

# File paths  
ONTOLOGY_FILE = SCRIPT_DIR / "ttl_shacl_data" / "lung_cancer_kg_schema.ttl"
DATA_FILE = SCRIPT_DIR / "ouput" / "lung_cancer_instances_out.ttl"

# Define namespaces
ONT = Namespace("http://lungkg.org/ontology#")
RES = Namespace("http://lungkg.org/resource/")


def load_knowledge_graph():
    """Load the knowledge graph from files"""
    print("Loading knowledge graph...")
    
    g = Graph()
    g.bind("ont", ONT)
    g.bind("res", RES)
    
    # Load ontology
    if ONTOLOGY_FILE.exists():
        print(f"  Loading ontology: {ONTOLOGY_FILE}")
        g.parse(ONTOLOGY_FILE)
    
    # Load instance data
    if DATA_FILE.exists():
        print(f"  Loading instances: {DATA_FILE}")
        g.parse(DATA_FILE)
    else:
        print(f"\n❌ Error: Instance data file not found: {DATA_FILE}")
        print("\n💡 Run this first:")
        print(f"   python {SCRIPT_DIR / 'lung_cancer_etl_engine.py'}")
        sys.exit(1)
    
    print(f"  ✓ Loaded {len(g)} triples\n")
    return g


def run_query(g, query_name, query_string):
    """Execute a SPARQL query and display results"""
    print(f"\n{'='*70}")
    print(f"Query: {query_name}")
    print(f"{'='*70}")
    
    try:
        results = g.query(query_string)
        
        # Print results
        if results:
            row_count = 0
            for row in results:
                row_count += 1
                print(f"{row_count}. {' | '.join(str(val) for val in row)}")
            
            if row_count == 0:
                print("  (No results)")
            else:
                print(f"\n  Total results: {row_count}")
        else:
            print("  (No results)")
    
    except Exception as e:
        print(f"\n❌ Query error: {e}")


def main():
    print("\n" + "="*70)
    print("LUNG CANCER KNOWLEDGE GRAPH - SPARQL QUERY EXECUTOR")
    print("="*70 + "\n")
    
    # Load graph
    g = load_knowledge_graph()
    
    # Define queries
    queries = {
        "Q1: List All Patients": """
            PREFIX : <http://lungkg.org/ontology#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            
            SELECT ?label ?age ?sex
            WHERE {
              ?patient a :Patient ;
                       rdfs:label ?label ;
                       :age ?age ;
                       :sex ?sex .
            }
            ORDER BY ?age
        """,
        
        "Q2: Stage IV Patients": """
            PREFIX : <http://lungkg.org/ontology#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            
            SELECT ?patientLabel ?age
            WHERE {
              ?patient a :Patient ;
                       rdfs:label ?patientLabel ;
                       :age ?age ;
                       :hasStage ?stage .
              
              ?stage :name "IV" .
            }
            ORDER BY ?age
        """,
        
        "Q3: Patients with Treatments & Drugs": """
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
            ORDER BY ?patientLabel
        """,
        
        "Q4: Biomarker Test Summary": """
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
        """,
        
        "Q5: Treatment Outcomes": """
            PREFIX : <http://lungkg.org/ontology#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            
            SELECT ?patientLabel ?drugLabel ?outcomeLabel
            WHERE {
              ?patient a :Patient ;
                       rdfs:label ?patientLabel ;
                       :receivedTherapy ?therapy ;
                       :hasOutcome ?outcome .
              
              ?therapy :usesDrug ?drug .
              ?drug rdfs:label ?drugLabel .
              ?outcome rdfs:label ?outcomeLabel .
            }
            ORDER BY ?patientLabel
        """,
        
        "Q6: Patients by Stage (Distribution)": """
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
        """,
        
        "Q7: EGFR+ Patients": """
            PREFIX : <http://lungkg.org/ontology#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            
            SELECT ?patientLabel ?age ?drugLabel
            WHERE {
              ?patient a :Patient ;
                       rdfs:label ?patientLabel ;
                       :age ?age ;
                       :testedForBiomarker ?biomarker ;
                       :receivedTherapy ?therapy .
              
              ?biomarker rdfs:label ?biomarkerLabel .
              FILTER(CONTAINS(?biomarkerLabel, "EGFR"))
              
              ?therapy :usesDrug ?drug .
              ?drug rdfs:label ?drugLabel .
            }
            ORDER BY ?age
        """,
        
        "Q8: High-Risk Patients (Stage IV + Heavy Smoking)": """
            PREFIX : <http://lungkg.org/ontology#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            
            SELECT ?patientLabel ?age ?smokingPackYears
            WHERE {
              ?patient a :Patient ;
                       rdfs:label ?patientLabel ;
                       :age ?age ;
                       :smokingPackYears ?smokingPackYears ;
                       :hasStage ?stage .
              
              ?stage :name "IV" .
              
              FILTER(?smokingPackYears > 20)
            }
            ORDER BY DESC(?smokingPackYears)
        """,
        
        "Q9: Histology Distribution": """
            PREFIX : <http://lungkg.org/ontology#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            
            SELECT ?histologyLabel (COUNT(?patient) AS ?patientCount)
            WHERE {
              ?patient a :Patient ;
                       :hasHistology ?histology .
              
              ?histology rdfs:label ?histologyLabel .
            }
            GROUP BY ?histologyLabel
            ORDER BY DESC(?patientCount)
        """,
    }
    
    # Run all queries
    for query_name, query_string in queries.items():
        run_query(g, query_name, query_string)
    
    print("\n" + "="*70)
    print("✅ All queries completed!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
