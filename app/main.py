from argparse import ArgumentParser
import mysql.connector # type: ignore
import os

def help_message():
    print("""Commands list:
    help - print this message
    init - initialize data from Kaggle into database
           (need to be done only once)""")

if __name__ == "__main__":
    database = mysql.connector.connect(
                host="mysql",
                port=3306,
                database="FraudData",
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
            )
    
    parser = ArgumentParser()
    parser.add_argument('command', type=str, 
        choices=['help','init'])
    args = parser.parse_args()

    if args.command == 'help':
        help_message()
    elif args.command == 'init':
        pass