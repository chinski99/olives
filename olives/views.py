from olives import app, db, models, forms
from flask import render_template, make_response, request
import pandas as pd
from bokeh.embed import components


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    desc = models.get_description()
    means = models.get_means()
    return render_template("index.html", ol_desc=desc, means=means)


@app.route('/violin/<acid>')
def violin(acid):
    bh = models.acid_violin(acid)
    script, div = components(bh)
    return render_template("bokeh.html", bsc=script, bdiv=div)


@app.route('/scatter', methods=['post', 'get'])
def scatter():
    form = forms.AcidSelForm()
    if request.method == 'POST':
        acid1 = form.acid1.data
        acid2 = form.acid2.data
        if acid1 == acid2:
            bh = models.acid_histogram(acid1)
        else:
            bh = models.acid_scatter(acid1, acid2)
        script, div = components(bh)
        return render_template("cross.html", form=form, bsc=script, bdiv=div)
    return render_template('cross.html', form=form)


@app.route('/multi.png')
def multiplot():
    data = models.prepare_multi()
    response = make_response(data.getvalue())
    response.mimetype = 'image/png'
    return response


@app.route('/multi')
def multi():
    return render_template("multi.html")


@app.route('/tree')
def tree():
    models.prepare_tree_visualization()
    return render_template("tree.html")


@app.context_processor
def acid_list():
    return dict(acids=models.get_acids())
