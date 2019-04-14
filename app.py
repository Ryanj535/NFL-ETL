##################################################
#Import Dependencies
##################################################
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import sqlite3


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///nfl_etl.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to the table
Stats = Base.classes.qb_stats2

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

#Create landing page with app route to the JSON document of quarterback data
@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.1/jsonified<br/>"
    )

#Create the rout for the JSON document of quarterback data
#Query the sqlite database quarterback table and return the stats in a JSON document
#Initnate session
#Query the database
#Create empty list and dictionaries to hold the database data
#Loop through the table and add the data to the lists and dictionary
#Zip the resulting list into a master dictionary of NFL quarterback 
#Convert the dinctionary to a JSON object and return it
@app.route("/api/v1.1/jsonified")
def quarterbacks():
    """Return a list of all quarterbacks and stats"""
    session = Session(engine)
    results = session.query(Stats.Player,Stats.Year_Drafted, Stats.Round_Drafted,
                            Stats.Overall_Pick, Stats.Draft_Position, 
                            Stats.Avg_Attempts, Stats.Avg_Completions, 
                            Stats.Avg_Passing_Yards, Stats.Avg_Yards_per_Attempt, 
                            Stats.Avg_TDs, Stats.Avg_Sacks, Stats.Avg_Loss_of_Yards,
                            Stats.Avg_QBR_REAL, Stats.Avg_Points, Stats.Game_Total ).all()

    player_names = []
    stats_list = []
    player_dict = {}

    for a in results:
        player_names.append(str(a[0]))

    for a,b,c,d,e,f,g,h,i,j,k,l,m,n,o in results:
        player_dict["Year_Drafted"] = b
        player_dict["Round_Drafted"] = c
        player_dict["Overall_Pick"] = d
        player_dict["Draft_Position"] = e
        player_dict["Avg_Attempts"] = f
        player_dict["Avg_Completions"] = g
        player_dict["Avg_Passing_Yards"] = h
        player_dict["Avg_Yards_per_Attempt"] = i
        player_dict["Avg_TDs"] = j
        player_dict["Avg_Sacks"] = k
        player_dict["Avg_Loss_of_Yards"] = l
        player_dict["Avg_QBR"] = m
        player_dict["Avg_Points"] = n
        player_dict["Game_Total"] = o
    
    
        stats_list.append(player_dict)
    nfl_dict = dict(zip(player_names,stats_list))
        
    return jsonify(nfl_dict)

if __name__ == '__main__':
    app.run(debug=True)