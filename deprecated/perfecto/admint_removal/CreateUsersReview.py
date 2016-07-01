import urllib2

cloud = 'CLOUD'
domain = 'DOMAIN'
adminu = 'shawnr@perfectomobile.com'
adminpw = 'Perfecto1234'

URL_BASE = 'https://{}/services/users?operation=create&user={}&password={}&email={}@CLOUD.com'
URL_BASE += '&userPassword={}&firstName={}&lastName={}&roles=ADMINISTRATOR&account.unlimited=true'
URL_BASE += '&companyName=Perfecto Mobile&location=US&country=United States&sendNotification=True'

URL_SUCCESS = ['already exists', 'success', 'Success']


def result_output(filename, msg):
    """outputs to an external file for logging"""
    with open(filename, mode="a") as f:
        f.write(values[3] + msg + '\n')
        f.close()
    # f = open(filename, "a")
    # f.write(cloud + ' ' + values[3] + ' - ' + msg + ' ' + '\n')
    # f.close()


def output_logic():
    """Main logic. Will attempt alternate credentials on 403 error"""
    if 'already exists' or 'Success' or 'success' in contents:
        attempts = 0
    elif '403 Forbidden' in contents:
        # I want to have this retry a second login if the first fails before moving on and logging it as an error.
        # Not sure if this is the most elegant way.
        if attempts == 0:
            attempts += 1
            adminu, adminpw = 'TEMP_USER2', 'TEMP_PASS2'
            create_user()
            output_logic()
        else:
            result_output('out.txt', '403 Forbidden')
            errors += 1
            attempts = 0
    else:
        result_output('out.txt', contents)
        errors += 1
        attempts = 0

def send_create_user(url):
    try:
        resp = urllib2.urlopen(url)
        contents = resp.read()
    except urllib2.HTTPError, error:
        contents = error.read()
        return contents

def create_user(url):
    """tries a copuple times and then returns True or False if created"""
    attempts = 0
    while True:
        contents = send_create_user(url)
        for condition in URL_SUCCESS:
            if condition in contents:
                return True, contents
        if '403 forbidden' in contents:
            if attempts:
                return False, contents
            attempts += 1
        else:
            return False, contents

def shell_output():
    if errors == 0:
        result_output('done.csv', 'Users Created')
        print (cloud + ' completed')
        print ('-----------')
    else:
        print (cloud + ' completed with ' + str(errors) + 'errors')
        print ('-----------')


cloudfile = open('PMCloudData Full.txt', 'r')

for aline in cloudfile:
    cvalues = aline.split()
    cloud = cvalues[0]
    errors = 0
    contents = ''

    userfile = open('PMUserdata.txt', 'r')

    for line in userfile:
        values = line.split()
        url = 'https://' + cloud + domain + '/services/users?operation=create&user=' + adminu + '&password=' + \
              adminpw + '&email=' + values[0] + '@DOMAIN.com' + '&userPassword=' + values[1] + '&firstName=' + \
              values[2] + '&lastName=' + values[3] + '&roles=ADMINISTRATOR&account.unlimited=true' + \
              '&companyName=COMPANYNAME&location=US&country=United States&sendNotification=True'

        create_user()
        output_logic()

    userfile.close()
    shell_output()

cloudfile.close()
