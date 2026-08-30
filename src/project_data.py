"""Evidence, readiness mappings, and Y.3172 application configuration."""

FACTORS = [
    {
        "name": "Open Data",
        "score": 2,
        "coverage": "Covered with controlled research access",
        "evidence": "ADNI shares participant data with approved researchers through the secure LONI Image and Data Archive under its data-use terms. The NeuroAPS-Net paper documents an ADNI-2DPC cohort of 1,000 subjects (500 AD / 500 CN).",
        "source_label": "ADNI | Data and Samples",
        "source_url": "https://adni.loni.usc.edu/data-samples/",
    },
    {
        "name": "Access to Research",
        "score": 3,
        "coverage": "Strong evidence",
        "evidence": "The accepted IJCNN 2026 NeuroAPS-Net paper provides the method, ablation, efficiency, and cohort evidence used by this application. Sampling Matters remains a characterized project record whose public link has not been supplied.",
        "source_label": "NeuroAPS-Net | arXiv",
        "source_url": "https://arxiv.org/abs/2604.22883",
    },
    {
        "name": "Deployment & Infrastructure",
        "score": 3,
        "coverage": "Strong evidence",
        "evidence": "Reported results are 84.85% accuracy, 1.48 ms inference, and 234.6 MB peak GPU memory on one NVIDIA RTX 3060.",
        "source_label": "Published comparison table",
        "source_url": "https://arxiv.org/abs/2604.22883",
    },
    {
        "name": "Standards",
        "score": 2,
        "coverage": "Covered in the demonstrator",
        "evidence": "The complete MRI-to-point-cloud decision-support workflow is mapped to the functional roles in ITU-T Y.3172 and to verified KSA policy sources.",
    },
    {
        "name": "Open Source",
        "score": 2,
        "coverage": "Covered in the public repository",
        "evidence": "The application source, offline retrieval logic, tests, launchers, configuration, and documentation are published at github.com/mjrjahid/NeuroAPS. Controlled imaging artifacts remain excluded.",
    },
    {
        "name": "Sandbox",
        "score": 2,
        "coverage": "Covered for local evaluation",
        "evidence": "The application provides a local research sandbox with evidence retrieval, controlled readiness checks, a reproducible test suite, and an authorized-data integration path.",
    },
]


