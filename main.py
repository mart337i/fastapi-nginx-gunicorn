from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from routes.facility_routes import router as facility_router
from routes.alarm_routes import router as alarm_router
from routes.building_routes import router as building_routes
from routes.pollution_sensor_routes import router as pollution_sensor_routes
from routes.temp_humidity_sensor_routes import router as temp_humidity_sensor_routes



app = FastAPI()

# Register Tortoise with FastAPI
register_tortoise(
    app,
    db_url="mysql://pi:Vds79bzw-@localhost:3306/facility",  # Use 'mysql' scheme
    modules={"models": ["models.facility",'models.alarm','models.building','models.pollution_sensor','models.temperature_humidity_sensor']},
    generate_schemas=True,
)
# Include the Facility routes
app.include_router(facility_router, prefix="/facility")
app.include_router(alarm_router, prefix="/alarm")
app.include_router(building_routes, prefix="/building_routes")
app.include_router(pollution_sensor_routes, prefix="/pollution_sensor_routes")
app.include_router(temp_humidity_sensor_routes, prefix="/temp_humidity_sensor_routes")

