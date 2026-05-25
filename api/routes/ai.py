from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any

from api.ai.narrators.narrator import intelligence_narrator
from api.ai.query_engine.context import dossier_query_engine
from api.ai.exporters.formatter import intelligence_exporter

router = APIRouter()

class QueryRequest(BaseModel):
    query: str
    context: Dict[str, Any]

class DossierRequest(BaseModel):
    dossier: Dict[str, Any]

@router.post("/query")
async def execute_query(req: QueryRequest):
    try:
        return await dossier_query_engine.execute_query(req.query, req.context)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/narrate")
async def generate_narrative(req: DossierRequest):
    try:
        narrative = await intelligence_narrator.generate_dossier_narrative(req.dossier)
        return {"narrative": narrative}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/export/markdown")
async def export_markdown(req: DossierRequest):
    try:
        narrative = await intelligence_narrator.generate_dossier_narrative(req.dossier)
        md = intelligence_exporter.export_markdown(req.dossier, narrative)
        return {"markdown": md}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
