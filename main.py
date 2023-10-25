from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from routes.facility_routes import router as facility_router

app = FastAPI()

# Register Tortoise with FastAPI
register_tortoise(
    app,
    db_url="mysql://pi:Vds79bzw-@localhost:3306/facility",  # Use 'mysql' scheme
    modules={"models": ["models.facility"]},
    generate_schemas=True,
)
# Include the Facility routes
app.include_router(facility_router, prefix="/facility")
