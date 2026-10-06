from argparse import ArgumentParser
import mysql.connector
from sqlalchemy import create_engine
import os
import numpy as np
import datainit

def help_message():
    print("""Commands list:
    help - print this message
    init [<seed>] - initialize data from Kaggle""")

if __name__ == "__main__":
    
    engine = create_engine(f"""mysql+mysqlconnector://
    {os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}
    @mysql:3306/FraudData""")
    
    parser = ArgumentParser()
    parser.add_argument('command', type=str, 
        choices=['help','init','drop'])
    parser.add_argument("seed", type=np.int32, nargs="?")
    args = parser.parse_args()

    if args.command == 'help':
        help_message()
    elif args.command == 'init':
        datainit.initialize_data(args.seed)