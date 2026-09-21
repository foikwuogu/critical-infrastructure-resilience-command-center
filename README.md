# Critical Infrastructure Resilience Command Center

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22866297.svg)](https://doi.org/10.5281/zenodo.22866297)

Project #4 in a research portfolio for secure, resilient critical infrastructure.

This project integrates three independent capabilities:

1. Zero-Trust security posture
2. Post-quantum cryptographic migration readiness
3. AI predictive maintenance and asset health

It provides a **synthetic digital-twin-style command center** for critical-energy assets. It is intentionally disconnected from real SCADA/ICS equipment and has no actuator/control path.

## Architecture

```text
                    RESILIENCE COMMAND CENTER
                              |
          +-------------------+-------------------+
          |                   |                   |
          v                   v                   v
     CYBER RISK          CRYPTO RISK         ASSET HEALTH
     Zero Trust          PQC readiness       Predictive AI
          |                   |                   |
          +-------------------+-------------------+
                              |
                              v
                    RESILIENCE SCORE
                              |
                              v
                    HUMAN DECISION MAKER
```

## Core features

### Executive dashboard
- overall resilience score
- cyber risk score
- PQC migration score
- asset health score
- operational continuity score
- critical/high-risk asset counts
- active incidents
- migration backlog

### Digital twin
Synthetic representations of:
- pumps
- compressors
- turbines
- generators
- substations

Each asset has:
- criticality
- health
- failure probability
- RUL
- anomaly score
- current cryptographic profile
- PQC readiness
- identity/trust state
- network zone
- last event

### Zero Trust module
Tracks:
- device identity
- authentication state
- authorization state
- least-privilege posture
- trust score
- segmentation zone
- policy violations

### PQC module
Tracks:
- current algorithm
- quantum vulnerability
- confidentiality lifetime
- migration priority
- migration status
- readiness score

### Predictive maintenance module
Tracks:
- AI health
- failure probability
- anomaly score
- RUL
- maintenance priority

### Incident correlation
Correlates synthetic:
- cyber events
- crypto exposure
- equipment degradation
- operational impact

### Scenario simulator
Run:
- baseline
- ransomware-style cyber disruption
- PQC migration urgency
- bearing degradation
- compressor overheating
- sensor drift
- cascading cyber + physical event

### Explainability
Each resilience decision includes reason codes and contributing dimensions.

## Safety

This is a research prototype using synthetic data.

It does not:
- connect to PLCs
- connect to SCADA
- change OT setpoints
- issue shutdown commands
- access employer infrastructure
- use proprietary operational data

## Run

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m pytest -q
python run.py
```

Windows:

```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m pytest -q
python run.py
```

Dashboard:

http://127.0.0.1:8003/

API:

http://127.0.0.1:8003/docs

## Docker

```bash
docker compose up --build
```

## Research value

The project demonstrates how cybersecurity, cryptographic migration and physical asset reliability can be represented as a single resilience-management problem rather than three isolated tools.

It is intended as an experimental platform for future research on:
- cyber-physical resilience
- AI-assisted critical infrastructure risk
- PQC migration prioritization
- Zero Trust for OT environments
- cross-domain risk correlation
- resilience scoring
- human-in-the-loop decision support

## Citation

If you use this work, please cite:

```
Friday Ogochukwu Ikwuogu. Critical Infrastructure Resilience Command Center.
Zenodo. https://doi.org/10.5281/zenodo.22866297
```

DOI: [10.5281/zenodo.22866297](https://doi.org/10.5281/zenodo.22866297)

**Author:** Friday Ogochukwu Ikwuogu
ORCID: [0009-0009-2222-1318](https://orcid.org/0009-0009-2222-1318)
Affiliation: Independent Researcher, Odessa, Texas, USA

