import numpy as np
import pandas as pd
import datetime

import sqlalchemy 
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

from flask import request, render_template

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

Measurements = Base.classes.measurement
Stations = Base.classes.station

session = Session(engine)

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
        f"/api/v1.0/tobs</br>"
        f"/api/v1.0/start_date</br>"
        f"/api/v1.0/start_end_date</br>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the JSON representation of Precipitation Dictionary"""

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
        precip_dict.update({date:temp})

    session.close()    
    return jsonify(precip_dict)

@app.route("/api/v1.0/stations")
def stations():
    """Return the JSON list of stations from the dataset"""

    results = session.query(Stations.station).all()
    stations_list = list(np.ravel(results))

    session.close()
    return jsonify(stations_list)
  
@app.route("/api/v1.0/tobs")
def tobs():
    """Return the JSON list of temperature observations"""
    
    results = session.query(Measurements.date, Measurements.station, Measurements.tobs).\
        order_by(Measurements.date.desc()).all()
   
    most_recent = [result[0] for result in results]
    most_recent = most_recent[0]
    compare_date = datetime.datetime.strptime(most_recent, '%Y-%m-%d') - datetime.timedelta(days=365)
    compare_date = compare_date.strftime('%Y-%m-%d')

    sel = [Measurements.station, func.count(Measurements.station)]
    active_stations = session.query(*sel).\
    group_by(Measurements.station).\
    order_by(func.count(Measurements.station).desc()).all()

    most_active_station = active_stations[0][0]

    sel = [Measurements.station, Measurements.date, Measurements.tobs]
    temps = session.query(*sel).\
    filter(Measurements.date <= most_recent).\
    filter(Measurements.date >= compare_date).\
    filter(Measurements.station == most_active_station).\
    order_by(Measurements.date.asc()).all()
    
    tobs_list = []
    for temp in temps:
        tobs_list.append(temp[2])

    session.close()
    return jsonify(tobs_list)

@app.route("/api/v1.0/start_date")
def start():
    
    """Return JSON dictionary of min, max, avg temps for all dates equal to start date"""
    start_date = datetime.datetime.strptime('2017-07-04', '%Y-%m-%d').date()
    
    sel = [Measurements.date, func.max(Measurements.tobs), func.min(Measurements.tobs), func.avg(Measurements.tobs)]
    temps = session.query(*sel).\
    filter(Measurements.date == start_date).all()    
       
    for a,b,c,d in temps:
        m_date = a
        max = b
        min = c
        avg = d

    start_dict = {'Maximum_Temperature': max, 'Minimum_Temperature': min, 'Average_Temperature': avg}

    session.close()
    return jsonify(start_dict)

@app.route("/api/v1.0/start_end_date")
def start_end():
    """Return JSON dictionary of min, max & avg temps between start & end dates"""
    start_date = datetime.datetime.strptime('2016-07-04', '%Y-%m-%d').date()
    end_date = datetime.datetime.strptime('2017-07-04', '%Y-%m-%d').date()
    
    results = session.query(Measurements.date, Measurements.station, Measurements.tobs).\
        order_by(Measurements.date.desc()).all()
   
    sel = [Measurements.date, func.max(Measurements.tobs), func.min(Measurements.tobs), func.avg(Measurements.tobs)]
    temps = session.query(*sel).\
    filter(Measurements.date >= start_date).\
    filter(Measurements.date <= end_date).all()    
       
    for a,b,c,d in temps:
        m_date = a
        max = b
        min = c
        avg = round(d,2)

    inclusive_dict = {'Maximum_Temperature': max, 'Minimum_Temperature': min, 'Average_Temperature': avg}

    session.close()
    return jsonify(inclusive_dict)

if __name__ == "__main__":
    app.run(debug=True)
