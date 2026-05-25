from fastapi import APIRouter, HTTPException
from api.website_scanner.reports.compiler import dossier_compiler

router = APIRouter()

@router.get("/")
async def list_websites():
    return {"data": []}

@router.get("/scan/{domain}")
async def scan_website(domain: str):
    try:
        report = await dossier_compiler.compile_report(domain)
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

