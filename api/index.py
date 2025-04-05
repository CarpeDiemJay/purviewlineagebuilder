from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
import json
from pyapacheatlas.auth import ServicePrincipalAuthentication
from pyapacheatlas.core import PurviewClient, AtlasProcess, AtlasEntity
from pyapacheatlas.core.util import GuidTracker

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration model
class Settings(BaseModel):
    accountName: str
    clientId: str
    tenantId: str

# Store settings in memory (in production, use a proper database)
settings = Settings(
    accountName=os.getenv("PURVIEW_ACCOUNT_NAME", ""),
    clientId=os.getenv("PURVIEW_CLIENT_ID", ""),
    tenantId=os.getenv("PURVIEW_TENANT_ID", "")
)

# Initialize Purview client
def get_purview_client():
    if not all([settings.accountName, settings.clientId, settings.tenantId]):
        raise HTTPException(status_code=400, detail="Purview settings not configured")
    
    oauth = ServicePrincipalAuthentication(
        client_id=settings.clientId,
        tenant_id=settings.tenantId,
        client_secret=os.getenv("PURVIEW_CLIENT_SECRET", "")
    )
    
    return PurviewClient(
        account_name=settings.accountName,
        authentication=oauth
    )

@app.get("/api/search")
async def search_assets(type: str, query: str):
    try:
        client = get_purview_client()
        
        if type == "sql":
            # Search for SQL tables
            results = client.search_entities(
                query=query,
                search_filter={"entityType": ["azure_sql_table"]}
            )
        elif type == "powerbi":
            # Search for Power BI datasets
            results = client.search_entities(
                query=query,
                search_filter={"entityType": ["powerbi_dataset"]}
            )
        else:
            raise HTTPException(status_code=400, detail="Invalid asset type")
        
        return [{
            "name": r["name"],
            "qualifiedName": r["qualifiedName"],
            "type": r["typeName"]
        } for r in results]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/lineage")
async def create_lineage(data: dict):
    try:
        client = get_purview_client()
        gt = GuidTracker()
        
        left_asset = data["leftAsset"]
        right_asset = data["rightAsset"]
        
        # Get the process node for the Power BI dataset
        process_qn = right_asset["qualifiedName"].replace("/datasets/", "/datasetprocesses/")
        
        # Create the input entity
        input_entity = AtlasEntity(
            name=left_asset["name"],
            typeName=left_asset["type"],
            qualified_name=left_asset["qualifiedName"]
        )
        
        # Create the process entity
        process_entity = AtlasProcess(
            name=f"{left_asset['name']} to {right_asset['name']} Process",
            typeName="powerbi_dataset_process",
            qualified_name=process_qn,
            guid=gt.get_guid(),
            inputs=[input_entity],
            outputs=None  # Preserve existing output metadata
        )
        
        # Upload the entities
        results = client.upload_entities(batch=[process_entity])
        return {"message": "Lineage created successfully", "results": results}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/settings")
async def get_settings():
    return settings

@app.post("/api/settings")
async def update_settings(new_settings: Settings):
    global settings
    settings = new_settings
    return {"message": "Settings updated successfully"} 