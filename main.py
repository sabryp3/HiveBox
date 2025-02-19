from fastapi import FastAPI
import requests
import httpx
from version import VERSION



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


boxes = ["5eba5fbad46fb8001b799786",
           "5a77184229b729001a150c10",
           "5ec950aed0545b001ca9a93e"
           ]

boxes_url = "https://api.opensensemap.org/boxes/"

def get_temp(response):
    x = 0
    for sensor in response['sensors']:
        if 'Temperatur' in sensor['title']:
            sensor_temp = float(sensor['lastMeasurement']['value'])
    return sensor_temp


@app.get("/temperature")
def temp_endpoint():
    temp_list = []
    for id in boxes:
        sensor_url = boxes_url+id
        response = httpx.get(sensor_url,timeout=600).json()
        sensor_temp = get_temp(response)
        temp_list.append(sensor_temp)
    average = sum(temp_list)/len(temp_list)
    return("average temperature is "+str(average))






   


