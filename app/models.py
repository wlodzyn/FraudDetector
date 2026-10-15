import numpy as np
import pandas as pd
from sqlalchemy.engine import Engine
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV, PredefinedSplit
from sklearn.metrics import accuracy_score
from sklearn.metrics import ConfusionMatrixDisplay
import matplotlib.pyplot as plt


def logistic_regression(engine: Engine):
    df_train = pd.read_sql(f"""SELECT * FROM fraud_data 
                WHERE split IN ('TRAIN', 'VALIDATE');""", engine)
    df_test = pd.read_sql(f"""SELECT * FROM fraud_data 
                    WHERE split='TEST';""", engine)

    x = df_train.drop(columns=['split','class'])
    y = df_train.loc[:,['class']].squeeze()
    test_fold = np.where(df_train['split']=='TRAIN',-1,0)
    ps = PredefinedSplit(test_fold)
    x_test = df_test.drop(columns=['split','class'])
    y_test = df_test.loc[:,['class']].squeeze()

    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("model", LogisticRegression())
    ])

    param_grid = {
        "model__C": [0.01, 0.1, 1, 10, 100],
        "model__max_iter": [10000],
        "model__solver": ["sag"],
        "model__l1_ratio": [0]
    }
    grid = GridSearchCV(pipeline, param_grid, cv=ps, scoring="accuracy")
    grid.fit(x, y)
    y_pred = grid.best_estimator_.predict(x_test)
    test_accuracy = accuracy_score(y_test, y_pred)

    file_path = "./results/logistic_regression_bestfit.dat"
    file = open(file_path,'w')
    file.write(str(grid.best_params_)+'\n')
    file.write(f"Validation accuracy: {grid.best_score_}\n")
    file.write(f"Test accuracy: {test_accuracy}\n")
    file.close()

    ConfusionMatrixDisplay.from_predictions(y_test, y_pred, colorbar=False, text_kw={"fontsize": 20})
    plt.savefig("results/confusion_matrix.png")
