import pandas as pd
from olives import db
import matplotlib.pyplot as plt
from io import BytesIO
import seaborn as sns


def prepare_multi():
    olives = pd.read_sql('olives', db.engine)
    acid_list = list(olives.columns.values)[-8:]
    regions = list(olives['area_main'].unique())
    pp = sns.pairplot(olives, vars=acid_list, hue="region", size=3, palette="Set2", diag_kind="kde")
    figdata = BytesIO()
    pp.savefig(figdata,format='png')
    plt.close("all")
    return figdata

