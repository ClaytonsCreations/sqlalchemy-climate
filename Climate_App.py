import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

#Flask Setup
app = Flask(__name__)

#Flask Routes

@app.route("/")
def welcome():
	return(
		f'Available Routes:<br/>'
		f'/api/v1.0/precipitation<br/>'
		f'/api/v1.0/stations<br/>'
		f'/api/v1.0/tobs<br/>'
		f'/api/v1.0/<start>/<end>'
		)

@app.route("/api/v1.0/precipitation")
def precipitation():
	session = Session(engine)

	precip = session.query(Measurement.prcp, Measurement.date).all()

	session.close()

	prcp_all = []
	for prcp, date in precip:
		precipitation_dict = {}
		precipitation_dict['precipitation'] = prcp
		precipitation_dict['date'] = date
		prcp_all.append(precipitation_dict)

	return jsonify(prcp_all)


@app.route("/api/v1.0/stations")
def stations():
	session = Session(engine)

	station_list = session.query(Station.station, Station.name).all()

	session.close()

	all_stations = list(np.ravel(station_list))

	return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
	session = Session(engine)

	twelve_months = '2016-08-23'
	active_station	= 'USC00519281'

	temps = session.query(Measurement.date, Measurement.tobs).\
		filter(Measurement.date >= twelve_months).\
		filter(Measurement.station == active_station).all()

	temps_all = []
	for date, tobs in temps:
		temps_dict = {}
		temps_dict['date'] = date
		temps_dict['tobs'] = tobs
		temps_all.append(temps_dict)

	session.close()

	return jsonify(temps_all)


@app.route("/api/v1.0/<start>")
def start(start):
	session = Session(engine)

	start_date = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
		filter(Measurement.date >= start).all()

	start_date = list(np.ravel(start_date, order='C'))

	session.close()
	 
	return jsonify(start_date)
    
   



@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
	session = Session(engine)

	start_end_dates = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
		filter(Measurement.date >= start).\
		filter(Measurement.date <= end).all()

	start_end_dates = list(np.ravel(start_end_dates, order='C'))

	session.close()

	return jsonify(start_end_dates)

if __name__ == '__main__':
    app.run(debug=True)