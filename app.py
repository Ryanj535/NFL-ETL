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

@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/jsonified<br/>"
    )


@app.route("/api/v1.0/jsonified")
def stations():
    """Return a list of all stations"""
    session = Session(engine)
    results = session.query(Stats.Player,Stats.Year_Drafted, Stats.Round_Drafted,
                            Stats.Overall_Pick, Stats.Draft_Position, 
                            Stats.Avg_Attempts, Stats.Avg_Completions, 
                            Stats.Avg_Passing_Yards, Stats.Avg_Yards_per_Attempt, 
                            Stats.Avg_TDs, Stats.Avg_Sacks, Stats.Avg_Loss_of_Yards,
                            Stats.Avg_QBR_REAL, Stats.Avg_Points, Stats.Game_Total ).all()

    stats_list =[]
    for a,b,c,d,e,f,g,h,i,j,k,l,m,n,o in results:
        stats_dict = {}
        stats_dict["Player"] = a
        stats_dict["Year_Drafted"] = b
        stats_dict["Round_Drafted"] = c
        stats_dict["Overall_Pick"] = d
        stats_dict["Draft_Position"] = e
        stats_dict["Avg_Attempts"] = f
        stats_dict["Avg_Completions"] = g
        stats_dict["Avg_Passing_Yards"] = h
        stats_dict["Avg_Yards_per_Attempt"] = i
        stats_dict["Avg_TDs"] = j
        stats_dict["Avg_Sacks"] = k
        stats_dict["Avg_Loss_of_Yards"] = l
        stats_dict["Avg_QBR"] = m
        stats_dict["Avg_Points"] = n
        stats_dict["Game_Total"] = o
        stats_list.append(stats_dict)
        
    return jsonify(stats_list)

@app.route("/search", methods=['GET','POST'])
def search():
    session = Session(engine)
    results = session.query(Stats.Player,Stats.Year_Drafted, Stats.Round_Drafted,
                            Stats.Overall_Pick, Stats.Draft_Position, 
                            Stats.Avg_Attempts, Stats.Avg_Completions, 
                            Stats.Avg_Passing_Yards, Stats.Avg_Yards_per_Attempt, 
                            Stats.Avg_TDs, Stats.Avg_Sacks, Stats.Avg_Loss_of_Yards,
                            Stats.Avg_QBR_REAL, Stats.Avg_Points, Stats.Game_Total ).filter(Stats.Year_Drafted==year_selected).all()
    return render_template("search.html", )

if __name__ == '__main__':
    app.run(debug=True)