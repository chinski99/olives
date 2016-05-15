from olives import app, db
from flask import render_template, flash, redirect, session, url_for, request, g, make_response
import pandas as pd

from bokeh.plotting import figure
from bokeh.embed import components
import seaborn as sns
from bokeh import mpl
from olives import models


@app.route('/bokeh')
def bokeh():
    plot = figure()
    plot.circle([1, 2], [3, 4])
    script, div = components(plot)
    return render_template("bokeh.html", bsc=script, bdiv=div)


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    ol = pd.read_sql_table('olives', db.session.connection())
    desc = ol.describe()
    return render_template("index.html", ol_desc=desc)


@app.route('/violin')
def violin():
    tips = sns.load_dataset("tips")
    sns.set_style("whitegrid")
    ax = sns.violinplot(x="day", y="total_bill", hue="sex",
                        data=tips, palette="Set2", split=True,
                        scale="count", inner="stick")
    bh = mpl.to_bokeh()
    script, div = components(bh)
    return render_template("bokeh.html", bsc=script, bdiv=div)


# @app.route('/scatter/<int:acid1>/<int:acid2>')
# def scatter(acid1, acid2):
#     if acid2 is None or acid1 == acid2:  # histogram
#         tips = sns.load_dataset("tips")
#         sns.set_style("whitegrid")
#         ax = sns.violinplot(x="day", y="total_bill", hue="sex",
#                             data=tips, palette="Set2", split=True,
#                             scale="count", inner="stick")
#         bh = mpl.to_bokeh()
#         script, div = components(bh)
#         return render_template("bokeh.html", bsc=script, bdiv=div)
#     else:  # scatter
#         scatter = bk.Scatter(tips, x='palmitic', y='linolenic',
#                              color='region', marker='area_main',
#                              title='Iris Dataset Color and Marker by Species',
#                              legend=True)

@app.route('/multi.png')
def multiplot():
    data = models.prepare_multi()
    response = make_response(data.getvalue())
    response.mimetype = 'image/png'
    return response

@app.route('/multi')
def multi():
    return render_template("multi.html")