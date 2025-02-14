from fastapi import FastAPI
from version import VERSION
import requests
import httpx

app = FastAPI()

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


sensors = ["5eba5fbad46fb8001b799786",
           "5a77184229b729001a150c10",
           "5ec950aed0545b001ca9a93e",
           ]

sensor_url = "https://api.opensensemap.org/boxes/"

@app.get("/temperature")
def temp_endpoint():
    for sensor_id in sensors:
        temp_url = sensor_url+sensor_id
        response = requests.get(temp_url,timeout=600).json()
        total_temp = 0
        x = 0
        while True:
            if response['sensors'][x]['title'].__contains__('Temperatur'):
                sensor_temp = float(response ['sensors'][x]['lastMeasurement']['value'])
                total_temp = total_temp+sensor_temp
                break
            x+=1
    average = total_temp/3
    return("average temperature is "+str(average))





   


