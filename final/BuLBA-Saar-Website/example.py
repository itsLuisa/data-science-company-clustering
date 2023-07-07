# coding: utf-8

from flask import Flask, render_template, request
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map, icons
import pandas as pd
#from dynaconf import FlaskDynaconf

app = Flask(__name__, template_folder="templates")
#FlaskDynaconf(app)  # will read GOOGLEMAPS_KEY from .secrets.toml


# you can set key as config
app.config['GOOGLEMAPS_KEY'] = ""

# you can also pass key here
GoogleMaps(
    app
)

# NOTE: this example is using a form to get the apikey


@app.route("/",methods=['POST','GET'])
def mapview():
    
    selected_domains = request.form.getlist('domains[]')
    print(selected_domains)
    selected_size = request.form.getlist('size[]')
    print(selected_size)
    selected_rating = request.form.getlist('rating[]')
    selected_rating = [float(r) for r in selected_rating]
    print(selected_rating)

    df = pd.read_csv('Saar-dex.csv', encoding='utf-8')
    domains = df["industry"].unique()
    size = df["size"].unique()
    rating = df["rating"].unique()

    markers_colors = [
        '//maps.google.com/mapfiles/ms/icons/blue-dot.png',
        '//maps.google.com/mapfiles/ms/icons/yellow-dot.png',
        '//maps.google.com/mapfiles/ms/icons/green-dot.png',
        '//maps.google.com/mapfiles/ms/icons/red-dot.png',
        '//maps.google.com/mapfiles/ms/icons/pink-dot.png'

    ]

    import random

    colors = {k:markers_colors[i] for i,k in enumerate(selected_domains)}

    legends = [(colors[k],k) for k in colors]


    # for k in domains:
    #     if k in colors:
    #         print(k)
    df2 = df
    if selected_size != []:
        df2 = df[df["size"].isin(selected_size)]
    if selected_rating != []:
        df2 = df2[df2["rating"].isin(selected_rating)]

    markers = {
    colors[k]:[(row["lat"],row["lng"],f"""<h3>{row["company_name"]}</h3>""") for _,row in df2[df2["industry"]==k].iterrows()] for k in df2["industry"] if k in colors
    }
    print(markers)

    circle = {
        "stroke_color": "#FF00FF",
        "stroke_opacity": 0.7,
        "stroke_weight": 1,
        "fill_color": "#FF00FF",
        "fill_opacity": 0.7,
        "center": {"lat": 49.2382, "lng": 6.9975},
        "radius": 2000,
        "infobox": f"""<h3>This is where you should build your company!</h3><h3>ToDo (our next feature to add to the website)</h3>""",
    }

    sndmap = Map(
        identifier="sndmap",
        varname="sndmap",
        # style=(
        #     "height:100%;"
        #     "width:100%;"
        #     "top:0;"
        #     "left:0;"
        #     "position:absolute;"
        #     # "overflow: hidden;"
        #     # "margin: 0 auto;"
        #     "z-index:200;"
        # ),
        lat=49.2382,#37.4419,
        lng=6.9975,#122.1419,
        zoom=10,
        markers=markers,
        circles=[circle]
        # {
        #     icons.dots.green: [(37.4419, -122.1419), (37.4500, -122.1350)],
        #     icons.dots.blue: [(37.4300, -122.1400, "Hello World")],
        # },
    )


    return render_template(
        "example.html",
        sndmap=sndmap,
        domains=domains,
        selected_domains = selected_domains,
        size=size,
        selected_size = selected_size,
        rating=rating,
        selected_rating = selected_rating,
        legends=legends,

        GOOGLEMAPS_KEY=request.args.get("apikey"),
    )



if __name__ == "__main__":
    app.run(port=5050, debug=True, use_reloader=True)
