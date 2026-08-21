from pathlib import Path
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import select
from sqlalchemy.orm import Session
from .config import APP_NAME, APP_VERSION
from .database import Base, engine, SessionLocal, get_db
from .models import Asset, Event, ScenarioRun
from .engine import seed, resilience, scenario

Base.metadata.create_all(bind=engine)
app=FastAPI(title=APP_NAME,version=APP_VERSION)
app.mount("/static", StaticFiles(directory=Path(__file__).parent/"static"), name="static")

@app.on_event("startup")
def startup():
    db=SessionLocal()
    try: seed(db)
    finally: db.close()

def get_seeded_db(db:Session=Depends(get_db)):
    seed(db)
    return db

@app.get("/",include_in_schema=False)
def home(): return FileResponse(Path(__file__).parent/"static/index.html")

@app.get("/api/health")
def health(): return {"status":"ok","service":APP_NAME,"version":APP_VERSION}

@app.get("/api/resilience")
def get_resilience(db:Session=Depends(get_seeded_db)): return resilience(db)

@app.get("/api/assets")
def assets(db:Session=Depends(get_seeded_db)):
    return db.scalars(select(Asset).order_by(Asset.id)).all()

@app.get("/api/events")
def events(db:Session=Depends(get_seeded_db)):
    return db.scalars(select(Event).order_by(Event.id.desc()).limit(100)).all()

@app.get("/api/scenarios")
def scenarios():
    return ["baseline","ransomware_disruption","pqc_migration_wave","bearing_degradation","compressor_overheat","cascading_event"]

@app.post("/api/scenarios/{name}")
def run_scenario(name:str,db:Session=Depends(get_seeded_db)):
    try:return scenario(db,name)
    except KeyError:raise HTTPException(404,"Unknown scenario")

@app.post("/api/reset")
def reset(db:Session=Depends(get_seeded_db)):
    db.query(Event).delete()
    db.query(ScenarioRun).delete()
    db.query(Asset).delete()
    db.commit()
    seed(db)
    return resilience(db)

@app.get("/api/migration")
def migration(db:Session=Depends(get_seeded_db)):
    assets=db.scalars(select(Asset)).all()
    return {
        "total":len(assets),
        "legacy":sum(a.pqc_status=="legacy" for a in assets),
        "planned":sum(a.pqc_status=="planned" for a in assets),
        "migrated":sum(a.pqc_status=="migrated" for a in assets),
        "priority":[
            {"asset":a.name,"algorithm":a.crypto_algorithm,"readiness":a.pqc_readiness,
             "criticality":a.criticality}
            for a in sorted(assets,key=lambda x:(x.pqc_readiness,-x.criticality))[:5]
        ]
    }
