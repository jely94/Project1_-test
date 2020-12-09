import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify, render_template

app = Flask(__name__)
engine = create_engine("sqlite:///data/happiness.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Happiness = Base.classes.happiness

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/happiness<br/>"
        f"/api/happiness1<br/>"
        f"/api/countries<br/>"
        f"/map<br/>"
        f"/scatter<br/>"
        f"/data<br/>"
    )

@app.route("/map")
def choropleth():
    return render_template("choropleth.html")

@app.route("/scatter")
def scatter():
    return render_template("scatter.html")

@app.route("/api/happiness")
def names():
    # Create our session (link) from Python to the DB
    #session = Session(engine)
    return jsonify(pd.read_sql_table("happiness", engine).to_json(orient="records"))


@app.route("/api/happiness1")
def cities():
    return pd.read_sql_table("happiness", engine).to_json(orient="records")

@app.route("/api/countries")
def countries():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all passengers
    results = session.query(Happiness.ISO2, Happiness.ISO3, Happiness.Country, Happiness.Region, Happiness.Score,
                                Happiness.GDP, Happiness.Social_Support, Happiness.Life_Exp, Happiness.Freedom_Choice,
                                 Happiness.Generosity, Happiness.Corruption, Happiness.Year).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_countries
    all_countries = []
    for ISO2, ISO3, Country, Region, Score, GDP, Social_Support, Life_Exp, Freedom_Choice, Generosity, Corruption, Year in results:
        countries_dict = {}
        countries_dict["ISO2"] = ISO2
        countries_dict["ISO3"] = ISO3
        countries_dict["Country"] = Country
        countries_dict["Region"] = Region
        countries_dict["Happiness_Score"] = Score
        countries_dict["GDP"] = GDP
        countries_dict["Social Support"] = Social_Support
        countries_dict["Life Expectancy"] = Life_Exp
        countries_dict["Freedom to Make Choices"] = Freedom_Choice
        countries_dict["Generosity"] = Generosity
        countries_dict["Corruption Perception"] = Corruption
        countries_dict["Year"] = Year
        all_countries.append(countries_dict)

    return jsonify(all_countries)

@app.route("/api/countries1")
def countries1():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all passengers
    results = session.query(Happiness).all()

    session.close()

    return jsonify(results)


@app.route("/data/<x>")
def pov(x):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all passengers
    results = session.query(Happiness.ISO2, Happiness.ISO3, Happiness.Country, Happiness.Region, Happiness.Score,
                                Happiness.GDP, Happiness.Social_Support, Happiness.Life_Exp, Happiness.Freedom_Choice,
                                 Happiness.Generosity, Happiness.Corruption, Happiness.Year).filter(Happiness.Year==x).all()
    print(results)

    session.close()

    # Create a dictionary from the row data and append to a list of all_countries
    all_countries = []
    for ISO2, ISO3, Country, Region, Score, GDP, Social_Support, Life_Exp, Freedom_Choice, Generosity, Corruption, Year in results:
        countries_dict = {}
        countries_dict["ISO2"] = ISO2
        countries_dict["ISO3"] = ISO3
        countries_dict["Country"] = Country
        countries_dict["Region"] = Region
        countries_dict["Happiness_Score"] = Score
        countries_dict["GDP"] = GDP
        countries_dict["Social Support"] = Social_Support
        countries_dict["Life Expectancy"] = Life_Exp
        countries_dict["Freedom to Make Choices"] = Freedom_Choice
        countries_dict["Generosity"] = Generosity
        countries_dict["Corruption Perception"] = Corruption
        countries_dict["Year"] = Year
        all_countries.append(countries_dict)

    return jsonify(all_countries)


if __name__ == "__main__":
    app.run(debug=True)