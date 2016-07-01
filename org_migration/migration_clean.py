from apperianapi import apperian

user = 'user'
pw = 'password'

e = apperian.Pyapi(user, pw)
usernames = e.user.list()

for i in usernames['result']:
    if i['id'] != user:
        print 'Deleting {}'.format(i['id'])
        e.user.delete(i['psk'])

print
print

app_list = e.app.list()
for i in app_list['result']:
    print 'Deleting {}'.format(i['name'])
    e.app.delete(i['psk'])


print
print

group_list = e.group.list()
for i in group_list['result']:
    if i['name'] != 'All Users':
        print 'Deleting {}'.format(i['name'])
        e.group.delete(i['psk'])
