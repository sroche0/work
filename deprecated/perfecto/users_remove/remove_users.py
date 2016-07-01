#########################
# !/usr/bin/python2.7
# encoding: utf-8
# Author: Shawn Roche
# Date: 07/02/2015
#########################
try:
    import requests
except ImportError(requests):
    print 'Python module "requests" is required to run this script. See http://docs.python-requests.org/en/latest/ ' \
          '\nfor installation instructions'
    print 'Exiting...'
    exit()
import csv
import argparse

ADMIN_USERNAME = ''
ADMIN_PASSWORD = ''
CLOUD = None

parser = argparse.ArgumentParser(
    prog='Bulk User Creation',
    usage='python create_users.py --user ADMIN_USER --pass, ADMIN_PASSWORD --roles ADMINISTRATOR,Other_role,ETC '
          '--cloud BASE_CLOUD_URL '
          '\n\nTo avoid setting user and password at runtime, edit the default values in the script itself. '
          '\nCurrent defaults are:'
          '\n    Admin User - {}'
          '\n    Password - {}'
          '\n    Cloud - {}'.format(ADMIN_USERNAME, ADMIN_PASSWORD, CLOUD))

parser.add_argument('--cloud', default=CLOUD)
parser.add_argument('--user', default=None, help='The username of the user you wish to delete')
parser.add_argument('--admin', default=ADMIN_USERNAME, help='Must be an admin on the target cloud')
parser.add_argument('--password', default=ADMIN_PASSWORD)


def main():
    args = parser.parse_args()
    info = {'admin_u': args.admin,
            'admin_pw': args.password,
            'user': args.user}
    users = list(args.user)

    if not args.cloud:
        with open('cloud_data.txt', 'rb') as f:
            clouds = []
            for row in f:
                clouds.append(row.rstrip())
    else:
        clouds = list(args.cloud)

    failed, delete_list, count, progress = [], [], 0, 0
    total = len(clouds) * len(users)
    for cloud in clouds:
        for user in users:
            count += 1
            info.update(cloud)
            info.update(user)
            url = '(cloud)/services/users/(user)?operation=info&user=(admin)&password=(password)'.format(info)
            try:
                r = requests.get(url)
                if r.ok:
                    delete_list.append('{}|{}'.format(cloud, user))
                else:
                    failed.append([cloud, user, '{} Error'.format(str(r.status_code))])
            except requests.ConnectionError:
                failed.append([cloud, user, requests.ConnectionError])

            if progress != (float(count) / float(total)) * 100:
                progress = int((float(count) / float(total)) * 100)
                print '{}% Completed'.format(progress)

    total = len(delete_list)
    for i in delete_list:
        cloud, user = i.split('|')
        url = '{}/services/users/{}?operation=delete&user={}&password={}'.format(cloud, user, args.admin, args.password)
        try:
            r = requests.get(url)
            if r.ok:
                pass
            else:
                failed.append([cloud, user, '{} Error'.format(str(r.status_code))])
        except requests.ConnectionError:
            failed.append([cloud, user, requests.ConnectionError])

        if progress != (float(count) / float(total)) * 100:
            progress = int((float(count) / float(total)) * 100)
            print '{}% Completed'.format(progress)

    if failed:
        print '%d users failed to create. Check failed.csv for details\n' % len(failed)

        with open('failed.csv', 'wb') as f:
            writer = csv.writer(f)
            writer.writerows(failed)

if __name__ == '__main__':
    main()
