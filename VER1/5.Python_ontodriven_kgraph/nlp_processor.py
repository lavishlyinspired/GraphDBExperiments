"""
NLP Processing Module for Lung Cancer Knowledge Graph
Extracts entities from biomedical text and links to ontology concepts
"""

import re
from typing import List, Dict, Tuple, Optional
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS


class EntityExtractor:
    """Extract medical entities from text using pattern matching and NLP"""
    
    def __init__(self, ontology_graph: Graph, ont_namespace: Namespace, res_namespace: Namespace):
        self.g = ontology_graph
        self.ONT = ont_namespace
        self.RES = res_namespace
        self.concept_patterns = self._build_concept_patterns()
    
    def _build_concept_patterns(self) -> Dict[str, List[str]]:
        """Build regex patterns for ontology concepts"""
        return {
            'Histology': [
                r'\b(adenocarcinoma|squamous cell carcinoma|small cell lung cancer|SCLC|NSCLC|'
                r'non-small cell lung cancer|large cell carcinoma|neuroendocrine)\b',
            ],
            'Stage': [
                r'\b(stage\s+[I1234]{1,3}[AB]?|T[1-4]N[0-3]M[01])\b',
            ],
            'Biomarker': [
                r'\b(EGFR|ALK|ROS1|BRAF|KRAS|MET|RET|NTRK|PD-L1|HER2|PIK3CA)\b',
            ],
            'Mutation': [
                r'\b(L858R|Ex19del|T790M|G12C|V600E|EML4-ALK|exon\s+\d+)\b',
            ],
            'Drug': [
                r'\b(osimertinib|erlotinib|gefitinib|afatinib|alectinib|crizotinib|'
                r'pembrolizumab|nivolumab|atezolizumab|cisplatin|carboplatin|'
                r'pemetrexed|docetaxel|paclitaxel|bevacizumab)\b',
            ],
            'Therapy': [
                r'\b(chemotherapy|immunotherapy|targeted therapy|radiation|surgery|'
                r'chemoradiation|stereotactic radiosurgery|SBRT|lobectomy|'
                r'pneumonectomy|VATS|thoracoscopic)\b',
            ],
            'Test': [
                r'\b(CT scan|PET scan|PET-CT|MRI|biopsy|genomic test|molecular testing|'
                r'next-generation sequencing|NGS|liquid biopsy)\b',
            ],
            'Outcome': [
                r'\b(complete response|partial response|stable disease|progressive disease|'
                r'CR|PR|SD|PD|progression-free survival|PFS|overall survival|OS|'
                r'recurrence|metastasis|remission)\b',
            ]
        }
    
    def extract_entities(self, text: str) -> Dict[str, List[Tuple[str, str]]]:
        """
        Extract entities from text using pattern matching
        
        Returns:
            Dict mapping concept type to list of (entity_text, canonical_name) tuples
        """
        text_lower = text.lower()
        entities = {}
        
        for concept_type, patterns in self.concept_patterns.items():
            matches = []
            for pattern in patterns:
                for match in re.finditer(pattern, text_lower, re.IGNORECASE):
                    entity_text = match.group(0)
                    # Canonicalize the entity name
                    canonical = self._canonicalize_entity(entity_text, concept_type)
                    if canonical:
                        matches.append((entity_text, canonical))
            
            if matches:
                # Remove duplicates
                entities[concept_type] = list(set(matches))
        
        return entities
    
    def _canonicalize_entity(self, entity_text: str, concept_type: str) -> Optional[str]:
        """Convert entity text to canonical form for URI creation"""
        clean = entity_text.strip().replace(' ', '_')
        
        # Uppercase for certain types
        if concept_type in ['Biomarker', 'Mutation']:
            return clean.upper()
        
        # Proper case for drugs and therapies
        if concept_type in ['Drug', 'Therapy']:
            return clean.title()
        
        # Stage normalization
        if concept_type == 'Stage':
            stage_match = re.search(r'stage\s+([I1234]{1,3}[AB]?)', entity_text, re.IGNORECASE)
            if stage_match:
                return stage_match.group(1).upper()
        
        return clean.title()
    
    def create_entity_triples(self, article_uri: URIRef, entities: Dict[str, List[Tuple[str, str]]]) -> List[Tuple]:
        """
        Create RDF triples linking article to extracted entities
        
        Returns:
            List of (subject, predicate, object) triples
        """
        triples = []
        
        for concept_type, entity_list in entities.items():
            for entity_text, canonical_name in entity_list:
                # Create URI for the entity
                entity_uri = self.RES[f"{concept_type}_{canonical_name}"]
                
                # Add type assertion
                triples.append((entity_uri, RDF.type, self.ONT[concept_type]))
                
                # Add label
                triples.append((entity_uri, RDFS.label, Literal(f"{concept_type} {canonical_name}")))
                
                # Link article to entity
                triples.append((article_uri, self.ONT['refersTo'], entity_uri))
        
        return triples
    
    def extract_patient_mentions(self, text: str) -> List[str]:
        """Extract patient age mentions from text"""
        age_pattern = r'(\d{2,3})[-\s]?year[-\s]?old'
        matches = re.findall(age_pattern, text, re.IGNORECASE)
        return [int(age) for age in matches if 0 < int(age) < 120]
    
    def calculate_salience_scores(self, entities: Dict[str, List[Tuple[str, str]]]) -> Dict[str, float]:
        """
        Calculate importance scores for entities
        Simple frequency-based scoring
        """
        scores = {}
        total_entities = sum(len(ents) for ents in entities.values())
        
        for concept_type, entity_list in entities.items():
            for entity_text, canonical_name in entity_list:
                # Biomarkers and drugs are often more salient
                base_score = 0.8 if concept_type in ['Biomarker', 'Drug'] else 0.5
                scores[canonical_name] = base_score
        
        return scores


