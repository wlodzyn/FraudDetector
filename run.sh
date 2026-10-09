#cp .env.example .env       #fill .env with your own values

docker compose up -d mysql  #start mysql container
#run python container:
docker compose run --rm python bash -c ' 
#python3 app/main.py help
#python3 app/main.py init
#python3 app/main.py histo
python3 app/main.py qqplot
'
docker compose down #stop composed container
