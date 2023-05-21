from flask import Flask
from flask import request
from pprint import pprint
import json
import osmnx as ox
import openai
import shapely.wkt
from shapely.geometry import mapping

from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

from data_loader import DataLoader

loader = DataLoader()

app = Flask(__name__)
gpt_model = "gpt-4"

with open("secrets.json", "r") as f:
    secrets = json.load(f)
    openai.api_key = secrets["gpt-token"]
    

@app.route('/building-footprints', methods=['POST'])
@cross_origin()
def test_route():
    payload = request.get_json()

    prompt = payload["prompt"]

    result = query_chat_gpt(prompt, json_output=payload["isJson"])

    return {
        "result": result
    }

@app.route('/sql', methods=['POST'])
@cross_origin()
def sql_route():
    payload = request.get_json()

    prompt = payload["prompt"]

    gpt_primer = """

    Do not answer the question, instead generate a SQL query to select relevant data from a table called CENSUSHEAT. Here are the fields available to you:

    index INTEGER NOT NULL PRIMARY KEY,
    census_county TEXT,
    census_city TEXT,
    heat_health_action_index FLOAT,
    perc_children FLOAT,
    perc_no_hs_diploma FLOAT,
    perc_elderly FLOAT,
    perc_outdoor_workers FLOAT,
    tract_population FLOAT,
    perc_poverty FLOAT,
    perc_two_races FLOAT,
    perc_nonwhite FLOAT,
    perc_no_vehicle_access FLOAT,
    perc_linguistic_isolation FLOAT,
    perc_no_transit_access FLOAT,
    asthma_prevalence FLOAT,
    perc_low_birth_weight FLOAT,
    cardio_disease_prevalence FLOAT,
    perc_ambulatory_disability FLOAT,
    perc_cognitive_disability FLOAT,
    pm25_concentration FLOAT,
    perc_impervious_surfaces FLOAT,
    change_in_dev FLOAT,
    perc_no_tree_canopy FLOAT,
    uhii_avgdeltat FLOAT,
    ozone_exceedance FLOAT,
    CT20 INTEGER NOT NULL,
    OBJECTID INTEGER NOT NULL.
    LABEL FLOAT,
    ShapeSTArea FLOAT,
    ShapeSTLength FLOAT,
    geometry TEXT

    Return just the valid SQL query string, do not add any additional text. Select all fields with *.
    """

    full_prompt = prompt + gpt_primer

    sql_query = query_chat_gpt(full_prompt)
    print(sql_query)
    result, headers = loader.query(sql_query)
    result = process_geospatial_data(result)
    result = populate_with_headers(result, headers)

    return result

def query_chat_gpt(prompt, json_output=False):
    payload = [{"role": "user", "content": prompt}]
    completion = openai.ChatCompletion.create(
                                            temperature=0,
                                            model=gpt_model,
                                            messages=payload
                                        )
    
    result = completion.choices[0].message.content
    if json_output:
        result = json.loads(result)
    return result

def process_geospatial_data(array):
    new_array = []
    for item in array:
        if type(item) == list or type(item) == tuple:
            new_array.append(process_geospatial_data(item))
        elif type(item) == str:
            if item.startswith("POLYGON") or item.startswith("MULTIPOLYGON"):
                p = shapely.wkt.loads(item)
                poly_mapped = mapping(p)
                poly_coordinates = poly_mapped['coordinates'][0]
                poly_ = [{'lat': coords[1],'lon': coords[0]} for coords in poly_coordinates]

                new_array.append(poly_)
            else:
                new_array.append(item)
        else:
            new_array.append(item)
    return new_array

def populate_with_headers(array, headers):
    output_array = []

    for line in array:
        obj = {}
        for value, header in zip(line, headers):
            obj[header] = value

        output_array.append(obj)

    return output_array
