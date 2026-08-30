# ITU Hackathon Criteria Cross-Check

Validated against `ITU-Hac-Final.docx` on 29 August 2026.

| DOCX criterion | Application coverage | Release 7.4 disposition |
|---|---|---|
| Problem, solution, value proposition | Covered | Context & Impact and Readiness connect fragmented MRI analysis, anatomical point clouds, compute efficiency, and human review. |
| NeuroAPS-Net evidence | Covered with boundary | Shows the published 84.85% accuracy, 1.48 ms latency, 234.6 MB peak GPU memory, 8,192-point configuration, and baseline comparison. These are research benchmark results, not a clinical-performance claim. |
| ADNI dataset | Updated | The ADNI Data and Samples official links are included: `https://adni.loni.usc.edu/` and `https://adni.loni.usc.edu/data-samples/`. ADNI is labelled controlled research access, not unrestricted public-domain data. |
| ITU-T Y.3172 | Covered | ML Intent, SRC, C, PP, M, P, D, SINK, MLFO, Sandbox, and Underlay are mapped. Model and Policy nodes state that live runtime enforcement remains pending the versioned model and preprocessing bundle. |
| Six readiness factors | Covered with qualification | Open Data, Access to Research, Deployment & Infrastructure, Standards, Open Source, and Sandbox are present. “Open Source” describes the inspectable packaged source; public GitHub publication is not claimed. |
| Thirteen readiness dimensions | Covered | All 13 dimensions include papers-only rating, current application coverage, implemented evidence, and next evaluation. Generated Content and Cross-Domain are labelled foundational rather than complete. |
| Six-step human review | Covered | Case intake, representation, model evidence, clinical review, escalation, and final decision/feedback are shown. The model step is explicitly future runtime behavior. |
| PDPL and AI ethics | Updated | Includes applicable lawful basis, purpose limitation, Article 25 impact-assessment triggers, Article 26 health-data safeguards, Article 33 processing records, human confirmation, escalation, audit, and prohibited unrelated profiling/advertising. The self-assessment is not presented as certification. |
| Four-step governance stress test | Covered | Controlled intake, human confirmation, purpose boundary, and escalation/audit are implemented as a synthetic evaluation scenario. |
| HSTP / prevention | Corrected | Official HSTP evidence supports disease prevention. “From treatment-based care toward prevention and early intervention” is an application interpretation, not a direct HSTP quotation or adoption claim. |
| Saudi MOH statistics dashboard | Cross-checked | The direct dashboard link is included. It supports health-indicator, workforce, facility, service, quality, and prevention/therapy context; it is not used as a single national or Dammam Alzheimer prevalence source. |
| Seha Virtual Hospital | Covered with boundary | Official capabilities support a plausible future evaluation pathway. No partnership, integration, pilot, regulatory approval, or deployment is claimed. |
| Saudi regional evidence | Covered with boundary | Includes public Saudi and Eastern Province/Dammam research. The 3.37% value is tied to the National Guard Health System study population, not the Saudi general population. The 152-patient KFSH study used clinical features, not MRI. |
| Evidence library / assistant | Covered | Ten characterized records, 46 regenerated offline retrieval chunks, visible citations, filters, and source links are present. The assistant retrieves public evidence and does not produce diagnosis or trained-model predictions. |
| MRI → point cloud workspace | Covered | Ten registered MRI/mask/PLY subject sets, brain-only slice views, 8,192-point clouds, and named labels for hippocampus, ventricles, cortical area, and other brain tissue are included. |
| Deployment workbench | Covered with boundary | The integration interface and prerequisites are documented. Live weights, exact preprocessing, class mapping, Saudi validation, clinical usability, identity/audit integration, and institutional approvals are pending. |

## Remaining evidence items

- The trained NeuroAPS-Net checkpoint and original preprocessing/runtime bundle have not been supplied.
- The packaged subject examples do not constitute AD-versus-CN validation or a Saudi cohort.
- A public link for the characterized “Sampling Matters” paper has not been supplied.
- A single source link for the general clinical-background record should be added before formal publication.
- Public GitHub publication is not verified by this release.
- Formal privacy, legal, security, AI-ethics, clinical-governance, usability, and regulatory reviews remain future work.
