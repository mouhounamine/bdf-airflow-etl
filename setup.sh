# create virtual environment
 python3 -m venv etl-airflow 

# activate virtual environment
source etl-airflow/bin/activate 
# WINDOWS : etl-airflow/bin/activate

# install airflow
pip install "apache-airflow[celery]==2.6.0" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.6.0/constraints-3.8.txt"

# generate requirements
pip freeze > requirements.txt 

# desactivate environment
desactivate venv

# install dependencies
pip install -r requirements.txt


#################################
# Pour lancer 
docker-compose up airflow-init  
docker-compose up -d  

# Pour shutdown 
docker-compose down -v 




#######
# Pour trigger le DAG d'upload dans S3 (via interface web normalement)
curl -X POST -F "file=@./backend/data/raw/menu_items.csv" http://127.0.0.1:5000/csv