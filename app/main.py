from argparse import ArgumentParser
import mysql.connector
import os
import datainit

def help_message():
    print("""Commands list:
    help - print this message
    init - initialize data from Kaggle
    drop - remove data""")

if __name__ == "__main__":
    database = mysql.connector.connect(
                host="mysql",
                port=3306,
                database="FraudData",
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                allow_local_infile=True
            )
    
    parser = ArgumentParser()
    parser.add_argument('command', type=str, 
        choices=['help','init','drop'])
    args = parser.parse_args()

    if args.command == 'help':
        help_message()
    elif args.command == 'init':
        datainit.initialize_data(database)
    elif args.command == 'drop':   
        datainit.drop_database(database)