READINESS_DIMENSIONS = [
    (
        "Data/Model Marketplace",
        "High",
        "Strong",
        "ADNI research access, reusable ADNI-2DPC records, model metrics, source files, and artifact catalogue are available in the application.",
        "Add institutional access roles and a signed model card before operational sharing.",
    ),
    (
        "Generated Content Marketplace",
        "Foundational",
        "Foundational",
        "Anatomical Priority Sampling deterministically converts each MRI into a reusable anatomical point-cloud asset. It is a derived representation, not synthetic clinical content or generative-AI output.",
        "Add a governed artifact catalogue so derived point clouds can be indexed and reused across approved studies.",
    ),
    (
        "Cross-Domain Correlation Analysis",
        "Minimal",
        "Foundational",
        "The labelled point-cloud viewer also supports anatomy and radiology education, exposing the transferable APS principle: prioritize reliable, task-relevant structures while retaining provenance.",
        "Pilot the viewer as a medical-education tool and evaluate APS in a second imaging task before claiming cross-domain performance.",
    ),
    (
        "Contextualization & Regional Impact",
        "Low",
        "Covered by KSA evidence",
        "The application connects the research to verified Eastern Province evidence, HSTP, NSDAI, Seha Virtual Hospital, and local resource constraints.",
        "Run a Saudi-cohort validation study with local clinicians.",
    ),
    (
        "Level of Integration in Workflows",
        "Medium-High",
        "Strong demonstrator",
        "MRI intake, brain extraction output, anatomical point cloud, readiness evidence, policy translation, and review workflow are connected.",
        "Integrate the final versioned model and hospital identity/audit services.",
    ),
    (
        "Human Interface",
        "Low",
        "Strong demonstrator",
        "A professional dashboard, Y.3172 explorer, synchronized MRI/point-cloud viewer, policy evidence, and cited research assistant are implemented.",
        "Complete structured usability testing with clinicians.",
    ),
    (
        "Strategy Alignment",
        "Low",
        "Covered by public strategy",
        "Application actions are linked to official NSDAI, HSTP, Seha Virtual Hospital, PDPL, and AI-ethics sources.",
        "Assign institutional owners and an approval pathway for a pilot.",
    ),
    (
        "Collaboration with AI",
        "High",
        "Strong",
        "The workflow presents model evidence to augment clinician review and retains the human decision and escalation path.",
        "Evaluate agreement, overrides, and confidence calibration in a reader study.",
    ),
    (
        "Impact of Humans in AI Integration",
        "Medium",
        "Covered by workflow",
        "The six-step evaluation scenario captures clinician quality review, anatomical inspection, escalation, final decision, and feedback.",
        "Collect local task-completion, trust, and override evidence.",
    ),
    (
        "AI & Policies",
        "Low",
        "Covered by design",
        "The policy workspace translates PDPL/data governance, AI ethics, HSTP, and NSDAI into application controls and evaluation actions.",
        "Complete formal legal, security, and clinical-governance review.",
    ),
    (
        "AI for Inclusion",
        "Not yet addressed",
        "Designed",
        "The interface uses plain language, high contrast, concise explanations, and a pathway for Arabic/English delivery.",
        "Implement bilingual content and test accessibility with representative users.",
    ),
    (
        "Granular Priorities",
        "Medium",
        "Strong",
        "Anatomical Priority Sampling emphasizes the hippocampus, ventricles, and cortical area while keeping other brain tissue visible.",
        "Validate region priorities and thresholds with local specialists.",
    ),
    (
        "Digital Infrastructure",
        "Very High",
        "Strong",
        "Measured 1.48 ms latency and 234.6 MB GPU memory on a consumer RTX 3060 support resource-conscious deployment planning.",
        "Benchmark the complete application on the target Saudi clinical workstation.",
    ),
]


BASELINE_COMPARISON = [
    ("PointNet", 83.33, 2.17, 543.00),
    ("PointCNN", 80.30, 119.56, 800.74),
    ("DGCNN", 81.82, 135.72, 6237.90),
    ("NeuroAPS-Net", 84.85, 1.48, 234.60),
]


PIPELINE = [
    ("ML Intent", "Define AD/CN decision-support purpose, inputs, constraints, and review output", "Configured", "Research use case and human-review objective"),
    ("SRC", "Provide T1 MRI, derived brain mask, anatomical point cloud, and experiment evidence", "Integrated", "10 AD1–AD10 MRI/mask/PLY sets plus characterized research records"),
    ("C", "Register the case and connect the three representations by subject", "Integrated", "Stable subject selector and local artifact registry"),
    ("PP", "Apply brain extraction, normalization, anatomical selection, and point-cloud generation", "Outputs demonstrated", "Brain-only MRI and anatomically labelled 8,192-point PLY outputs"),
    ("M", "Define the NeuroAPS-Net AD/CN probability, confidence, class-map, and version interface", "Benchmark demonstrated; runtime pending", "Published accuracy, latency, memory, ablation, and baseline comparison; live weights are not integrated"),
    ("P", "Specify quality, confidence, escalation, privacy, and clinician-review rules", "Interface implemented; enforcement pending runtime integration", "Six-step human-review workflow plus PDPL/AI-ethics control specification"),
    ("D", "Present imaging evidence, model evidence, policy evidence, and citations", "Implemented", "Dashboard, viewer, policy alignment, and cited knowledge assistant"),
    ("SINK", "Support clinician or researcher review and final human decision", "Review workflow demonstrated", "Professional decision-support interface; clinical usability study remains pending"),
    ("MLFO", "Coordinate versions, stages, review state, and future monitoring", "Interface prepared", "Visible pipeline status and deployment workbench"),
    ("Sandbox", "Evaluate de-identified cases before institutional deployment", "Implemented", "Local research sandbox, uploads, retrieval, and tests"),
    ("Underlay", "Run on a local workstation or approved institutional infrastructure", "Implemented", "Windows/macOS/Linux launchers and resource-conscious runtime"),
]


