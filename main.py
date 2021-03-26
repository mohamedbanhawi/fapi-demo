from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from typing import Optional
import requests

app = FastAPI()

#### city class and db
class City(BaseModel):
    """ Class for keeping track of city """
    name: str
    timezone: str
    current_time: Optional[str] 

city_db: [City] = [] # city_db
 
def save_city_to_db(city: City):
    city_db.append(city)

def delete_city_from_db(city_id: int):
    city_db.pop(city_id)

def get_city_from_db(city_id: int):
    return city_db[city_id]

#update time zone
def update_city_time(city):
    time_response = requests.get('http://worldtimeapi.org/api/timezone/' + city.timezone)
    if time_response.ok:
        city.current_time = time_response.json()['datetime']

#### endpoints

@app.get('/')
def index():
    return {'key': 'value'}

@app.get('/cities')
async def get_cities_endpoint(background_tasks: BackgroundTasks):
    for city in city_db:
        background_tasks.add_task(update_city_time, city)
    return city_db

@app.get('/cities/{city_id}')
def get_city_endpoint(city_id: int):
    city = get_city_from_db(city_id)
    update_city_time(city)
    return city

@app.post('/cities')
def create_city_endpoint(city: City):
    update_city_time(city)
    save_city_to_db(city)
    return city_db[-1]

@app.delete('/cities/{city_id}')
def delete_city_endpoint(city_id: int):
    delete_city_from_db(city_id)
    return 200