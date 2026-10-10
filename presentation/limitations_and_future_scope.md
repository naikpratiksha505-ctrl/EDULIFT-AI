# EduLift AI — Limitations and Future Scope

This document provides a realistic, honest appraisal of current system limitations and outlines a structured engineering roadmap for production readiness.

---

## 1. Current System Limitations

### A. Synthetic Data Limitations
* **Simulated Distributions:** The machine learning model is trained on 500 synthetically generated student profiles. Real-world learning behaviors exhibit far more complex socio-economic, health, and curriculum variations that cannot be captured by simple Gaussian distributions.
* **Non-Clinical & Non-Official:** Predictions are purely advisory demonstrations. They are not psychometrically or pedagogically validated and must never be used for administrative sanctions, grading, or retention penalties.
* **Static Features:** Current features cover attendance, average test marks, assignment rates, and short-term trends. Qualitative factors like project collaboration quality or self-reported stress are not currently modeled.

### B. Security & Architectural Scope (MVP Status)
* **Local SQLite Concurrency:** SQLite is ideal for demonstration and local prototypes, but it lacks the high-concurrency throughput needed for an entire university campus with thousands of simultaneous users.
* **Session Storage:** Sessions are signed client cookies using Flask's `secret_key`. In high-security enterprise environments, server-side Redis session stores with hardware-security token support are standard.
* **Authentication Single-Factor:** The system currently relies on single-factor username and hashed passwords. Campus deployments would require Single Sign-On (SSO) via SAML 2.0, OAuth2, or institutional LDAP.
* **Static Role Hierarchy:** There are currently two strict roles: Student and Faculty. Department heads, deans, and academic counselors are not yet broken out into distinct permission tiers.

---

## 2. Future Engineering Roadmap

### Phase 1: Institutional Compliance & Privacy Hardening
1. **FERPA / GDPR Alignment:** Implement audit logging for every faculty inspection of student records, ensuring compliance with student privacy regulations.
2. **Campus SSO Integration:** Connect with Microsoft Azure AD / Google Workspace for Education so students log in using institutional accounts.
3. **Database Migration to PostgreSQL:** Transition SQLite schemas to PostgreSQL with connection pooling to handle campus-wide concurrent traffic.

### Phase 2: Enhanced AI & Advisory Enhancements
1. **Explainable AI (SHAP / LIME):** Integrate SHAP (SHapley Additive exPlanations) values to provide granular mathematical proofs of feature contributions for each prediction.
2. **Context-Aware Study Recommendations:** Incorporate Bloom's Taxonomy into study planner generation (e.g., distinguishing between introductory concept review and advanced coding lab practice).
3. **Opt-In Peer Tutoring Matching:** Enable students who excel in a subject (e.g., scoring >85%) to volunteer as peer mentors for classmates requesting study support.

### Phase 3: Mobile & LMS Connectivity
1. **Learning Management System (LMS) Webhooks:** Build automated sync adapters for Canvas, Moodle, and Google Classroom to ingest quiz submissions and attendance logs automatically.
2. **Progressive Web App (PWA):** Enable offline study schedule checklists and push notifications for upcoming study sessions on mobile devices.
3. **Faculty Multi-Cohort Dashboard:** Allow academic deans and department coordinators to benchmark curriculum outcomes across multiple engineering sections.
