__author__ = 'ShawnR'

import urllib2

domain = '.perfectomobile.com'
ADMIN_USER = 'shawnr@perfectomobile.com'
ADMIN_PASS = 'Perfecto1234'
USERID = 'shawnr@perfectomobile.com'
NEW_PASS = '!Perfecto1234$'


def result_output(filename, msg):
    f = open(filename, "a")
    f.write(cloud + " " + msg + '\n')
    f.close()


URL_SUCCESS = ['already exists', 'Success', 'success']


# def output_logic():
#     for condition in URL_SUCCESS:
#         if condition in contents:
#             return True, contents
#     if '403 Forbidden' in contents:
#         if attempts == 0:
#             attempts += 1
#             remove_user('admint', 'admin')
#             output_logic()
#         else:
#             result_output('manual_clouds.txt', "")
#             errors += 1
#             attempts = 0
#     else:
#         result_output('out.txt', contents)
#         errors += 1
#         attempts = 0


def send_change_pass(adminu, adminpw):
    try:
        resp = urllib2.urlopen(cloud + '/services/users/' + USERID + '?operation=changePassword&user=' + adminu +
                               '&password=' + adminpw + '&userPassword=' + NEW_PASS)
        contents = resp.read()
    except urllib2.HTTPError, error:
        contents = error.read()
    except urllib2.URLError:
        result_output('manual_clouds.txt', "")
        contents = 'failed'


def change_pass(adminu,adminpw):
    """tries a couple times and then returns True or False if created"""
    attempts = 0
    print cloud + '/services/users/' + USERID + '?operation=changePassword&user=' + adminu + \
          '&password=' + adminpw + '&userPassword=' + NEW_PASS
    while True:
        contents = send_change_pass(adminu,adminpw)
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


cloudfile = open('cloud_data.txt', 'r')

for aline in cloudfile:
    cvalues = aline.split()
    cloud = cvalues[0]
    print (cloud + ' working')
    errors, contents = 0, ''

    userfile = open('userdata.txt', 'r')
    for line in userfile:
        values = line.split()
        send_change_pass('shawnr@perfectomobile.com', values[0])

    userfile.close()
    shell_output()

cloudfile.close()
