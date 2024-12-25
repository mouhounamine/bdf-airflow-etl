import os
import logging
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
from hdfs import InsecureClient

app = Flask(__name__)

# Autoriser CORS pour localhost:3000 uniquement (interface web)
CORS(app, origins=["http://localhost:3000"])

# Configuration des fichiers CSV autorisés
ALLOWED_EXTENSIONS = {'csv'}

# Configuration du client WebHDFS
HDFS_URL = "http://namenode:9870"  # URL pour WebHDFS
HDFS_UPLOAD_PATH = "/uploads"       # Chemin cible dans HDFS
HDFS_USER = "dr.who"                # Utilisateur pour WebHDFS

# Initialisation du client WebHDFS
client = InsecureClient(HDFS_URL, user=HDFS_USER)

# Créer le répertoire temporaire local si inexistant
LOCAL_UPLOAD_DIR = "/app/uploads"
os.makedirs(LOCAL_UPLOAD_DIR, exist_ok=True)

def allowed_file(filename):
    """Vérifier si l'extension du fichier est autorisée."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_to_hdfs(local_file_path, filename):
    """
    Uploader un fichier local vers HDFS en utilisant WebHDFS.
    
    Args:
        local_file_path (str): Chemin du fichier temporaire local.
        filename (str): Nom du fichier à uploader.

    Returns:
        str: Chemin complet dans HDFS en cas de succès, None en cas d'erreur.
    """
    try:
        # Créer un chemin temporaire avec .temp
        hdfs_temp_path = os.path.join(HDFS_UPLOAD_PATH, f"{filename}.temp")
        hdfs_final_path = os.path.join(HDFS_UPLOAD_PATH, filename)

        # Upload du fichier temporaire vers HDFS
        with open(local_file_path, 'rb') as local_file:
            client.write(hdfs_temp_path, local_file, overwrite=True)
        logging.info(f"Fichier temporaire uploadé vers HDFS : {hdfs_temp_path}")

        # Renommer le fichier pour retirer .temp
        client.rename(hdfs_temp_path, hdfs_final_path)
        logging.info(f"Fichier renommé en : {hdfs_final_path}")
        return hdfs_final_path
    except Exception as e:
        logging.error(f"Erreur lors de l'upload vers HDFS : {str(e)}")
        return None

@app.route('/csv', methods=['POST'])
def handle_file_upload():
    """Gérer l'upload de fichiers CSV."""
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        local_temp_path = os.path.join(LOCAL_UPLOAD_DIR, filename)  # Fichier temporaire local

        try:
            # Sauvegarder temporairement le fichier localement
            file.save(local_temp_path)
            logging.info(f"Fichier temporaire enregistré : {local_temp_path}")

            # Upload vers HDFS
            hdfs_file_path = upload_to_hdfs(local_temp_path, filename)
            if not hdfs_file_path:
                return jsonify({"error": "Failed to upload file to HDFS"}), 500

            # Supprimer le fichier temporaire local après succès
            os.remove(local_temp_path)
            logging.info(f"Fichier temporaire supprimé : {local_temp_path}")

            return jsonify({
                "message": "File successfully uploaded to HDFS!",
                "hdfs_path": hdfs_file_path
            }), 200

        except Exception as e:
            logging.error(f"Erreur lors du traitement du fichier : {str(e)}")
            return jsonify({"error": "Internal server error"}), 500

    else:
        return jsonify({"error": "File type not allowed"}), 400

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run(host='0.0.0.0', port=5000, debug=True)
