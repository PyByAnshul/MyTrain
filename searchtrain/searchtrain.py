from flask import Blueprint
import requests







searchtrain = Blueprint('searchtrain_blueprint', __name__)







@searchtrain.route('/searchtrain')
def index():

    url = "https://trains.p.rapidapi.com/"

    payload = { "search": "delhi" }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "793a7dc73cmsh5fc4ac4754f7c66p1ca8ebjsn655a0b81d347",
        "X-RapidAPI-Host": "trains.p.rapidapi.com"
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response.json())
    return "This is an example app"