POLICY_COVERAGE = {
    "NSDAI / SDAIA": [1, 3, 2, 3, 0, 2],
    "HSTP / Vision 2030": [0, 1, 3, 2, 0, 1],
    "Seha Virtual Hospital": [0, 2, 3, 2, 0, 3],
    "PDPL / AI Ethics": [0, 0, 1, 3, 0, 2],
}


POLICY_SOURCES = [
    {
        "source": "Health Sector Transformation Program (HSTP)",
        "authority": "Saudi Vision 2030",
        "supports": "Healthcare access, quality, primary care, digital transformation, and disease prevention.",
        "application": "Positions lightweight neuroimaging decision support as a prevention-aligned research use case. Early intervention is the application's interpretation, not a quoted HSTP phrase.",
        "boundary": "No HSTP adoption, Alzheimer screening program, clinical deployment, or regulatory approval is implied.",
        "checked": "29 Aug 2026",
        "links": [
            {"label": "HSTP official program page", "url": "https://www.vision2030.gov.sa/en/explore/programs/health-sector-transformation-program"},
            {"label": "HSTP Report 2024", "url": "https://www.vision2030.gov.sa/media/h0yb5d03/health-sector-transformation-report-2024.pdf"},
        ],
    },
    {
        "source": "National Strategy for Data & AI (NSDAI)",
        "authority": "SDAIA",
        "supports": "Healthcare is a priority sector; data and AI should improve access and preventive care.",
        "application": "Connects the research workflow to national data/AI capability, governance, preventive-care, and health priorities.",
        "boundary": "Strategy alignment does not establish SDAIA endorsement, a local cohort, or production authorization.",
        "checked": "17 Aug 2026",
        "links": [
            {"label": "NSDAI official page", "url": "https://sdaia.gov.sa/en/SDAIA/SdaiaStrategies/Pages/NationalStrategyForDataAndAI.aspx"},
            {"label": "NSDAI official PDF", "url": "https://sdaia.gov.sa/en/SDAIA/SdaiaStrategies/Documents/NSDAI.pdf"},
        ],
    },
    {
        "source": "Seha Virtual Hospital & Innovation Empowerment Center",
        "authority": "Saudi Ministry of Health",
        "supports": "Remote specialist care, teleradiology, an innovation sandbox, and clinical research infrastructure.",
        "application": "Provides a plausible public evaluation pathway for a resource-efficient imaging tool through teleradiology, sandbox, and clinical research capabilities.",
        "boundary": "No Seha partnership, integration, pilot commitment, or approval is implied.",
        "checked": "29 Aug 2026",
        "links": [
            {"label": "Seha Virtual Hospital official page", "url": "https://www.moh.gov.sa/en/ministry/projects/pages/seha-virtual-hospital.aspx"},
        ],
    },
    {
        "source": "PDPL and AI Ethics",
        "authority": "SDAIA",
        "supports": "PDPL implementing regulations require documented impact assessment for sensitive health data, linked datasets, new technologies, and automated decisions; SDAIA also provides an AI Ethics Self-Assessment.",
        "application": "Requires a documented lawful basis, purpose limitation, data minimization, health-data safeguards, audit records, DPIA where Article 25 applies, and mandatory human confirmation before external use of an AI flag.",
        "boundary": "The demonstrator is not a PDPL certification or legal opinion. Consent is required only where consent is the applicable lawful basis; formal privacy, legal, security, and clinical-governance review remains pending.",
        "checked": "29 Aug 2026",
        "links": [
            {"label": "PDPL implementing regulations", "url": "https://dgp.sdaia.gov.sa/wps/portal/pdp/knowledgecenter/details/PDPL2/"},
            {"label": "AI Ethics Self-Assessment", "url": "https://dgp.sdaia.gov.sa/wps/portal/pdp/services/servicesdetails/AIEthicsAssessment/"},
        ],
    },
]


