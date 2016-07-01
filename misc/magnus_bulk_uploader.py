from apperianapi import apperian

ease = apperian.Pyapi('user', 'password', 'env')

metadata = {
    'author': 'Apperian',
    'name':'',
    'shortdescription': 'none',
    'longdescription': 'none',
    'version': 1,
    'versionNotes': 'none'
}

app_name = 'Test App'

for x in range(500):
    metadata['name'] = '{} {}'.format(app_name, x)
    count = 0
    while count < 2:
        count += 1
        resp = ease.app.add('Training.ipa', metadata)
        if resp['status'] != 401:
            break

    if count == 2:
        exit('Upload failed, check creds')
