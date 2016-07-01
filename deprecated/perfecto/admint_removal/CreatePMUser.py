import urllib2

domain = '.perfectomobile.com'
adminu = 'shawnr@perfectomobile.com'
adminpw = 'Perfecto1234'
roles = 'ADMINISTRATOR'


def result_output(filename, msg):
    f = open(filename, "a")
    f.write(cloud + " " + msg + '\n')
    f.close()


def output_logic():
    if 'already exists' or 'Success' or 'success' in contents:
        attempts = 0
    elif '403 Forbidden' in contents:
        if attempts == 0:
            attempts += 1
            remove_user('admint', 'admin')
            output_logic()
        else:
            result_output('manual_clouds.txt', "")
            errors += 1
            attempts = 0
    else:
        result_output('out.txt', contents)
        errors += 1
        attempts = 0


def create_user():
    try:
        resp = urllib2.urlopen(url)
        contents = resp.read()
    except urllib2.HTTPError, error:
        contents = error.read()
    except urllib2.URLError:
        result_output('manual_clouds.txt', "")
        contents = 'failed'


def terminal_output():
    if errors == 0:
        result_output('done.csv', 'Users Created')
        print (cloud + ' completed')
        print ('-----------')
    else:
        print (cloud + ' completed with ' + str(errors) + 'errors')
        print ('-----------')


cloudfile = open('cloud_data.txt', 'r')

for aline in cloudfile:
    cvalues = aline.split()
    cloud = cvalues[0]
    errors = 0
    contents = ''

    userfile = open('userdata.txt', 'r')

    for aline in userfile:
        values = aline.split()
        url = 'https://' + cloud + str(domain) + '/services/users?operation=create&user=' + str(
            adminu) + '&password=' + str(adminpw) + '&email=' + values[0] + '&userPassword=' + \
              values[1] + '&firstName=' + values[2] + '&lastName=' + values[
                  3] + '&roles=' + roles + '&account.unlimited=true&companyName=' + values[
                  4] + '&location=US&country=United States&sendNotification=True'

        create_user()
        output_logic

    userfile.close()
    terminal_output()

cloudfile.close()

