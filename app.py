import numpy as np
import pandas as pd
import datetime

import sqlalchemy 
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

Measurements = Base.classes.measurement
Stations = Base.classes.station

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def HomePage():
    return (
        f"Welcome to the Climate App Home Page<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations</br>"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the JSON representation of Precipitation Dictionary"""

    session = Session(engine)
    results = session.query(Measurements.id, Measurements.station, Measurements.date, Measurements.prcp, Measurements.tobs).\
    order_by(Measurements.date.desc()).all()

    most_recent = [result[2] for result in results]
    most_recent = most_recent[0]
    compare_date = datetime.datetime.strptime(most_recent, '%Y-%m-%d') - datetime.timedelta(days=365)
    compare_date = compare_date.strftime('%Y-%m-%d')

    sel = [Measurements.date, func.avg(Measurements.prcp)]
    yearly_precip = session.query(*sel).\
    filter(Measurements.date <= most_recent).\
    filter(Measurements.date >= compare_date).\
    group_by(Measurements.date).\
    order_by(Measurements.date.asc()).all()
    
    precip_dict = {}
    for date, temp in yearly_precip:
        precip_dict.update({date: temp})
                
    return jsonify(precip_dict)

@app.route("/api/v1.0/stations")
def stations():
    """Return the JSON list of stations from the dataset"""
    return jsonify(stations_list)
  
@app.route("/api/v1.0/tobs")
def tobs():
    """Return the JSON list of temperature observations"""
    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def start():
    """Return JSON dictionary of min, max, avg temps for all dates greater than start date"""
    return jsonify(start_temps_dict)

@app.route("/api/v1.0/<start>/<end>")
def start_end():
    """Return JSON dictionary of min, max & avg temps between start & end dates"""
    return jsonify(inclusive_dict)





if __name__ == "__main__":
    app.run(debug=True)
