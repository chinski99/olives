from olives import app, db
from flask import render_template, flash, redirect, session, url_for, request, g
import pandas as pd




@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    ol = pd.read_sql_table('olives', db.session.connection())
    desc = ol.describe()
    return render_template("index.html", ol_desc=desc)