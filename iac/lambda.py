import boto3
import os

BUCKET_NAME = 'bigdata-bdml2-project-bucket'

# Structure du bucket S3
DIR_STRUCTURE = [
    'raw/',
    'processed/',
    'logs/'
]

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    try:
        s3_client.head_bucket(Bucket=BUCKET_NAME)
        
        # Créer les répertoires si nécessaire
        for directory in DIR_STRUCTURE:
            key = f"{directory}"
            response = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix=key)
            if 'Contents' not in response:
                s3_client.put_object(Bucket=BUCKET_NAME, Key=f"{key}")
                print(f"Created directory: {key}")
        
        # Récupérer les fichiers existants à la racine du bucket ou autres endroits
        response = s3_client.list_objects_v2(Bucket=BUCKET_NAME)
        if 'Contents' in response:
            for obj in response['Contents']:
                file_key = obj['Key']
                
                # Vérifier si le fichier n'est pas déjà dans 'raw/'
                if not file_key.startswith('raw/') and not file_key.endswith('/'):
                    # Déplacer le fichier dans le dossier raw/
                    destination_key = f"raw/{os.path.basename(file_key)}"
                    
                    # Copier le fichier
                    s3_client.copy_object(
                        Bucket=BUCKET_NAME,
                        CopySource={'Bucket': BUCKET_NAME, 'Key': file_key},
                        Key=destination_key
                    )
                    
                    # Supprimer le fichier original après copie (si nécessaire)
                    s3_client.delete_object(Bucket=BUCKET_NAME, Key=file_key)
                    
                    print(f"Moved file {file_key} to {destination_key}")
        
        return {
            'statusCode': 200,
            'body': f"Initialized minimal directories and moved files to 'raw/' in bucket {BUCKET_NAME}"
        }
    except Exception as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'body': f"Error initializing directories or moving files: {e}"
        }
