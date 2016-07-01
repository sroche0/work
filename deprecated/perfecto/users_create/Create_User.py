#########################
# !/usr/bin/python2.7
# encoding: utf-8
# Author: Shawn Roche
# Date: 10/20/2014
#########################
import requests
import csv

# All the fields you will need to edit are in the main function have a comment next to them explaining what they do.
# All of the values you enter for admin_user, roles, etc must be strings.


def main():
    info = {'admin_u': 'shawnr@perfectomobile.com',
            'admin_pw': '!Perfecto',
            'cloud_data': 'cloud_data.txt',
            'user_data': 'userdata.txt',
            'roles': 'ADMINISTRATOR'}
    headers = ['email', 'password', 'firstname', 'lastname', 'company']

    with open(info['cloud_data'], 'rb') as f:
        clouds = []
        for row in f:
            clouds.append(row.rstrip())

    with open(info['user_data.csv'], 'rb') as f:
        reader =
        for row in f:
            users.append(row.split())

    for x in clouds:
        for y in users:
            info['cloud'] = x
            print y
            info.update(dict(zip(headers, y)))
            print info
            # create_user(info)
    

def error_logging(msg):
    """logs any errors into out.txt, located in the same folder as the script"""
    with open('out.txt', 'a') as f:
        f.write(msg + '\n')


def output(http_reply, info, url):
    """Provides shell feedback on script progress and logs any error messages in out.txt"""
    url_success = ['already exists', 'Success', 'success']

    for condition in url_success:
        if condition in http_reply:
            print 'Success' 
    if '403' in http_reply:
        print '403 Forbidden error on %(cloud)s, check admin username/password and that IP is whitelisted' % info
        msg = '%(cloud)s - %(email)s - 403 FORBIDDEN' % info
        error_logging(msg)

    else:
        print '%(email)s failed on %(cloud)s, check out.txt for error details' % info
        msg = '%(cloud)s - %(email)s - ' + url % info
        error_logging(msg)


def create_user(info):
    """Builds the http request and sends it, actually creating the users"""
    url = '%(cloud)s/services/users?operation=create&user=%(admin_u)s&password=%(admin_pw)s&email=%(email)s' \
          '&userPassword=%(password)s&firstName=%(firstname)s&lastName=%(lastname)s&roles=%(roles)s' \
          '&account.unlimited=true&companyName=%(company)s&sendNotification=True' % info

    print url

    try:
        resp = urllib2.urlopen(url)
        contents = resp.read()
    except urllib2.HTTPError, error:
        contents = error.read()
    except urllib2.URLError:
        contents = '%(cloud) failed, URL appears unreachable. Check if cloud is accessible from this machine' % info
        print(contents)
        error_logging(contents)
    output(contents, info, url)


if __name__ == '__main__':
    main()