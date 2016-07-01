from apperianapi import apperian

ease = apperian.Pyapi('user', 'password')

php_apps = ease.publisher.get_list()
php_apps = php_apps['result']

pyapps = ease.app.list()['result']

print 'Len of publishing api list - {}'.format(len(php_apps))
print 'Len of applications api list - {}'.format(len(pyapps))

matched = [x['bundleId'] for x in php_apps for y in pyapps if x['bundleId'] == y['bundle_id']]

print 'Len of matching bundle IDs - {}'.format(len(matched))
print
for i in matched:
    print i

for i in pyapps:
    if i['bundle_id'] not in matched:
        print 'Missing bundle ID: {}'.format(i['bundle_id'])
