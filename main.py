import os
from dotenv import load_dotenv
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
import httpx 
import aioredis 
from version import VERSION

# Load environment variables
load_dotenv()

app = FastAPI()

# Instrument your app with default metrics and expose the metrics with /metrics endpoint
Instrumentator().instrument(app).expose(app)

# Initialize Redis connection
redis = None

@app.on_event("startup")
async def startup_event():
    global redis
    redis = await aioredis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"))

@app.on_event("shutdown")
async def shutdown_event():
    await redis.close()
   
def get_version() -> str:
    """Returns the current version of the software."""
    return VERSION 
def main():
    """Main function to execute the program."""
    version = get_version()
    print(f"Current software version: {version}")

if __name__ == "__main__":
    main()

@app.get("/version")
def version_endpoint():
    version = get_version()
    return (f"Current software version: {version}")


# getting boxes IDs
boxes = os.getenv("BOXES").split(",")
print(boxes)

# getting API URL of Boxes
boxes_url = os.getenv("BOXES_URL")

# getting the temperature from the provided API response
def get_temp(response):
    for sensor in response['sensors']:
        if 'Temperatur' in sensor['title']:
            sensor_temp = float(sensor['lastMeasurement']['value'])
    return sensor_temp


@app.get("/temperature")
async def temp_endpoint():
    cached_temp = await redis.get("average_temperature")
    if cached_temp:
        return f"Cached average temperature is {cached_temp.decode('utf-8')}"
    else:
# Fetch and calculate temperature if not cached
        temp_list = []
        for id in boxes:
            sensor_url = boxes_url+id
            response = httpx.get(sensor_url,timeout=600).json()
            sensor_temp = get_temp(response)
            temp_list.append(sensor_temp)
        average = sum(temp_list)/len(temp_list)
# Cache the result
        await redis.set("average_temperature", str(average), ex=300)  # Cache for 5 minutes
        
    if average <= 10:
        return("Too cold")
    elif 11 <= average <= 26:
        return("Good")
    else:
        return("Too hot")







   


