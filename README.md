# SaaS Lead Conversion


### High-Velocity Lead Scoring & Enrichment for B2B SaaS Growth


## Problem Statement
In a high-growth SaaS environment, the Sales team are overwhelmed by a "Free-Tier Flood" with thousands of new signups daily and no clear way to prioritize outreach. So I built an automated system to identify, enrich, and alert on Product Qualified Leads (PQLs) in real-time.



## Technical Architecture
This repository contains a modular, production-grade GTM logic stack:

* **Extraction & Modeling (DuckDB / SQL):** A local OLAP engine that transforms raw behavioral logs into a fct_pql_master table using weighted intent scoring (Teammate invites, feature adoption, and login frequency).
* **Enrichment Engine (Python):** A "Logic-as-Code" layer that simulates a Clay Waterfall, fetching firmographic data (Industry, Funding, Tech Stack) for identified PQLs.
* **GTM Strategy Mapping:** A custom Python engine that intersects Product Signals with Company Size to map specific Personas (e.g., VP Ops vs. Founder) to tailored Value Propositions.
* **Activation Layer (n8n & Webhooks):** An orchestration bridge that pushes data payloads from the warehouse to Slack and Mailing services for real-time sales intervention.



## Repository Structure
* **/notebooks:** SQL modeling of the PQL scoring matrix and exploratory distribution analysis of user intent.
* **/scripts:** The '/gtm_alert_engine.py' script featuring the Enrichment Mapping logic and Webhook trigger.
* **/data:** Tiered storage containing '/raw' usage data and '/processed' CRM sync-ready payloads.
* **/sql:** The transformation logic used to define leads into Intent tiers.



## Problems Solved

* **Automated Lead Prioritization:** Implemented a 100-point weighted scoring matrix that filters out 60% of low-intent "noise," focusing Sales on the top 10% of users.
* **Contextual Enrichment:** Bridges the "Context Gap" by simulating Clay-style enrichment, providing AEs with funding and industry data before they start their research.
* **Persona-Based Messaging:** Solves "Generic Outreach" by automatically mapping leads to specific pain points (e.g., Security for Enterprise, Velocity for Startups).
* **System Resilience:** Developed a data-validation layer in Python to handle SQL naming inconsistencies and ensure zero-failure synchronization between the warehouse and GTM tools.
