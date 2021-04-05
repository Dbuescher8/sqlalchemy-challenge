import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify 


#####################################################
# Database Setup
####################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
         f"List of Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    results1 = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date>="2016-08-23").all()
    first_dict = list(np.ravel(results1))
#  Convert the query results to a Dictionary using `date` as the key and `tobs` as the value.
    first_dict = []
    for temps in results1:
        temps_dict = {}
        temps_dict["date"] = Measurement.date
        temps_dict["tobs"] = Measurement.tobs
        first_dict.append(temps_dict)

#  Return the JSON representation of your dictionary.
    return jsonify(first_dict)

@app.route("/api/v1.0/stations")
def stations():
    results2 = session.query(Station.station, Station.name).all()

    sec_dict = list(np.ravel(results2))
# # #  Convert the query results to a Dictionary.
    sec_dict = []
    for sta in results2:
        station_dict = {}
        station_dict["station"] = Station.station
        station_dict["name"] = Station.name
        sec_dict.append(station_dict)

# # #  Return the JSON representation of your dictionary.

    return jsonify(sec_dict)

@app.route("/api/v1.0/<start_date>")
def Start_date(start_date):
 session = Session(engine)

results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start_date).all()

  # Get a list of column names and types
columns = inspector.get_columns('measurement')
for c in columns:
    print(c['name'], c["type"])
# columns


# Get a list of column names and types
columns = inspector.get_columns('station')
for c in columns:
    print(c['name'], c["type"])
# columns
    session.close()

results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

start_end_tobs = []
for min, avg, max in results:
    start_end_tobs_dict = {}
    start_end_tobs_dict["min_temp"] = min
    start_end_tobs_dict["avg_temp"] = avg
    start_end_tobs_dict["max_temp"] = max
    start_end_tobs.append(start_end_tobs_dict) 

if __name__ == "__main__":
app.run(debug=True)
