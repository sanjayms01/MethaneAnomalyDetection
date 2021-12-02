from flask import Flask, jsonify, request
from flask_cors import CORS

import altair as alt

#Local Imports
from explore import get_data_shape, get_bar_zone_split, \
                    get_feature_dashboard, get_vista_ca_dashboard, \
                    get_missing_data_dashboard

from product import get_anomaly_df, get_recent_line_chart, get_product_line_chart, get_methane_map, get_recent_tweets, is_in_california

from patternPrint import printDiamond
from classes.dataLoader import DataLoader
from classes.chartLoader import ChartLoader

app = Flask(__name__)
CORS(app)

alt.data_transformers.disable_max_rows()

### Pre-Defined Loaders
DL = DataLoader()
CL = ChartLoader(DL)

zone_id_list = DL.cl_gdf['BZone'].tolist()
region_poly_list = DL.cl_gdf['geometry'].tolist()

printDiamond("READY TO SERVE")

### TEST ROUTE ###

@app.route("/")
def route_homepage():
    return jsonify({"zone": get_data_shape(DL.df_zone),
                    "all" : get_data_shape(DL.df_all),
                    "climate_zones" : get_data_shape(DL.cl_gdf),
                    "ca_geo": get_data_shape(DL.ca_gdf),
                    "non_oil_df" : get_data_shape(DL.non_oil_df),
                    "miss_time": get_data_shape(DL.miss_time),
                    "all_dates_df": get_data_shape(DL.all_dates_df),
                    })


@app.route("/get_date_range")
def route_get_date_range():
    return jsonify({'dates': DL.get_date_range()})


### EXPLORE ROUTES ###

@app.route("/get_bar_zone_split")
def route_get_bar_zone_split():
    return jsonify({"chart": get_bar_zone_split(DL.df_all)})

@app.route("/get_feature_dashboard")
def route_get_feature_dashboard():
    time_feature = request.args.get("tfeat")
    bar_feature = request.args.get("bfeat")
    return jsonify({"chart": get_feature_dashboard(DL, time_feature, bar_feature)})

@app.route("/get_vista_ca_dashboard")
def route_get_vista_ca_dashboard():
    return jsonify({"chart": get_vista_ca_dashboard(DL)})

@app.route("/get_missing_data_dashboard")
def route_get_missing_data_dashboard():
    resolution = request.args.get("reso")
    resolution = "Zone" if resolution == "Zone" else float(resolution)
    
    freq = request.args.get("freq")
    return jsonify({"chart": get_missing_data_dashboard(DL, CL, resolution, freq)})

@app.route("/get_missing_data_line")
def route_get_missing_data_line():
    return jsonify({"chart": CL.missing_data_line_chart.to_json()})



### PRODUCT ROUTES ###
@app.route("/get_location_check")
def route_get_location_check():
    lat = float(request.args.get('lat'))
    lng = float(request.args.get('lng'))
    return jsonify({"result": is_in_california(DL, lat, lng, zone_id_list, region_poly_list)})

@app.route("/get_anomaly_df")
def route_get_anomaly_df():
    z = int(request.args.get('zone'))
    return jsonify({"table": get_anomaly_df(DL, z)})

@app.route("/get_recent_line_chart")
def route_get_recent_line_chart():
    z = int(request.args.get('zone'))
    return jsonify({"chart": get_recent_line_chart(DL, z)})

@app.route("/get_product_line_chart")
def route_get_product_line_chart():
    z = int(request.args.get('zone'))
    return jsonify({"chart": get_product_line_chart(DL, z)})

@app.route("/get_methane_map")
def route_get_methane_map():
    z = int(request.args.get('zone'))
    return jsonify({"chart": get_methane_map(DL, z)})

@app.route("/get_recent_tweets")
def route_get_recent_tweets():
    return get_recent_tweets()

if __name__ == "__main__":
    app.run(host='0.0.0.0')
