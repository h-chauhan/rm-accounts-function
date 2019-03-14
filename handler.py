import boto3
from bs4 import BeautifulSoup
from robobrowser import RoboBrowser
from botocore.exceptions import ClientError
import sentry_sdk
from sentry_sdk.integrations.aws_lambda import AwsLambdaIntegration
import epsagon

sentry_sdk.init(
    "https://b60cf5052e05436597457e63f44b55ab@sentry.io/1412597",
    integrations=[AwsLambdaIntegration()]
)

epsagon.init(
    token='b817b19f-3969-4481-8ec0-c7a646dbbb33',
    app_name='RM Updates',
    metadata_only=False,
)

dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')

getParams = lambda type: {
    "loginUrl": "http://tnp.dtu.ac.in/rm_2016-17/intern/intern_login",
    "username_field": "intern_student_username_rollnumber",
    "password_field": "intern_student_password",
    "notifsUrl": "http://tnp.dtu.ac.in/rm_2016-17/intern/intern_student",
    "year": "2K16"
} if type == "internship" else {
    "loginUrl": "http://tnp.dtu.ac.in/rm_2016-17/login",
    "username_field": "student_username_rollnumber",
    "password_field": "student_password",
    "notifsUrl": "http://tnp.dtu.ac.in/rm_2016-17/student",
    "year": "2K15"
}

def login(type, account):
    params = getParams(type)
    browser = RoboBrowser(history=True, parser="html.parser")
    browser.open(params["loginUrl"])
    form = browser.get_form(0)

    if not form:
        raise ValueError("Couldn't login")

    form[params["username_field"]].value = account['username']
    form[params["password_field"]].value = account['password']
    browser.submit_form(form)
    browser.open(params["notifsUrl"])
    soup = browser.parsed
    ul = soup.find('ul',attrs={'class':'timeline'})
    return True if ul else False  

def findAccount(type):
    params = getParams(type)
    branches = ["CO", "SE", "IT", "EC", "EL", "EE", "CE", "PS", "BT", "EP", "MC", "ME", "AM", "PE", "EN"]
    for branch in branches:
        for i in range(14, 100):
            rollno = "00" + str(i) if i < 10 else "0" + str(i)
            account = {
                'username': params["year"] + "/" + branch + "/" + rollno,
                'password': "password"
            }
            if login(type, account):
                return account

@epsagon.lambda_wrapper
def handler(event, context):
    try:
        type = event['type']
        account = findAccount(type)
        table = dynamodb.Table('rm-account')
        try:
            table.get_item(Key={
                'type': type
            })
            table.delete_item(Key={
                'type': type
            })
        except ClientError:
            pass
        table.put_item(Item={
            'type': type,
            'username': account['username'],
            'password': account['password'] 
        })
        return account
    except Exception as e:
        sentry_sdk.capture_exception(e)

handler({}, {})