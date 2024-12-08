import os
import logging
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import requests
from requests.auth import HTTPBasicAuth
from flask_cors import CORS  

app = Flask(__name__)

# Autoriser CORS pour localhost:3000 uniquement (l'interface web)
CORS(app, origins=["http://localhost:3000"]) 

ALLOWED_EXTENSIONS = {'csv'}
UPLOAD_FOLDER = './uploads'

# Créer le répertoire partagé entre l'API flask & Airflow-webserver 
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# URL de l'API Airflow pour lancer le DAG
AIRFLOW_API_URL = 'http://etl-airflow-webserver-1:8080/api/v1/dags/user_upload_handler/dagRuns'
AIRFLOW_DAG_URL = 'http://etl-airflow-webserver-1:8080/api/v1/dags/user_upload_handler'  # URL pour manipuler l'état du DAG
AUTH = HTTPBasicAuth('airflow', 'airflow')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def trigger_airflow_dag(file_name):
    try:
        # Définir le payload à envoyer à Airflow
        payload = {
            "conf": {
                "file_name": file_name,  # Passer le nom du fichier au DAG
            }
        }

        # Setup du Basic Auth pour se connecter à Airflow
        
        # Envoyer la requête POST à Airflow pour créer une instance d'exécution du DAG
        response = requests.post(AIRFLOW_API_URL, json=payload, auth=AUTH)

        if response.status_code == 200:
            logging.info(f"DAG triggered successfully for {file_name}")
            
            logging.info("DAG is triggered, now unpausing the DAG.")
            unpause_dag()  
            return True
        else:
            logging.error(f"Failed to trigger DAG: {response.text}")
            return False
        
    except Exception as e:
        logging.error(f"Error triggering DAG: {str(e)}")
        return False

# Fonction pour dépauser le DAG en envoyant une requête PATCH
def unpause_dag():
    try:
        payload = {
            "is_paused": False  
        }
        
        response = requests.patch(AIRFLOW_DAG_URL, json=payload, auth=AUTH)

        if response.status_code == 200:
            logging.info("DAG unpaused successfully!")
        else:
            logging.error(f"Failed to unpause DAG: {response.text}")
    
    except Exception as e:
        logging.error(f"Error unpausing DAG: {str(e)}")

# Route Flask pour recevoir le fichier CSV
@app.route('/csv', methods=['POST'])
def handle_file_upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    logging.info(file)
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file:  # Penser à ' and allowed_file(file.filename) '
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        
        # Sauvegarder le fichier dans le répertoire temporaire
        file.save(filepath)
        logging.info(f"File saved to {filepath}")
        
        # Lancer le DAG avec le fichier
        if trigger_airflow_dag(filename):
            # Supprimer le fichier temporaire après avoir déclenché le DAG
            logging.info(f"Temporary file {filepath} removed after triggering DAG")
        
        return jsonify({"message": "File successfully uploaded, DAG triggered!"}), 200
    
    else:
        return jsonify({"error": "File type not allowed"}), 400


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