PUBLIC_DOMAIN_SOURCES = [
    {
        "tier": "Official government",
        "source": "Health Sector Transformation Program",
        "publisher": "Saudi Vision 2030",
        "supports": "Healthcare access, quality, service transformation, digital transformation, and disease prevention. Early intervention is an application-alignment interpretation, not a direct quotation.",
        "url": "https://www.vision2030.gov.sa/en/explore/programs/health-sector-transformation-program",
        "verified": "29 Aug 2026",
    },
    {
        "tier": "Official government",
        "source": "Health Sector Transformation Report 2024",
        "publisher": "Saudi Vision 2030",
        "supports": "Published implementation evidence and national digital-health achievements.",
        "url": "https://www.vision2030.gov.sa/media/h0yb5d03/health-sector-transformation-report-2024.pdf",
        "verified": "17 Aug 2026",
    },
    {
        "tier": "Official government",
        "source": "National Strategy for Data & AI",
        "publisher": "SDAIA",
        "supports": "National data/AI strategy with healthcare as a priority sector.",
        "url": "https://sdaia.gov.sa/en/SDAIA/SdaiaStrategies/Pages/NationalStrategyForDataAndAI.aspx",
        "verified": "17 Aug 2026",
    },
    {
        "tier": "Official government",
        "source": "Seha Virtual Hospital",
        "publisher": "Saudi Ministry of Health",
        "supports": "Teleradiology, remote specialty care, innovation sandbox, and clinical research infrastructure.",
        "url": "https://www.moh.gov.sa/en/ministry/projects/pages/seha-virtual-hospital.aspx",
        "verified": "29 Aug 2026",
    },
    {
        "tier": "Official government",
        "source": "Sections of MOH Statistics",
        "publisher": "Saudi Ministry of Health",
        "supports": "Official gateway for health indicators, facilities, workforce, performance, services, and preventive/therapeutic activity; the overview does not supply a single Saudi Alzheimer prevalence estimate.",
        "url": "https://www.moh.gov.sa/en/statistics/pages/dashboard.aspx",
        "verified": "29 Aug 2026",
    },
    {
        "tier": "Official government",
        "source": "National Data Governance Platform",
        "publisher": "SDAIA",
        "supports": "PDPL services, data-governance registries, impact assessment, and regulatory sandbox access.",
        "url": "https://dgp.sdaia.gov.sa/wps/portal/pdp/home",
        "verified": "29 Aug 2026",
    },
    {
        "tier": "Official government",
        "source": "AI Ethics Self-Assessment",
        "publisher": "SDAIA",
        "supports": "Structured assessment against Saudi AI ethics principles.",
        "url": "https://dgp.sdaia.gov.sa/wps/portal/pdp/services/servicesdetails/AIEthicsAssessment/",
        "verified": "29 Aug 2026",
    },
    {
        "tier": "Public background",
        "source": "NSDAI overview",
        "publisher": "Saudipedia",
        "supports": "Public overview of NSDAI components, targets, initiatives, and priority sectors.",
        "url": "https://saudipedia.com/en/national-strategy-for-data-and-ai-nsdai",
        "verified": "17 Aug 2026",
    },
    {
        "tier": "Public background",
        "source": "NSDAI regulation index",
        "publisher": "Regulations.AI",
        "supports": "Secondary plain-language index; not an official source and not legal advice.",
        "url": "https://regulations.ai/regulations/saudi-arabia-2020-10-national-strategy-data-ai",
        "verified": "17 Aug 2026",
    },
    {
        "tier": "Public research",
        "source": "Saudi AD perspectives and genetics",
        "publisher": "PubMed record · Journal of Alzheimer's Disease (2025)",
        "supports": "Saudi-specific Alzheimer’s disease context and population-representation needs.",
        "url": "https://pubmed.ncbi.nlm.nih.gov/39994993/",
        "verified": "17 Aug 2026",
    },
    {
        "tier": "Public research",
        "source": "Dementia prevalence in the Saudi National Guard Health System",
        "publisher": "PubMed record (2025)",
        "supports": "Multi-region Saudi dementia evidence; not a Dammam-specific prevalence estimate.",
        "url": "https://pubmed.ncbi.nlm.nih.gov/39962762/",
        "verified": "29 Aug 2026",
    },
    {
        "tier": "Public research",
        "source": "Eastern Province cognitive decline study",
        "publisher": "PubMed Central",
        "supports": "Dammam/Eastern Province cognitive-decline context from a public full-text study.",
        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC11114873/",
        "verified": "17 Aug 2026",
    },
    {
        "tier": "Public research",
        "source": "KFSH Dammam Alzheimer’s prediction study",
        "publisher": "PubMed Central",
        "supports": "Local clinical-ML precedent using 152 patients; the study did not use MRI.",
        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC9427223/",
        "verified": "29 Aug 2026",
    },
]


