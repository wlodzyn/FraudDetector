from argparse import ArgumentParser
import mysql.connector
from sqlalchemy import create_engine
import os
import numpy as np
import pandas as pd
import datainit
import datavisual

def help_message():
    print("""Commands list:
    help - print this message
    init [<seed>] - initialize data from Kaggle
    histo [<bins>] - create histograms for features
    qqplot - create Q-Q plots for features""")

if __name__ == "__main__":
    
    engine = create_engine(f"mysql+mysqlconnector://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@mysql:3306/FraudData")
    
    parser = ArgumentParser()
    parser.add_argument('command', type=str, 
        choices=['help','init','histo','qqplot'])
    parser.add_argument("number", type=np.int32, nargs="?")
    args = parser.parse_args()

    if args.command == 'help':
        help_message()
    elif args.command == 'init':
        datainit.initialize_data(args.number)
    elif args.command == 'histo':
        datavisual.histograms(engine,args.number)
    elif args.command == 'qqplot':
        datavisual.qqplots(engine)