class GCPNLPIntegration:
    """
    Optional GCP NLP API integration
    Requires google-cloud-language package and API key
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.client = None
        
        if api_key:
            try:
                from google.cloud import language_v1
                self.client = language_v1.LanguageServiceClient()
            except ImportError:
                print("⚠️  google-cloud-language not installed. Using deterministic extraction only.")
    
    def extract_entities_nlp(self, text: str) -> List[Dict]:
        """
        Extract entities using GCP NLP API
        
        Returns:
            List of entity dicts with {name, type, salience, mentions}
        """
        if not self.client:
            return []
        
        from google.cloud import language_v1
        
        document = language_v1.Document(
            content=text,
            type_=language_v1.Document.Type.PLAIN_TEXT
        )
        
        response = self.client.analyze_entities(
            request={'document': document}
        )
        
        entities = []
        for entity in response.entities:
            entities.append({
                'name': entity.name,
                'type': language_v1.Entity.Type(entity.type_).name,
                'salience': entity.salience,
                'mentions': [mention.text.content for mention in entity.mentions]
            })
        
        return entities


def process_article_text(article_body: str, ontology_graph: Graph, 
                        ont_ns: Namespace, res_ns: Namespace,
                        use_gcp: bool = False, api_key: Optional[str] = None) -> Dict:
    """
    Main function to process article text and extract entities
    
    Args:
        article_body: Text content of the article
        ontology_graph: RDF graph with ontology
        ont_ns: Ontology namespace
        res_ns: Resource namespace
        use_gcp: Whether to use GCP NLP API
        api_key: GCP API key (if use_gcp=True)
    
    Returns:
        Dict with extracted entities and metadata
    """
    extractor = EntityExtractor(ontology_graph, ont_ns, res_ns)
    
    # Deterministic extraction
    entities = extractor.extract_entities(article_body)
    patient_ages = extractor.extract_patient_mentions(article_body)
    
    result = {
        'entities': entities,
        'patient_ages': patient_ages,
        'entity_count': sum(len(ents) for ents in entities.values()),
        'nlp_used': False
    }
    
    # Optional GCP NLP
    if use_gcp and api_key:
        gcp = GCPNLPIntegration(api_key)
        nlp_entities = gcp.extract_entities_nlp(article_body)
        result['nlp_entities'] = nlp_entities
        result['nlp_used'] = True
    
    return result
