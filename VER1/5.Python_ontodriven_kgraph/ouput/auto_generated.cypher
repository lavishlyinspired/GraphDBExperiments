MERGE (n:Patient {id:'Patient_P001'})
SET n.label='Patient P001'
SET n.patientId='P001'
SET n.age='67'
SET n.sex='M'
SET n.smokingPackYears='45'
MERGE (o:Tumor {id:'Tumor_P001'})
SET o.label='Tumor P001'
MERGE (n)-[:HASTUMOR]->(o)
MERGE (o:Stage {id:'Stage_IV'})
SET o.label='Stage IV'
MERGE (n)-[:HASSTAGE]->(o)
MERGE (o:Histology {id:'Histology_Adenocarcinoma'})
SET o.label='Histology Adenocarcinoma'
MERGE (n)-[:HASHISTOLOGY]->(o)
MERGE (n:Patient {id:'Patient_P002'})
SET n.label='Patient P002'
SET n.patientId='P002'
SET n.age='58'
SET n.sex='F'
SET n.smokingPackYears='20'
MERGE (o:Tumor {id:'Tumor_P002'})
SET o.label='Tumor P002'
MERGE (n)-[:HASTUMOR]->(o)
MERGE (o:Stage {id:'Stage_III'})
SET o.label='Stage III'
MERGE (n)-[:HASSTAGE]->(o)
MERGE (o:Histology {id:'Histology_Squamous'})
SET o.label='Histology Squamous'
MERGE (n)-[:HASHISTOLOGY]->(o)
MERGE (n:Patient {id:'Patient_P003'})
SET n.label='Patient P003'
SET n.patientId='P003'
SET n.age='72'
SET n.sex='M'
SET n.smokingPackYears='60'
MERGE (o:Tumor {id:'Tumor_P003'})
SET o.label='Tumor P003'
MERGE (n)-[:HASTUMOR]->(o)
MERGE (o:Stage {id:'Stage_IV'})
SET o.label='Stage IV'
MERGE (n)-[:HASSTAGE]->(o)
MERGE (o:Histology {id:'Histology_Adenocarcinoma'})
SET o.label='Histology Adenocarcinoma'
MERGE (n)-[:HASHISTOLOGY]->(o)
MERGE (n:Patient {id:'Patient_P004'})
SET n.label='Patient P004'
SET n.patientId='P004'
SET n.age='49'
SET n.sex='F'
SET n.smokingPackYears='5'
MERGE (o:Tumor {id:'Tumor_P004'})
SET o.label='Tumor P004'
MERGE (n)-[:HASTUMOR]->(o)
MERGE (o:Stage {id:'Stage_II'})
SET o.label='Stage II'
MERGE (n)-[:HASSTAGE]->(o)
MERGE (o:Histology {id:'Histology_Adenocarcinoma'})
SET o.label='Histology Adenocarcinoma'
MERGE (n)-[:HASHISTOLOGY]->(o)
MERGE (n:Patient {id:'Patient_P005'})
SET n.label='Patient P005'
SET n.patientId='P005'
SET n.age='63'
SET n.sex='M'
SET n.smokingPackYears='40'
MERGE (o:Tumor {id:'Tumor_P005'})
SET o.label='Tumor P005'
MERGE (n)-[:HASTUMOR]->(o)
MERGE (o:Stage {id:'Stage_III'})
SET o.label='Stage III'
MERGE (n)-[:HASSTAGE]->(o)
MERGE (o:Histology {id:'Histology_Squamous'})
SET o.label='Histology Squamous'
MERGE (n)-[:HASHISTOLOGY]->(o)
MERGE (n:Patient {id:'Patient_P006'})
SET n.label='Patient P006'
SET n.patientId='P006'
SET n.age='55'
SET n.sex='F'
SET n.smokingPackYears='10'
MERGE (o:Tumor {id:'Tumor_P006'})
SET o.label='Tumor P006'
MERGE (n)-[:HASTUMOR]->(o)
MERGE (o:Stage {id:'Stage_I'})
SET o.label='Stage I'
MERGE (n)-[:HASSTAGE]->(o)
MERGE (o:Histology {id:'Histology_Adenocarcinoma'})
SET o.label='Histology Adenocarcinoma'
MERGE (n)-[:HASHISTOLOGY]->(o)
MERGE (o:Biomarker {id:'Biomarker_EGFR'})
SET o.label='Biomarker EGFR'
MERGE (n)-[:TESTEDFORBIOMARKER]->(o)
MERGE (o:Biomarker {id:'Biomarker_KRAS'})
SET o.label='Biomarker KRAS'
MERGE (n)-[:TESTEDFORBIOMARKER]->(o)
MERGE (o:Biomarker {id:'Biomarker_ALK'})
SET o.label='Biomarker ALK'
MERGE (n)-[:TESTEDFORBIOMARKER]->(o)
MERGE (o:Biomarker {id:'Biomarker_EGFR'})
SET o.label='Biomarker EGFR'
MERGE (n)-[:TESTEDFORBIOMARKER]->(o)
MERGE (o:Biomarker {id:'Biomarker_PD-L1'})
SET o.label='Biomarker PD-L1'
MERGE (n)-[:TESTEDFORBIOMARKER]->(o)
MERGE (o:Biomarker {id:'Biomarker_BRAF'})
SET o.label='Biomarker BRAF'
MERGE (n)-[:TESTEDFORBIOMARKER]->(o)
MERGE (o:Therapy {id:'Therapy_P001_Osimertinib'})
SET o.label='Therapy P001 Osimertinib'
MERGE (n)-[:RECEIVEDTHERAPY]->(o)
MERGE (o:Drug {id:'Drug_Osimertinib'})
SET o.label='Drug Osimertinib'
MERGE (n)-[:USESDRUG]->(o)
MERGE (o:Outcome {id:'Outcome_P001_Partial_Response'})
SET o.label='Outcome P001 Partial Response'
MERGE (n)-[:HASOUTCOME]->(o)
MERGE (o:Therapy {id:'Therapy_P002_Cisplatin'})
SET o.label='Therapy P002 Cisplatin'
MERGE (n)-[:RECEIVEDTHERAPY]->(o)
MERGE (o:Drug {id:'Drug_Cisplatin'})
SET o.label='Drug Cisplatin'
MERGE (n)-[:USESDRUG]->(o)
MERGE (o:Outcome {id:'Outcome_P002_Stable'})
SET o.label='Outcome P002 Stable'
MERGE (n)-[:HASOUTCOME]->(o)
MERGE (o:Therapy {id:'Therapy_P003_Alectinib'})
SET o.label='Therapy P003 Alectinib'
MERGE (n)-[:RECEIVEDTHERAPY]->(o)
MERGE (o:Drug {id:'Drug_Alectinib'})
SET o.label='Drug Alectinib'
MERGE (n)-[:USESDRUG]->(o)
MERGE (o:Outcome {id:'Outcome_P003_Complete_Response'})
SET o.label='Outcome P003 Complete Response'
MERGE (n)-[:HASOUTCOME]->(o)
MERGE (o:Therapy {id:'Therapy_P004_Erlotinib'})
SET o.label='Therapy P004 Erlotinib'
MERGE (n)-[:RECEIVEDTHERAPY]->(o)
MERGE (o:Drug {id:'Drug_Erlotinib'})
SET o.label='Drug Erlotinib'
MERGE (n)-[:USESDRUG]->(o)
MERGE (o:Outcome {id:'Outcome_P004_Partial_Response'})
SET o.label='Outcome P004 Partial Response'
MERGE (n)-[:HASOUTCOME]->(o)
MERGE (o:Therapy {id:'Therapy_P005_Pembrolizumab'})
SET o.label='Therapy P005 Pembrolizumab'
MERGE (n)-[:RECEIVEDTHERAPY]->(o)
MERGE (o:Drug {id:'Drug_Pembrolizumab'})
SET o.label='Drug Pembrolizumab'
MERGE (n)-[:USESDRUG]->(o)
MERGE (o:Outcome {id:'Outcome_P005_Partial_Response'})
SET o.label='Outcome P005 Partial Response'
MERGE (n)-[:HASOUTCOME]->(o)
MERGE (o:Therapy {id:'Therapy_P006_nan'})
SET o.label='Therapy P006 nan'
MERGE (n)-[:RECEIVEDTHERAPY]->(o)
MERGE (o:Drug {id:'Drug_nan'})
SET o.label='Drug nan'
MERGE (n)-[:USESDRUG]->(o)
MERGE (o:Outcome {id:'Outcome_P006_Disease_Free'})
SET o.label='Outcome P006 Disease Free'
MERGE (n)-[:HASOUTCOME]->(o)