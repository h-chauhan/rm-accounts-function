import sentry_sdk
from sentry_sdk.integrations.serverless import serverless_function
from google.cloud import firestore

from account import findAccount

db = firestore.Client()

sentry_sdk.init('https://b60cf5052e05436597457e63f44b55ab@sentry.io/1412597')

@serverless_function
def handler(event):
    accounts = {
        'internship': findAccount('internship'),
        'placement': findAccount('placement')
    }

    collectionRef = db.collection('accounts')
    collectionRef.document('internship').set(accounts['internship'])
    collectionRef.document('placement').set(accounts['placement'])

    print('Response: ', accounts)
    return str(accounts)