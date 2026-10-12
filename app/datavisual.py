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

    fig, axes = plt.subplots(nrows=6,ncols=5,figsize=(16, 12))
    axes = axes.flatten()
    bins = bins or 50

    for ax, col in zip(axes, df1):
        xlim = np.percentile(pd.concat([df0[col],df1[col]]), [1, 99])
        bins_vec = np.linspace(*xlim, bins+1)
        ax.hist(df0[col], bins=bins_vec, alpha=0.5, label="not fraudulent")
        ax.hist(df1[col], bins=bins_vec, alpha=0.5, label="fraudulent")
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(col, fontsize=12, pad=2)

    fig.delaxes(axes[-1])
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
        sp.stats.probplot(sp.stats.zscore(df0[col]), dist="norm", fit=False, plot=ax)
        sp.stats.probplot(sp.stats.zscore(df1[col]), dist="norm", fit=False, plot=ax)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xlabel('')
        ax.set_ylabel('')
        ax.set_title(col, fontsize=12, pad=2)
        ax.get_lines()[0].set_markersize(1)
        ax.get_lines()[0].set_color('blue')
        ax.get_lines()[1].set_markersize(1)
        ax.get_lines()[1].set_color('red')
        ax.axline((0, 0), slope=1, color="black", linestyle="--")
        y0 = np.percentile(ax.get_lines()[0].get_ydata(), [0.1, 99.9])
        y1 = np.percentile(ax.get_lines()[1].get_ydata(), [0.1, 99.9])
        ax.set_ylim(min(y0[0], y1[0]), max(y0[1], y1[1]))
        x0 = np.percentile(ax.get_lines()[0].get_xdata(), [0.1, 99.9])
        x1 = np.percentile(ax.get_lines()[1].get_xdata(), [0.1, 99.9])
        ax.set_xlim(min(x0[0], x1[0]), max(x0[1], x1[1]))
            
    fig.delaxes(axes[-1])
    fig.delaxes(axes[-2])

    fig.legend(handles=[ax.get_lines()[0], ax.get_lines()[1]],
            labels=['not fraudulent', 'fraudulent'], loc=(0.75,0.08), fontsize=14, markerscale=3)
    plt.subplots_adjust(wspace=0.1, hspace=0.3)
    plt.savefig("plots/QQplots.png", bbox_inches="tight")


def scatterplot_matrix(engine: Engine):
    df0 = pd.read_sql(f"""SELECT {",".join(f"v{i}" for i in range(1, 29))},amount 
                            FROM fraud_data WHERE split = 'TRAIN' AND class=0 LIMIT 5000""", engine)
    df1 = pd.read_sql(f"""SELECT {",".join(f"v{i}" for i in range(1, 29))},amount 
                                FROM fraud_data WHERE split = 'TRAIN' AND class=1 LIMIT 5000""", engine)
    df0.rename(columns={"amount":"amt"},inplace=True)
    df1.rename(columns={"amount":"amt"},inplace=True)

    fig, axes = plt.subplots(nrows=29,ncols=29,figsize=(64, 64))
    for axes_x, col_x in zip(axes[:,],df0):
        for ax, col_y in zip(axes_x,df0):
            if col_x != col_y:
                ax.scatter(df0[col_x], df0[col_y],s=0.05, color='blue')
                ax.scatter(df1[col_x], df1[col_y],s=0.05, color='red')
                y0=np.percentile(df0[col_y], [1, 99])
                y1=np.percentile(df1[col_y], [1, 99])
                ax.set_ylim(min(y0[0], y1[0]), max(y0[1], y1[1]))
                x0=np.percentile(df0[col_x], [1, 99])
                x1=np.percentile(df1[col_x], [1, 99])
                ax.set_xlim(min(x0[0], x1[0]), max(x0[1], x1[1]))
            else:
                ax.text(0.5, 0.5, col_x, fontsize=40,
                        transform=ax.transAxes,
                        ha='center', va='center')
            ax.set_xticks([])
            ax.set_yticks([])

    plt.subplots_adjust(wspace=0.05, hspace=0.05)
    plt.savefig("plots/scatterplots.png", bbox_inches="tight")