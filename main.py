import asyncio
import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from prometheus_fastapi_instrumentator import Instrumentator
from minio import Minio
import httpx 
from redis.asyncio import Redis
from version import VERSION
import io

# Load environment variables
load_dotenv()

# Initialize Redis connection
redis = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global redis
    # Startup logic
    redis = await Redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"))
    minio_task = asyncio.create_task(schedule_minio_upload())  # Start the Minio upload task
    try:
        yield
    finally:
        # Shutdown logic
        minio_task.cancel()  # Cancel the Minio upload task
        await redis.aclose()

# Pass the lifespan context manager to the FastAPI app
app = FastAPI(lifespan=lifespan)

# Instrument your app with default metrics and expose the metrics with /metrics endpoint
Instrumentator().instrument(app).expose(app)

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

@app.get("/readyz")
async def readiness():
    x=0
    for id in boxes:
        sensor_url = boxes_url+id
        response = httpx.get(sensor_url,timeout=600).json()
        if response.status_code == 200:
            x+=1
        else:
            continue
    if x >= (len(boxes)/2):
        raise HTTPException(status_code=200, detail="Service is ready")
    else:
        raise HTTPException(status_code=503, detail="Service unavailable")




# Initialize Minio client
client = Minio(
    "play.min.io:9000",
    access_key=os.getenv("MINIO_ACCESS_KEY"),
    secret_key=os.getenv("MINIO_SECRET_KEY"),
    secure=True
)
# upload the cached temperature to Minio
async def stream_minio():
    # Fetch the cached temperature from Redis
    cached_temp = await redis.get("average_temperature")
    
    # If no cached temperature is found, fetch and cache it
    if not cached_temp:
        temp_list = []
        for id in boxes:
            sensor_url = boxes_url + id
            response = httpx.get(sensor_url, timeout=600).json()
            sensor_temp = get_temp(response)
            temp_list.append(sensor_temp)
        average = sum(temp_list) / len(temp_list)
        
        # Cache the result in Redis
        cached_temp = str(average).encode("utf-8")  # Convert to bytes for Redis
        await redis.set("average_temperature", cached_temp, ex=300)  # Cache for 5 minutes

    # Wrap the bytes object in a file-like object
    cached_temp_stream = io.BytesIO(cached_temp)
    
    # Upload the file-like object to Minio
    result = client.put_object(
        "hive-bucket",  # Bucket name
        "hive-temp",    # Object name
        cached_temp_stream,  # File-like object
        length=len(cached_temp),  # Length of the data
        part_size=10*1024*1024,  # Part size for multipart uploads
    )


# upload the cached temperature to Minio every 5 minutes
async def schedule_minio_upload():
    while True:
        await stream_minio()  # Add await here to properly call the coroutine
        await asyncio.sleep(300)  # Sleep for 5 minutes

@app.get("/store")
async def stream_minio_endpoint():
    await stream_minio()
    return("Cached temperature uploaded to Minio")