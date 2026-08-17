"""Evidence, readiness mappings, and Y.3172 application configuration."""

FACTORS = [
    {
        "name": "Open Data",
        "score": 2,
        "coverage": "Covered with access conditions",
        "evidence": "ADNI provides research access under its data-use terms, and ADNI-2DPC is documented as a reusable 1,000-subject representation (500 AD / 500 CN).",
    },
    {
        "name": "Access to Research",
        "score": 3,
        "coverage": "Strong evidence",
        "evidence": "NeuroAPS-Net and Sampling Matters provide the peer-reviewed method, ablation, efficiency, and sampling evidence used by this application.",
    },
    {
        "name": "Deployment & Infrastructure",
        "score": 3,
        "coverage": "Strong evidence",
        "evidence": "Reported results are 84.85% accuracy, 1.48 ms inference, and 234.6 MB peak GPU memory on one NVIDIA RTX 3060.",
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
        "coverage": "Covered in this package",
        "evidence": "The application source, offline retrieval logic, tests, launchers, configuration, and documentation are included and inspectable in this ZIP.",
    },
    {
        "name": "Sandbox",
        "score": 2,
        "coverage": "Covered for local evaluation",
        "evidence": "The package provides a local research sandbox with de-identified examples, evidence retrieval, controlled uploads, and a reproducible test suite.",
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
        "Not applicable",
        "Not applicable",
        "APS converts an existing MRI into a point-cloud representation; it does not create synthetic clinical content.",
        "Keep the dimension explicitly out of scope.",
    ),
    (
        "Cross-Domain Correlation Analysis",
        "Minimal",
        "Foundational",
        "The interface exposes the transferable APS principle: prioritize reliable, task-relevant structures while retaining provenance.",
        "Evaluate the principle in a second imaging task before claiming cross-domain performance.",
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
    ("M", "Run NeuroAPS-Net and return AD/CN probability with confidence", "Benchmark demonstrated", "Published accuracy, latency, memory, ablation, and baseline comparison"),
    ("P", "Apply quality, confidence, escalation, privacy, and clinician-review rules", "Workflow implemented", "Six-step human-in-the-loop evaluation scenario"),
    ("D", "Present imaging evidence, model evidence, policy evidence, and citations", "Implemented", "Dashboard, viewer, policy alignment, and cited knowledge assistant"),
    ("SINK", "Support clinician or researcher review and final human decision", "Implemented", "Professional decision-support interface"),
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
        "supports": "Healthcare access, quality, digital transformation, and service-model modernization.",
        "application": "Positions lightweight neuroimaging decision support as a digital-health access and quality use case.",
        "url": "https://www.vision2030.gov.sa/en/explore/programs/health-sector-transformation-program",
    },
    {
        "source": "National Strategy for Data & AI (NSDAI)",
        "authority": "SDAIA",
        "supports": "Healthcare is a priority sector; data and AI should improve access and preventive care.",
        "application": "Connects the research workflow to national data/AI capability, governance, and health priorities.",
        "url": "https://sdaia.gov.sa/en/SDAIA/SdaiaStrategies/Pages/NationalStrategyForDataAndAI.aspx",
    },
    {
        "source": "Seha Virtual Hospital & Innovation Empowerment Center",
        "authority": "Saudi Ministry of Health",
        "supports": "Remote specialist care, teleradiology, an innovation sandbox, and clinical research infrastructure.",
        "application": "Provides an evidence-based evaluation pathway for a resource-efficient imaging tool; no partnership is implied.",
        "url": "https://www.moh.gov.sa/en/ministry/projects/pages/seha-virtual-hospital.aspx",
    },
    {
        "source": "PDPL, National Data Governance Platform & AI Ethics Assessment",
        "authority": "SDAIA",
        "supports": "Personal-data protection, governance, compliance assessment, and AI-ethics evaluation.",
        "application": "Requires controlled data handling, privacy review, auditability, and documented human oversight.",
        "url": "https://dgp.sdaia.gov.sa/wps/portal/pdp/home",
    },
]


PUBLIC_DOMAIN_SOURCES = [
    {
        "tier": "Official government",
        "source": "Health Sector Transformation Program",
        "publisher": "Saudi Vision 2030",
        "supports": "Healthcare access, quality, service transformation, and digital transformation.",
        "url": "https://www.vision2030.gov.sa/en/explore/programs/health-sector-transformation-program",
        "verified": "17 Aug 2026",
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
        "source": "NSDAI strategy PDF",
        "publisher": "SDAIA",
        "supports": "Public strategy document for policy, skills, research, investment, and ecosystem alignment.",
        "url": "https://sdaia.gov.sa/en/SDAIA/SdaiaStrategies/Documents/NSDAI.pdf",
        "verified": "17 Aug 2026",
    },
    {
        "tier": "Official government",
        "source": "Seha Virtual Hospital",
        "publisher": "Saudi Ministry of Health",
        "supports": "Teleradiology, remote specialty care, innovation sandbox, and clinical research infrastructure.",
        "url": "https://www.moh.gov.sa/en/ministry/projects/pages/seha-virtual-hospital.aspx",
        "verified": "17 Aug 2026",
    },
    {
        "tier": "Official government",
        "source": "Sections of MOH Statistics",
        "publisher": "Saudi Ministry of Health",
        "supports": "Official health indicators, facilities, workforce, performance, and service statistics.",
        "url": "https://www.moh.gov.sa/en/statistics/pages/dashboard.aspx",
        "verified": "17 Aug 2026",
    },
    {
        "tier": "Official government",
        "source": "National Data Governance Platform",
        "publisher": "SDAIA",
        "supports": "PDPL services, data-governance registries, impact assessment, and regulatory sandbox access.",
        "url": "https://dgp.sdaia.gov.sa/wps/portal/pdp/home",
        "verified": "17 Aug 2026",
    },
    {
        "tier": "Official government",
        "source": "AI Ethics Self-Assessment",
        "publisher": "SDAIA",
        "supports": "Structured assessment against Saudi AI ethics principles.",
        "url": "https://dgp.sdaia.gov.sa/wps/portal/pdp/services/servicesdetails/AIEthicsAssessment/",
        "verified": "17 Aug 2026",
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
        "verified": "17 Aug 2026",
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
        "verified": "17 Aug 2026",
    },
]


SCENARIO = [
    ("1", "Case intake", "A clinician selects a de-identified T1 MRI and confirms the scan is suitable for review."),
    ("2", "Representation", "The workflow isolates the brain and prepares the anatomically labelled point cloud."),
    ("3", "Model evidence", "NeuroAPS-Net returns AD/CN decision-support evidence with confidence and version context."),
    ("4", "Clinical review", "The clinician compares the brain MRI with hippocampal, ventricular, cortical, and other regions."),
    ("5", "Escalation", "Low-confidence, poor-quality, or discordant cases are referred for specialist review and clinical testing."),
    ("6", "Decision & feedback", "The clinician records the final decision, rationale, and feedback for monitoring and improvement."),
]


POINT_LABELS = {
    1: "Hippocampus",
    3: "Ventricles",
    5: "Cortical area",
    7: "Other brain tissue",
}


SCORE_LABEL = {0: "Not addressed", 1: "Partial", 2: "Covered", 3: "Strong evidence"}
SCORE_COLOR = {0: "#B4233A", 1: "#C77B17", 2: "#2E6C7C", 3: "#0B6E4F"}
