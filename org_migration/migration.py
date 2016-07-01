import sys
import os
import csv
import argparse
import datetime
import logging

from apperianapi import apperian


def get_args():
    p = argparse.ArgumentParser()
    p.add_argument('--org', metavar='Name of the folder to save files to', required=True)
    p.add_argument('--suser', '--su', metavar='Source org admin user', required=True)
    p.add_argument('--spassword', '--spw', metavar='Source org admin password', required=True)
    p.add_argument('--sourceenv', '--senv', metavar='Source environment', default='na')
    p.add_argument('--duser', '--du', metavar='Destination org admin user', required=True)
    p.add_argument('--dpassword', '--dpw', metavar='Destination org admin password', required=True)
    p.add_argument('--destenv', '--denv', metavar='Destination environment', default='na')
    p.add_argument('--app_list', metavar='Comma separated list of app psks to migrate', default=None)
    p.add_argument('--verbose', action='store_true', default=False)

    args = p.parse_args()
    return args


class Migrate:
    def __init__(self, args):
        self.source_user = args.suser
        self.source_pw = args.spassword
        self.dest_user = args.duser
        self.dest_pw = args.dpassword
        self.dest_env = args.destenv
        self.source_env = args.sourceenv
        self.app_list = args.app_list
        self.org = args.org
        self.source_ease = apperian.Pyapi(self.source_user, self.source_pw, self.source_env, verbose=args.verbose)
        self.dest_ease = apperian.Pyapi(self.dest_user, self.dest_pw, self.dest_env, verbose=args.verbose)
        self.upload_list = []
        self.upload_failed = []
        self.app_psk_map = []
        self.dl_failed = []

    def download_apps(self):
        self.status_print('Building app list')
        data = self.build_app_list()
        print 'Success'
        print '\nDownloading {} Apps'.format(len(data))
        try:
            os.mkdir(self.org)
        except OSError:
            pass

        print '-' * 50
        cwd = os.getcwd()
        os.chdir(self.org)
        for i in data:
            attempt = 0
            while attempt < 2:
                attempt += 1
                download = self.source_ease.app.download(i['psk'])

                if download['status'] == 200:
                    i.update({'name': download['result']})
                    self.upload_list.append(i)
                    break
                elif download['status'] == 401:
                    self.source_ease.auth()
                else:
                    self.dl_failed.append([i['psk'], i['name'], download['status']])
                    break
        os.chdir(cwd)

    def upload_apps(self):
        print '\nUploading {} Apps'.format(len(self.upload_list))
        print '-' * 40
        for i, v in enumerate(self.upload_list):
            self.status_print(v['name'])
            count = 0
            while count < 2:
                count += 1
                publish = self.dest_ease.app.add('{}/{}'.format(self.org, v['name']), v['meta_data'])
                if publish['status'] == 200:
                    self.app_psk_map.append((v['psk'], publish['result']))
                    print 'Success'
                    break
                elif publish['status'] == 401:
                    self.dest_ease.auth()
                else:
                    print 'Failed'
                    self.upload_failed.append([v['psk'], v['name'], publish['result']])

    def enable_apps(self):
        print
        self.status_print('Enabling apps')
        apps = self.dest_ease.app.list()
        for i in apps['result']:
            self.dest_ease.app.toggle(i['psk'], True)

        print 'Success'

    def build_app_list(self):
        # Get app list from python API, needed for metadata for upload
        ease_list = self.source_ease.app.list()
        if ease_list['status'] != 200:
            exit(ease_list['result'])

        ease_list = ease_list['result']

        # Get app list from PHP API
        pub_list = self.source_ease.publisher.get_list()
        if pub_list['status'] != 200:
            exit(pub_list['result'])

        pub_list = pub_list['result']

        # Actually build the list
        master = []
        data = [{'psk': y['psk'], 'os': y['operating_system'], 'exp': y['version']['install_file']['expires'],
                 'meta_data': x, 'dl_url': y.get('direct_download_binary_url')} for x in pub_list for y in ease_list if
                x['name'] == y['name'] and
                y['status'] == 1 and
                y['is_app_catalog'] == False and
                y['operating_system'] != 3]

        for i in data:
            date = i['exp'].split('T')[0].split('-')
            date = datetime.date(int(date[0]), int(date[1]), int(date[2]))
            if date > datetime.date.today():
                if self.app_list:
                    target = self.app_list.split(',')
                    if i['psk'] in target:
                        master.append(i)
                else:
                    master.append(i)

        return master

    def group_migration(self):
        user_list = self.dest_ease.user.list()
        group_list = self.source_ease.group.list()
        group_list = [x for x in group_list['result'] if x['name'] != 'All Users']
        # Create groups in new org
        print '\nMigrating Groups'
        print '-' * 40
        logging.debug('[EASE] app_psk_map - {}'.format(self.app_psk_map))
        for index, value in enumerate(group_list):
            print '{}/{} - {}'.format(index + 1, len(group_list), value['name'])

            self.status_print('  Creating')

            new_group = self.dest_ease.group.add_group({'group_name': value['name'], 'group_description': value['description']})
            if new_group['status'] == 200:
                logging.debug('[EASE]  new_group - {}'.format(new_group))
                print 'Success'
            elif new_group['status'] == 400:
                if 'already exists' in new_group['result']['message']:
                    print 'Success'
            else:
                print 'Error\n'
                continue

            self.status_print('  Adding Apps')

            app_list = self.source_ease.group.list_apps(value['psk'])
            apps_to_add = [x[1] for x in self.app_psk_map for y in app_list['result'] if y['psk'] == x[0]]
            logging.debug('[EASE]  app_list - {}'.format(app_list))
            logging.debug('[EASE]  app_to_add - {}'.format(apps_to_add))
            added = self.dest_ease.group.add_apps(new_group['result']['psk'], apps_to_add)
            if added['status'] == 200:
                print 'Success'
            else:
                print 'Failed'

            self.status_print('  Adding Users')
            group_members = self.source_ease.group.list_members(value['psk'])
            member_psks = [x['psk'] for x in user_list['result'] for y in group_members['result'] if x['id'] == y['id']]
            logging.debug('[EASE]  group_members - {}'.format(group_members))
            logging.debug('[EASE]  member_psks - {}'.format(member_psks))
            added = self.dest_ease.group.add_multiple_users(new_group['result']['psk'], member_psks)
            if added['status'] == 200:
                print 'Success\n'
            else:
                print 'Failed\n'

    def app_migration(self):
        self.download_apps()
        self.upload_apps()
        self.enable_apps()

    def user_migration(self):
        user_list = self.source_ease.user.list()
        self.status_print('Adding {} Users'.format(len(user_list['result'])))
        if user_list['status'] == 200:
            for user in user_list['result']:
                meta_data = {
                    'user_id': user['id'],
                    'password': 'temp123',
                    'first_name': user['first_name'],
                    'last_name': user['last_name'],
                    'email': user['email'],
                    'role': user['role'],
                    'phone': user['mobile_phone'],
                    'send_invite': False
                }
                new_user = self.dest_ease.user.add(meta_data)

                if user['disabled']:
                    self.dest_ease.user.update(new_user['result'], {'disabled': True})
            print 'Success'
        else:
            print 'Failed'
            exit()

    @staticmethod
    def status_print(msg):
        sys.stdout.write(msg.ljust(30, '.'))
        sys.stdout.flush()