SCENARIO = [
    ("1", "Case intake", "A clinician selects a de-identified T1 MRI and confirms the scan is suitable for review."),
    ("2", "Representation", "The workflow isolates the brain and prepares the anatomically labelled point cloud."),
    ("3", "Model evidence", "After versioned runtime integration, NeuroAPS-Net will return AD/CN decision-support evidence with confidence and model context. This build shows the benchmark and interface only."),
    ("4", "Clinical review", "The clinician compares the brain MRI with hippocampal, ventricular, cortical, and other regions."),
    ("5", "Escalation", "Low-confidence, poor-quality, or discordant cases are referred for specialist review and clinical testing."),
    ("6", "Decision & feedback", "The clinician records the final decision, rationale, and feedback for monitoring and improvement."),
]


GOVERNANCE_SCENARIO = [
    ("1", "Controlled intake", "Use only an approved, de-identified research case and record purpose, lawful basis, access role, and model version before processing."),
    ("2", "Human confirmation", "Treat every AI flag as decision-support evidence. Do not disclose it to a patient, insurer, employer, or other third party before authorized clinician review."),
    ("3", "Purpose boundary", "Do not reuse inferred cognitive or health signals for advertising, unrelated profiling, or coverage decisions. Any new purpose requires separate governance and legal review."),
    ("4", "Escalation and audit", "Log blocked disclosure attempts, model/version context, reviewer action, and final outcome; escalate privacy, safety, or discordant cases to the designated governance owners."),
]


PDPL_AI_ETHICS_CONTROLS = [
    ("Purpose and lawful basis", "Define the specific research/clinical-support purpose, inform the data subject where applicable, and document the lawful basis; do not assume consent is the only possible basis.", "Design requirement"),
    ("DPIA / impact assessment", "Complete a written assessment where PDPL Article 25 applies, including sensitive health data, linked datasets, new technology, automated decisions, or serious privacy risk.", "Required before operational processing"),
    ("Health-data safeguards", "Use minimum necessary data, role-based access, approved storage/transfer controls, retention limits, and measures against unauthorized or incompatible use.", "Design requirement"),
    ("Human oversight", "Require authorized clinician confirmation before an AI flag can drive disclosure or action; document overrides, escalation, and rationale.", "Specified; enforcement pending model integration"),
    ("No unrelated profiling", "Block advertising, unrelated profiling, and insurer/employer use of inferred cognitive signals outside the approved purpose.", "Specified governance boundary"),
    ("Audit and review", "Retain processing/activity records and complete formal privacy, AI-ethics, security, legal, and clinical-governance review before a pilot.", "Pending institutional review"),
]


POINT_LABELS = {
    1: "Hippocampus",
    3: "Ventricles",
    5: "Cortical area",
    7: "Other brain tissue",
}


SCORE_LABEL = {0: "Not addressed", 1: "Partial", 2: "Covered", 3: "Strong evidence"}
SCORE_COLOR = {0: "#B4233A", 1: "#C77B17", 2: "#2E6C7C", 3: "#0B6E4F"}
