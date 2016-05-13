from olives import app, db
from flask import render_template, flash, redirect, session, url_for, request, g
import pandas as pd

from bokeh.plotting import figure
from bokeh.embed import components


@app.route('/bokeh')
def bokeh():
    plot = figure()
    plot.circle([1,2], [3,4])
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
    import seaborn as sns

    from bokeh import mpl
    from bokeh.plotting import output_file, show

    tips = sns.load_dataset("tips")

    sns.set_style("whitegrid")


    ax = sns.violinplot(x="day", y="total_bill", hue="sex",
                        data=tips, palette="Set2", split=True,
                        scale="count", inner="stick")


    output_file("seaborn_violin.html", title="seaborn_violin.py example")

    show(mpl.to_bokeh())
    script, div = components(mpl)
    return render_template("bokeh.html", bsc=script, bdiv=div)