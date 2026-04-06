
🏗️ System Architecture – Agent-Inspired Medical Imaging AI

                    ┌──────────────────────────┐
                    │   Medical Image Input    │
                    │ (JPEG / PNG / DICOM /   │
                    │        NIfTI)           │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │   Preprocessing Layer    │
                    │ - pydicom (DICOM)       │
                    │ - NiBabel (NIfTI)       │
                    │ - Normalization         │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │     Vision LLM Layer     │
                    │ - Image Understanding    │
                    │ - Region Detection       │
                    │ - Structured Output      │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │   Findings Extraction    │
                    │ - Key anomalies          │
                    │ - Medical keywords       │
                    └────────────┬────────────┘
                                 │
               ┌─────────────────┼─────────────────┐
               │                 │                 │
               ▼                 ▼                 ▼
   ┌──────────────────┐  ┌──────────────────┐  ┌────────────────────┐
   │ Heatmap Generator│  │  Vector DB (RAG) │  │ Literature Retrieval│
   │   (OpenCV)       │  │  (FAISS / Embed) │  │   (PubMed API)      │
   └────────┬─────────┘  └────────┬─────────┘  └─────────┬──────────┘
            │                     │                      │
            └────────────┬────────┴────────────┬────────┘
                         │                     │
                         ▼                     ▼
               ┌──────────────────────────┐
               │   Report Generation LLM  │
               │ - Radiology-style report │
               │ - Research grounding     │
               └────────────┬────────────┘
                            │
                            ▼
               ┌──────────────────────────┐
               │   Semantic Q&A Layer     │
               │ - Context retrieval      │
               │ - Follow-up queries      │
               └────────────┬────────────┘
                            │
                            ▼
               ┌──────────────────────────┐
               │ Multi-Agent Collaboration│
               │ - Specialist simulation  │
               │ - Discussion reasoning   │
               └────────────┬────────────┘
                            │
                            ▼
               ┌──────────────────────────┐
               │        Outputs           │
               │ - PDF Report             │
               │ - Heatmaps               │
               │ - Structured JSON        │
               │ - Q&A Responses          │
               └──────────────────────────┘

---

🧠 Architecture Highlights

- Modular pipeline → Each stage is independently replaceable
- Hybrid AI system → Combines Vision LLM + RAG + CV
- Interpretability-first → Heatmaps + structured outputs
- Research-grounded → PubMed integration
- Agent-inspired workflow → Multi-step reasoning instead of single LLM call

---

🔁 Data Flow Summary

Input Image → Preprocessing → Vision LLM → Findings → (Heatmap + RAG + PubMed) → Report → Q&A → Multi-Agent Discussion → Final Outputs
