import mysql.connector
import kagglehub
from dotenv import load_dotenv
import os
import numpy as np

def initialize_data(seed: np.int32 | None):

    db = mysql.connector.connect(
                    host="mysql",
                    port=3306,
                    database="FraudData",
                    user=os.getenv("DB_USER"),
                    password=os.getenv("DB_PASSWORD"),
                    allow_local_infile=True
                )
    cursor = db.cursor()
    
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS fraud_data (
        id INT PRIMARY KEY,
        {",".join(f"v{i} FLOAT NOT NULL" for i in range(1, 29))},
        amount FLOAT NOT NULL,
        class BOOL NOT NULL,
        split ENUM('TRAIN','VALIDATE','TEST') DEFAULT NULL
        );""")
    cursor.execute("TRUNCATE TABLE fraud_data;")
    
    path = "./data"
    filename = "/creditcard_2023.csv"
    dataset_path="nelgiriyewithana/credit-card-fraud-detection-dataset-2023"
    load_dotenv()
    kagglehub.dataset_download(dataset_path, output_dir=path)
    if not os.path.isfile(path+filename):
        print("error: data were not download from Kaggle")
        raise SystemExit(1)
    
    cursor.execute(f"""
        LOAD DATA LOCAL INFILE '{path+filename}'
        INTO TABLE fraud_data
        FIELDS TERMINATED BY ','
        IGNORE 1 ROWS
        ;""")

    cursor.execute("SELECT COUNT(*) FROM fraud_data")
    table_size = cursor.fetchone()[0]


    cursor.execute(f"""
        UPDATE fraud_data
        SET split = 'TRAIN'
        ORDER BY RAND({seed if seed is not None else ''})
        LIMIT {int(table_size*0.9)}
        ;""")          

    cursor.execute(f"""
        UPDATE fraud_data
        SET split = 'VALIDATE'
        WHERE split IS NULL
        ORDER BY RAND({seed if seed is not None else ''})
        LIMIT {int(table_size*0.05)}
        ;""")

    cursor.execute("""
        UPDATE fraud_data
        SET split = 'TEST'
        WHERE split IS NULL
        ;""")

    db.commit()
    cursor.close()
    db.close()