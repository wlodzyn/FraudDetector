import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

def histograms(engine: Engine, bins: np.uint32 | None):
    df = pd.read_sql(f"""SELECT {",".join(f"v{i}" for i in range(1, 29))},amount 
                        FROM fraud_data WHERE split = 'TRAIN'""", engine)

    axes = df.hist(grid=False,bins=(bins or 50),figsize=(16, 12)).flatten()
    for ax in axes:
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(ax.get_title(), fontsize=12, pad=2)
    plt.subplots_adjust(wspace=0.1, hspace=0.3)
    plt.savefig("plots/histograms.png", bbox_inches="tight")

def qqplots(engine: Engine):
    df = pd.read_sql(f"""SELECT {",".join(f"v{i}" for i in range(1, 29))} 
                            FROM fraud_data WHERE split = 'TRAIN' LIMIT 1000""", engine)
    fig, axes = plt.subplots(nrows=6,ncols=5,figsize=(16, 12))
    axes = axes.flatten()

    for ax, col in zip(axes, df):
        sp.stats.probplot(df[col], dist="norm", plot=ax)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xlabel('')
        ax.set_ylabel('')
        ax.set_title(col, fontsize=12, pad=2)
        ax.get_lines()[0].set_markersize(2)
            
    fig.delaxes(axes[-1])
    fig.delaxes(axes[-2])

    plt.subplots_adjust(wspace=0.1, hspace=0.3)
    plt.savefig("plots/QQplots.png", bbox_inches="tight")



def single_feature_dependence():
    pass


def two_features_corr():
    pass