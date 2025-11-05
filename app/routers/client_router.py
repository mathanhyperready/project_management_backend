from fastapi import APIRouter, HTTPException,status
from app.database import db
from app.models.client_model import ClientResponse,ClientCreate,ClientUpdate
from datetime import datetime, date
from typing import List

router = APIRouter()

@router.get("/", response_model=List[ClientResponse])
async def get_all_clients():
    try:
        clients = await db.client.find_many(
            include={"creator": True},   # ✅ fetch creator details
            order={"id": "asc"}
        )
        return clients
    except HTTPException:
        raise
    except Exception as e:
        print("Get All Clients Error:", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to Get Clients"
        )
    

@router.get("/{client_id}")
async def get_single_client(client_id : int):
    try:
        clients = await db.client.find_many(where = {"id" : client_id})
        return clients
    except HTTPException:
        raise
        
    except Exception as e:
        print("Get All Clients Error", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Failed to Get Clients")
    
    


@router.post("/", response_model=ClientResponse)
async def create_client(data: ClientCreate):
    try:
        # Check duplicate
        existing_client = await db.client.find_first(where={"name": data.name})
        if existing_client:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Client name '{data.name}' already exists"
            )

        # ✅ Accept created_by manually (if passed from frontend)
        client_data = data.dict()
        if "created_by" not in client_data or not client_data["created_by"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing created_by user ID"
            )

        # ✅ Create client and include creator relation in response
        client = await db.client.create(
            data=client_data,
            include={"creator": True}
        )
        return client

    except HTTPException:
        raise
    except Exception as e:
        print("Client Creation Failed:", e)
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Client creation failed due to server error"
        )


        
@router.put("/{client_id}", response_model=ClientResponse)
async def update_client(client_id: int, client: ClientUpdate):
    try:
        data = client.dict(exclude_unset=True)
        if not data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields provided to update"
            )

        existing = await db.client.find_unique(where={"id": client_id})
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Client with id {client_id} not found"
            )

        updated_client = await db.client.update(
            where={"id": client_id},
            data=data
        )
        return updated_client

    except HTTPException:
        raise
    except Exception as e:
        print("Client Update Failed:", e)
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Client update failed due to server error"
        )

@router.delete("/{client_id}")
async def delete_client(client_id : int):
    try:
        client_with_project = await db.project.find_many(where={"client_id": client_id})
        if client_with_project:
            raise HTTPException(
                status_code=400,
                detail="Cannot delete client because project are assigned to it"
            )

        await db.client.delete(where={"id": client_id})
        return {"message": f"Client {client_id} deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        print("Delete Role Error:", e)
        raise HTTPException(status_code=500, detail="Failed to delete client")
    

        