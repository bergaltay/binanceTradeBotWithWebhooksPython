import firebase_admin
from firebase_admin import credentials, firestore, exceptions
import loggerMain


credentialData = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(credentialData)


try:
    DBConnector = firestore.client()
    DBException = firebase_admin.exceptions
    loggerMain.log.info('Successfully connected to the DB')
except firebase_admin.exceptions as e:
    loggerMain.log.error('Couldn\'t connect to the DB   Error :  '+e)


