import json
from sqlalchemy import select
from .models import Asset, Event, ScenarioRun

ALGORITHMS = ["RSA-2048", "ECDSA-P256", "X25519", "AES-256-GCM", "ML-KEM-768 + AES-256-GCM"]

def seed(db):
    if db.scalar(select(Asset.id).limit(1)):
        return
    vals = [
        ("Pump-101","pump","OT-ZONE-A",95,82,.18,680,"X25519","legacy",35),
        ("Pump-102","pump","OT-ZONE-A",75,91,.08,900,"ML-KEM-768 + AES-256-GCM","migrated",94),
        ("Compressor-201","compressor","OT-ZONE-B",98,64,.54,190,"RSA-2048","legacy",22),
        ("Turbine-301","turbine","OT-ZONE-C",100,88,.12,760,"ECDSA-P256","planned",48),
        ("Generator-401","generator","OT-ZONE-C",90,73,.31,420,"X25519","planned",52),
        ("Pump-103","pump","OT-ZONE-B",70,95,.05,1040,"ML-KEM-768 + AES-256-GCM","migrated",97),
        ("Compressor-202","compressor","OT-ZONE-B",88,78,.24,530,"ECDSA-P256","planned",58),
        ("Generator-402","generator","OT-ZONE-A",80,86,.15,710,"RSA-2048","legacy",28),
    ]
    for n,t,z,c,h,f,r,a,s,p in vals:
        db.add(Asset(name=n,asset_type=t,zone=z,criticality=c,health=h,
                     failure_probability=f,rul_hours=r,anomaly_score=min(1,f+.08),
                     crypto_algorithm=a,pqc_status=s,pqc_readiness=p,
                     identity_trust=78 if s=="migrated" else 62,least_privilege=s!="legacy"))
    db.commit()

    assets = db.scalars(select(Asset)).all()
    for i,a in enumerate(assets):
        db.add(Event(asset_id=a.id,category="baseline",severity="INFO",
                     title="Asset registered",
                     description=f"Synthetic digital-twin asset {a.name} initialized.",
                     operational_impact=0))
    db.commit()

def resilience(db):
    assets = db.scalars(select(Asset)).all()
    if not assets:
        return {"overall":0}
    avg_health=sum(a.health for a in assets)/len(assets)
    avg_pqc=sum(a.pqc_readiness for a in assets)/len(assets)
    avg_trust=sum(a.identity_trust for a in assets)/len(assets)
    availability=sum(1 for a in assets if a.status=="operational")/len(assets)*100
    risk_penalty=sum(a.failure_probability*100*.35 for a in assets)/len(assets)
    legacy=sum(1 for a in assets if a.pqc_status=="legacy")/len(assets)*12
    overall=max(0,min(100,.30*avg_health+.22*avg_pqc+.23*avg_trust+.25*availability-risk_penalty-legacy))
    cyber=max(0,min(100,.60*avg_trust+.40*avg_pqc-legacy))
    physical=max(0,min(100,.70*avg_health+.30*availability-risk_penalty))
    return {"overall":round(overall,2),"cyber":round(cyber,2),"physical":round(physical,2),
            "pqc":round(avg_pqc,2),"availability":round(availability,2)}

def scenario(db,name):
    assets=db.scalars(select(Asset)).all()
    before=resilience(db)["overall"]
    if name=="baseline":
        for a in assets:
            a.status="operational"
    elif name=="ransomware_disruption":
        for a in assets:
            if a.zone=="OT-ZONE-B":
                a.identity_trust=max(15,a.identity_trust-35)
                a.health=max(35,a.health-18)
        db.add(Event(asset_id=assets[2].id,category="cyber",severity="CRITICAL",
                     title="Synthetic lateral-movement event",
                     description="Simulated identity compromise across an OT segment.",
                     operational_impact=38))
    elif name=="pqc_migration_wave":
        for a in assets:
            if a.pqc_status=="legacy":
                a.pqc_status="planned"; a.pqc_readiness=min(90,a.pqc_readiness+35)
        db.add(Event(asset_id=assets[0].id,category="crypto",severity="HIGH",
                     title="PQC migration initiated",
                     description="Synthetic migration program prioritizes legacy cryptography.",
                     operational_impact=5))
    elif name=="bearing_degradation":
        for a in assets:
            if a.asset_type in {"pump","generator"}:
                a.health=max(30,a.health-20); a.failure_probability=min(.98,a.failure_probability+.28)
                a.rul_hours=max(24,a.rul_hours-300); a.anomaly_score=min(1,a.anomaly_score+.35)
        db.add(Event(asset_id=assets[0].id,category="physical",severity="HIGH",
                     title="Bearing degradation detected",
                     description="Synthetic vibration/degradation condition propagated to the asset twin.",
                     operational_impact=25))
    elif name=="compressor_overheat":
        for a in assets:
            if a.asset_type=="compressor":
                a.health=max(25,a.health-27); a.failure_probability=min(.98,a.failure_probability+.32)
                a.rul_hours=max(12,a.rul_hours-360); a.anomaly_score=min(1,a.anomaly_score+.4)
        db.add(Event(asset_id=assets[2].id,category="physical",severity="CRITICAL",
                     title="Compressor overheating",
                     description="Synthetic thermal excursion with elevated failure risk.",
                     operational_impact=40))
    elif name=="cascading_event":
        for a in assets:
            a.health=max(25,a.health-12); a.failure_probability=min(.99,a.failure_probability+.18)
            a.identity_trust=max(20,a.identity_trust-18)
            if a.pqc_status=="legacy": a.pqc_readiness=max(5,a.pqc_readiness-10)
        db.add(Event(asset_id=assets[2].id,category="correlated",severity="CRITICAL",
                     title="Cyber-physical cascade",
                     description="Synthetic simultaneous cyber, cryptographic and equipment degradation.",
                     operational_impact=60))
    else:
        raise KeyError(name)
    db.commit()
    after=resilience(db)["overall"]
    explanation={
        "scenario":name,
        "resilience_change":round(after-before,2),
        "decision_rule":"Prioritize actions that reduce the largest combined cyber, cryptographic and physical risk.",
        "human_review_required":True
    }
    db.add(ScenarioRun(scenario=name,resilience_before=before,resilience_after=after,
                       explanation=json.dumps(explanation)))
    db.commit()
    return {"before":before,"after":after,"change":round(after-before,2),"explanation":explanation}
