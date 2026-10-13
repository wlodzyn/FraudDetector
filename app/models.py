import numpy as np
import pandas as pd
from sqlalchemy.engine import Engine
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV, PredefinedSplit
from sklearn.metrics import accuracy_score


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

    
    param_grid = {
        "C": [0.01, 0.1, 1, 10, 100],
        "max_iter": [10000],
        "solver": ["saga"],
        "l1_ratio": [0,1]
    }

    grid = GridSearchCV(LogisticRegression(), param_grid, cv=ps, scoring="accuracy")
    grid.fit(x, y)
    print(grid.best_params_)
    print(grid.best_score_)
    y_pred = grid.best_estimator_.predict(x_test)
    test_accuracy = accuracy_score(y_test, y_pred)
    print("Test accuracy:", test_accuracy)
