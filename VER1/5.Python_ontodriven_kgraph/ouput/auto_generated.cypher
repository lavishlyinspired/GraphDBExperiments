MERGE (n:Patient {id:'Patient_P001'})
SET n.patientId='P001'
SET n.age='67'
SET n.sex='M'
SET n.smokingPackYears='45'
MERGE (o:Tumor {id:'Tumor_P001'})
MERGE (n)-[:HASTUMOR]->(o)
MERGE (o:Stage {id:'Stage_IV'})
MERGE (n)-[:HASSTAGE]->(o)
MERGE (o:Histology {id:'Histology_Adenocarcinoma'})
MERGE (n)-[:HASHISTOLOGY]->(o)
MERGE (n:Patient {id:'Patient_P002'})
SET n.patientId='P002'
SET n.age='58'
SET n.sex='F'
SET n.smokingPackYears='20'
MERGE (o:Tumor {id:'Tumor_P002'})
MERGE (n)-[:HASTUMOR]->(o)
MERGE (o:Stage {id:'Stage_III'})
MERGE (n)-[:HASSTAGE]->(o)
MERGE (o:Histology {id:'Histology_Squamous'})
MERGE (n)-[:HASHISTOLOGY]->(o)
MERGE (n:Patient {id:'Patient_P003'})
SET n.patientId='P003'
SET n.age='72'
SET n.sex='M'
SET n.smokingPackYears='60'
MERGE (o:Tumor {id:'Tumor_P003'})
MERGE (n)-[:HASTUMOR]->(o)
MERGE (o:Stage {id:'Stage_IV'})
MERGE (n)-[:HASSTAGE]->(o)
MERGE (o:Histology {id:'Histology_Adenocarcinoma'})
MERGE (n)-[:HASHISTOLOGY]->(o)
MERGE (n:Patient {id:'Patient_P004'})
SET n.patientId='P004'
SET n.age='49'
SET n.sex='F'
SET n.smokingPackYears='5'
MERGE (o:Tumor {id:'Tumor_P004'})
MERGE (n)-[:HASTUMOR]->(o)
MERGE (o:Stage {id:'Stage_II'})
MERGE (n)-[:HASSTAGE]->(o)
MERGE (o:Histology {id:'Histology_Adenocarcinoma'})
MERGE (n)-[:HASHISTOLOGY]->(o)
MERGE (n:Patient {id:'Patient_P005'})
SET n.patientId='P005'
SET n.age='63'
SET n.sex='M'
SET n.smokingPackYears='40'
MERGE (o:Tumor {id:'Tumor_P005'})
MERGE (n)-[:HASTUMOR]->(o)
MERGE (o:Stage {id:'Stage_III'})
MERGE (n)-[:HASSTAGE]->(o)
MERGE (o:Histology {id:'Histology_Squamous'})
MERGE (n)-[:HASHISTOLOGY]->(o)
MERGE (n:Patient {id:'Patient_P006'})
SET n.patientId='P006'
SET n.age='55'
SET n.sex='F'
SET n.smokingPackYears='10'
MERGE (o:Tumor {id:'Tumor_P006'})
MERGE (n)-[:HASTUMOR]->(o)
MERGE (o:Stage {id:'Stage_I'})
MERGE (n)-[:HASSTAGE]->(o)
MERGE (o:Histology {id:'Histology_Adenocarcinoma'})
MERGE (n)-[:HASHISTOLOGY]->(o)
MERGE (o:Biomarker {id:'Biomarker_EGFR'})
MERGE (n)-[:TESTEDFORBIOMARKER]->(o)
MERGE (o:Biomarker {id:'Biomarker_KRAS'})
MERGE (n)-[:TESTEDFORBIOMARKER]->(o)
MERGE (o:Biomarker {id:'Biomarker_ALK'})
MERGE (n)-[:TESTEDFORBIOMARKER]->(o)
MERGE (o:Biomarker {id:'Biomarker_EGFR'})
MERGE (n)-[:TESTEDFORBIOMARKER]->(o)
MERGE (o:Biomarker {id:'Biomarker_PD-L1'})
MERGE (n)-[:TESTEDFORBIOMARKER]->(o)
MERGE (o:Biomarker {id:'Biomarker_BRAF'})
MERGE (n)-[:TESTEDFORBIOMARKER]->(o)
MERGE (o:Therapy {id:'Therapy_P001_Osimertinib'})
MERGE (n)-[:RECEIVEDTHERAPY]->(o)
MERGE (o:Drug {id:'Drug_Osimertinib'})
MERGE (n)-[:USESDRUG]->(o)
MERGE (o:Outcome {id:'Outcome_P001_Partial_Response'})
MERGE (n)-[:HASOUTCOME]->(o)
MERGE (o:Therapy {id:'Therapy_P002_Cisplatin'})
MERGE (n)-[:RECEIVEDTHERAPY]->(o)
MERGE (o:Drug {id:'Drug_Cisplatin'})
MERGE (n)-[:USESDRUG]->(o)
MERGE (o:Outcome {id:'Outcome_P002_Stable'})
MERGE (n)-[:HASOUTCOME]->(o)
MERGE (o:Therapy {id:'Therapy_P003_Alectinib'})
MERGE (n)-[:RECEIVEDTHERAPY]->(o)
MERGE (o:Drug {id:'Drug_Alectinib'})
MERGE (n)-[:USESDRUG]->(o)
MERGE (o:Outcome {id:'Outcome_P003_Complete_Response'})
MERGE (n)-[:HASOUTCOME]->(o)
MERGE (o:Therapy {id:'Therapy_P004_Erlotinib'})
MERGE (n)-[:RECEIVEDTHERAPY]->(o)
MERGE (o:Drug {id:'Drug_Erlotinib'})
MERGE (n)-[:USESDRUG]->(o)
MERGE (o:Outcome {id:'Outcome_P004_Partial_Response'})
MERGE (n)-[:HASOUTCOME]->(o)
MERGE (o:Therapy {id:'Therapy_P005_Pembrolizumab'})
MERGE (n)-[:RECEIVEDTHERAPY]->(o)
MERGE (o:Drug {id:'Drug_Pembrolizumab'})
MERGE (n)-[:USESDRUG]->(o)
MERGE (o:Outcome {id:'Outcome_P005_Partial_Response'})
MERGE (n)-[:HASOUTCOME]->(o)
MERGE (o:Therapy {id:'Therapy_P006_nan'})
MERGE (n)-[:RECEIVEDTHERAPY]->(o)
MERGE (o:Drug {id:'Drug_nan'})
MERGE (n)-[:USESDRUG]->(o)
MERGE (o:Outcome {id:'Outcome_P006_Disease_Free'})
MERGE (n)-[:HASOUTCOME]->(o)