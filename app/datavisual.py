import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

def histograms(engine: Engine, bins: np.uint32 | None):
    df0 = pd.read_sql(f"""SELECT {",".join(f"v{i}" for i in range(1, 29))},amount 
                        FROM fraud_data WHERE split = 'TRAIN' AND class = 0""", engine)
    df1 = pd.read_sql(f"""SELECT {",".join(f"v{i}" for i in range(1, 29))},amount 
                        FROM fraud_data WHERE split = 'TRAIN' AND class = 1""", engine)

    print(df0.shape[0],df1.shape[0])

    axes = df0.hist(grid=False,bins=(bins or 50),figsize=(16, 12), alpha=0.5, label="not fraudulent").flatten()
    for ax, col in zip(axes, df1):
        df1[col].hist(grid=False,bins=(bins or 50),figsize=(16, 12), alpha=0.5, label="fraudulent", ax=ax)
        for patch in ax.patches:
            patch.set_height(patch.get_height()/patch.get_width())
        ax.relim()
        ax.autoscale_view()
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(ax.get_title(), fontsize=12, pad=2)

    fig = axes[0].get_figure()
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc=(0.79,0.08), fontsize=14, markerscale=3)
    plt.subplots_adjust(wspace=0.1, hspace=0.3)
    plt.savefig("plots/histograms.png", bbox_inches="tight")


def qqplots(engine: Engine):
    df0 = pd.read_sql(f"""SELECT {",".join(f"v{i}" for i in range(1, 29))} 
                        FROM fraud_data WHERE split = 'TRAIN' AND class = 0""", engine)
    df1 = pd.read_sql(f"""SELECT {",".join(f"v{i}" for i in range(1, 29))} 
                        FROM fraud_data WHERE split = 'TRAIN' AND class = 1""", engine)

    fig, axes = plt.subplots(nrows=6,ncols=5,figsize=(16, 12))
    axes = axes.flatten()

    for ax, col in zip(axes, df0):
        sp.stats.probplot(sp.stats.zscore(df0[col]), dist="norm", plot=ax)
        sp.stats.probplot(sp.stats.zscore(df1[col]), dist="norm", plot=ax)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xlabel('')
        ax.set_ylabel('')
        ax.set_title(col, fontsize=12, pad=2)
        ax.get_lines()[0].set_markersize(1.5)
        ax.get_lines()[0].set_color('blue')
        ax.get_lines()[1].set_color('black')
        ax.get_lines()[2].set_markersize(1.5)
        ax.get_lines()[2].set_color('red')
        ax.get_lines()[3].set_color('black')
            
    fig.delaxes(axes[-1])
    fig.delaxes(axes[-2])

    fig.legend(handles=[ax.get_lines()[0], ax.get_lines()[2]],
            labels=['not fraudulent', 'fraudulent'], loc=(0.75,0.08), fontsize=14, markerscale=3)
    plt.subplots_adjust(wspace=0.1, hspace=0.3)
    plt.savefig("plots/QQplots.png", bbox_inches="tight")


def two_features_corr():
    pass