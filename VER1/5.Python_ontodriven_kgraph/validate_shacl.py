"""
SHACL Validation for Lung Cancer Knowledge Graph

This script validates the lung cancer RDF data against SHACL shapes to ensure:
- Data quality and completeness
- Constraint compliance
- Relationship integrity
"""

from pyshacl import validate
from rdflib import Graph
from pathlib import Path
import sys

# Get the directory where this script is located
SCRIPT_DIR = Path(__file__).parent.parent

# File paths
ONTOLOGY_FILE = SCRIPT_DIR / "ttl_shacl_data" / "lung_cancer_kg_schema.ttl"
DATA_FILE = SCRIPT_DIR / "ouput" / "lung_cancer_instances_out.ttl"
SHACL_FILE = SCRIPT_DIR / "ttl_shacl_data" / "lung_cancer_shacl_shapes.ttl"
REPORT_FILE = SCRIPT_DIR / "ouput" / "shacl_validation_report.txt"


def load_graph(file_path, description="Graph"):
    """Load an RDF graph from file"""
    print(f"Loading {description} from: {file_path}")
    try:
        g = Graph()
        g.parse(file_path)
        print(f"  ✓ Loaded {len(g)} triples")
        return g
    except Exception as e:
        print(f"  ✗ Error loading {description}: {e}")
        sys.exit(1)


def validate_data(data_graph, shapes_graph, ontology_graph=None):
    """Validate data graph against SHACL shapes"""
    print("\n" + "="*60)
    print("VALIDATING DATA AGAINST SHACL CONSTRAINTS")
    print("="*60)
    
    try:
        # Perform validation with RDFS inference
        conforms, results_graph, results_text = validate(
            data_graph,
            shacl_graph=shapes_graph,
            ont_graph=ontology_graph,
            inference='rdfs',  # Use RDFS inference for class hierarchies
            abort_on_first=False,  # Get all violations
            meta_shacl=False,
            advanced=True,  # Enable SPARQL-based constraints
            js=False
        )
        
        return conforms, results_graph, results_text
    
    except Exception as e:
        print(f"\n✗ Validation error: {e}")
        sys.exit(1)


def parse_validation_results(results_text):
    """Parse and categorize validation results"""
    violations = []
    warnings = []
    info = []
    
    if not results_text or "Validation Report" not in results_text:
        return violations, warnings, info
    
    # Split into individual results
    lines = results_text.split('\n')
    current_result = []
    
    for line in lines:
        if line.startswith('Constraint Violation') or line.startswith('Validation Result'):
            if current_result:
                result_text = '\n'.join(current_result)
                
                if 'Severity: sh:Violation' in result_text:
                    violations.append(result_text)
                elif 'Severity: sh:Warning' in result_text:
                    warnings.append(result_text)
                elif 'Severity: sh:Info' in result_text:
                    info.append(result_text)
                
                current_result = []
        
        current_result.append(line)
    
    # Don't forget the last one
    if current_result:
        result_text = '\n'.join(current_result)
        if 'Severity: sh:Violation' in result_text:
            violations.append(result_text)
        elif 'Severity: sh:Warning' in result_text:
            warnings.append(result_text)
        elif 'Severity: sh:Info' in result_text:
            info.append(result_text)
    
    return violations, warnings, info


def print_summary(conforms, violations, warnings, info):
    """Print validation summary"""
    print("\n" + "="*60)
    print("VALIDATION SUMMARY")
    print("="*60)
    
    if conforms:
        print("✅ VALIDATION PASSED - All constraints satisfied!")
    else:
        print("❌ VALIDATION FAILED - Constraint violations detected")
    
    print(f"\n📊 Results:")
    print(f"  🔴 Violations: {len(violations)}")
    print(f"  ⚠️  Warnings:   {len(warnings)}")
    print(f"  ℹ️  Info:       {len(info)}")
    
    if violations:
        print(f"\n{'='*60}")
        print("🔴 VIOLATIONS (Must Fix)")
        print(f"{'='*60}")
        for i, violation in enumerate(violations, 1):
            print(f"\n--- Violation {i} ---")
            # Extract key information
            for line in violation.split('\n'):
                if any(keyword in line for keyword in ['Message', 'Focus Node', 'Result Path', 'Value']):
                    print(f"  {line.strip()}")
    
    if warnings:
        print(f"\n{'='*60}")
        print("⚠️  WARNINGS (Should Fix)")
        print(f"{'='*60}")
        for i, warning in enumerate(warnings, 1):
            print(f"\n--- Warning {i} ---")
            for line in warning.split('\n'):
                if any(keyword in line for keyword in ['Message', 'Focus Node', 'Result Path']):
                    print(f"  {line.strip()}")
    
    if info:
        print(f"\n{'='*60}")
        print("ℹ️  INFORMATIONAL (Optional)")
        print(f"{'='*60}")
        print(f"  {len(info)} informational messages")


def save_report(conforms, results_text, violations, warnings, info):
    """Save validation report to file"""
    try:
        with open(REPORT_FILE, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("LUNG CANCER KNOWLEDGE GRAPH - SHACL VALIDATION REPORT\n")
            f.write("="*80 + "\n\n")
            
            f.write(f"Overall Result: {'PASS ✅' if conforms else 'FAIL ❌'}\n\n")
            f.write(f"Violations: {len(violations)}\n")
            f.write(f"Warnings: {len(warnings)}\n")
            f.write(f"Info: {len(info)}\n\n")
            
            f.write("="*80 + "\n")
            f.write("FULL VALIDATION REPORT\n")
            f.write("="*80 + "\n\n")
            f.write(results_text)
        
        print(f"\n💾 Full report saved to: {REPORT_FILE}")
    
    except Exception as e:
        print(f"\n⚠️  Could not save report: {e}")


def main():
    print("\n" + "="*60)
    print("LUNG CANCER KG - SHACL VALIDATION")
    print("="*60 + "\n")
    
    # Check if files exist
    if not DATA_FILE.exists():
        print(f"❌ Error: Data file not found: {DATA_FILE}")
        print("\n💡 Run this first:")
        print(f"   python {SCRIPT_DIR / 'lung_cancer_etl_engine.py'}")
        sys.exit(1)
    
    if not SHACL_FILE.exists():
        print(f"❌ Error: SHACL shapes file not found: {SHACL_FILE}")
        sys.exit(1)
    
    # Load graphs
    data_graph = load_graph(DATA_FILE, "Instance Data")
    shapes_graph = load_graph(SHACL_FILE, "SHACL Shapes")
    ontology_graph = load_graph(ONTOLOGY_FILE, "Ontology") if ONTOLOGY_FILE.exists() else None
    
    # Validate
    conforms, results_graph, results_text = validate_data(
        data_graph, 
        shapes_graph,
        ontology_graph
    )
    
    # Parse results
    violations, warnings, info = parse_validation_results(results_text)
    
    # Print summary
    print_summary(conforms, violations, warnings, info)
    
    # Save report
    save_report(conforms, results_text, violations, warnings, info)
    
    # Exit with appropriate code
    if not conforms and violations:
        print("\n❌ Exiting with error code due to violations")
        sys.exit(1)
    else:
        print("\n✅ Validation complete!")
        sys.exit(0)


if __name__ == "__main__":
    main()
