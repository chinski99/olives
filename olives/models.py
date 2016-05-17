import pandas as pd
from olives import db
import matplotlib.pyplot as plt
from io import BytesIO
import seaborn as sns
import bokeh.charts as bk
from bokeh import mpl
from sklearn.cross_validation import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_graphviz
import os
import subprocess


def prepare_multi():
    olives = pd.read_sql('olives', db.engine)
    acid_list = list(olives.columns.values)[-8:]
    regions = list(olives['area_main'].unique())
    pp = sns.pairplot(olives, vars=acid_list,
                      hue="region",
                      size=3,
                      palette="Set2",
                      diag_kind="kde")
    figdata = BytesIO()
    pp.savefig(figdata, format='png')
    plt.close("all")
    return figdata


def get_acids():
    olives = pd.read_sql('olives', db.engine)
    acid_list = list(olives.columns.values)[-8:]
    return acid_list


def acid_violin(acid):
    olives = pd.read_sql('olives', db.engine, columns=['region', 'area_main', acid])
    sns.set_style("whitegrid")
    sns.mpl.rc("figure", figsize=(15, 6))
    ax = sns.violinplot(data=olives,
                        x="area_main",
                        y=acid,
                        cut=0.1,
                        scale='count',
                        title=acid + " acid distribution")
    bh = mpl.to_bokeh(ax.figure)
    return bh


def acid_histogram(acid):
    olives = pd.read_sql('olives', db.engine, columns=[acid, 'area_main'])
    hist = bk.Histogram(olives, values=acid,
                        title="Acids by area",
                        color='area_main',
                        legend='top_right',
                        agg='count',
                        bins=10)
    return hist


def acid_scatter(acid1, acid2):
    olives = pd.read_sql('olives', db.engine, columns=['area_main', 'region', acid1, acid2])
    scatter = bk.Scatter(olives, x=acid1, y=acid2,
                         color='region', marker='area_main',
                         title='Cross-acid comparison',
                         legend='top_right')
    return scatter


def get_description():
    ol = pd.read_sql_table('olives', db.engine)
    desc = ol.describe()
    return desc


def get_means():
    ol = pd.read_sql_table('olives', db.engine)
    desc = ol.groupby('area_main').mean()
    desc = desc.drop(desc.columns[[0, 1, 2]], axis=1)
    cm = sns.light_palette("green", as_cmap=True)
    s = desc.style.background_gradient(cmap=cm)
    s = s.set_properties(**{'cellpadding': '30',
                            'border-color': 'white'})
    return s.render()


def train_decision_tree(dataset, features, explained):
    train, test = train_test_split(dataset, test_size=0.2)
    dt = DecisionTreeClassifier(min_samples_split=20, random_state=99)
    fitresult = dt.fit(train[features], train[explained])
    return dt


def visualize_tree(tree, acids, regions):  # this is a hack at this point
    my_dir = os.path.dirname(__file__)
    dot_file_path = os.path.join(my_dir, 'static/images/dt.dot')
    png_file_path = os.path.join(my_dir, 'static/images/dt.png')
    with open(dot_file_path, 'w') as f:
        export_graphviz(tree, out_file=f,
                        feature_names=acids,
                        class_names=regions,
                        filled=True, rounded=True,
                        special_characters=True)

    my_env = os.environ.copy()
    my_env["PATH"] = "/usr/local/bin:/usr/bin:" + my_env["PATH"]
    command = ["dot", "-Tpng", dot_file_path, "-o", png_file_path]
    try:
        subprocess.check_call(command, env=my_env)
    except:
        print("Could not run dot, ie graphviz, to produce visualization")


def prepare_tree_visualization():
    olives = pd.read_sql('olives', db.engine)
    acid_list = list(olives.columns.values)[-8:]
    regions = list(olives['area_main'].unique())
    tree = train_decision_tree(olives, acid_list, 'area_main')
    visualize_tree(tree, acid_list, regions)