def main(params):
    print
    msg = 'Checking credentials'
    sys.stdout.write(msg.ljust(30, '.'))
    sys.stdout.flush()

    source_test = apperian.Pyapi(params.suser, params.spassword, params.sourceenv, params.verbose)
    if source_test.status != 200:
        exit('Check source user credentials')
    dest_test = apperian.Pyapi(params.duser, params.dpassword, params.destenv, params.verbose)
    if dest_test.status != 200:
        exit('Check dest user credentials')
    print 'Success'

    migrate = Migrate(params)

    migrate.user_migration()
    migrate.app_migration()
    migrate.group_migration()

    if migrate.dl_failed:
        with open('failed_downloads.csv', 'wb') as f:
            writer = csv.writer(f)
            writer.writerows(migrate.dl_failed)

    if migrate.upload_failed:
        with open('failed_uploads.csv', 'wb') as f:
            writer = csv.writer(f)
            writer.writerows(migrate.upload_failed)

    if not migrate.upload_failed:
        print '\nNo errors, cleaning up files'
        to_delete = os.listdir(migrate.org)
        for i in to_delete:
            os.remove('{}/{}'.format(migrate.org, i))

        os.rmdir(migrate.org)

    print 'Migration Complete'


if __name__ == '__main__':
    arguments = get_args()
    main(arguments)
