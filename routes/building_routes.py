from fastapi import APIRouter, HTTPException
from models.building import Building
from schemas.building_response import BuildingResponse

router = APIRouter()
from pydantic import BaseModel

class BuildingCreate(BaseModel):
    name: str
    facility_id: int

class BuildingUpdate(BaseModel):
    name: str = None
    facility_id: int = None


# Create a new Building
@router.post("/", response_model=BuildingResponse)
async def create_building(building_data: BuildingCreate):
    building = await Building.create(**building_data.dict())
    return building

# Get all Buildings
@router.get("/", response_model=list[BuildingResponse])
async def get_all_buildings():
    buildings = await Building.all()
    return buildings

# Get a Building by ID
@router.get("/{building_id}", response_model=BuildingResponse)
async def get_building(building_id: int):
    building = await Building.get_or_none(id=building_id)
    if not building:
        raise HTTPException(status_code=404, detail="Building not found")
    return building

# Update a Building by ID
@router.put("/{building_id}", response_model=BuildingResponse)
async def update_building(building_id: int, building_data: BuildingUpdate):
    building = await Building.get_or_none(id=building_id)
    if not building:
        raise HTTPException(status_code=404, detail="Building not found")
    
    for field, value in building_data.dict(exclude_unset=True).items():
        setattr(building, field, value)
    
    await building.save()
    return building

# Delete a Building by ID
@router.delete("/{building_id}", response_model=dict)
async def delete_building(building_id: int):
    building = await Building.get_or_none(id=building_id)
    if not building:
        raise HTTPException(status_code=404, detail="Building not found")
    
    await building.delete()
    return {"message": "Building deleted"}
