#########################
# !/usr/bin/python2.7
# encoding: utf-8
# Author: Shawn Roche
# Date: 3/13/2015
#########################
from urllib import quote, unquote
import requests
import plistlib
import random
from sys import argv

USER = 'user'
PASS = 'password'


def main():
    link_prefix = 'itms-services://?action=download-manifest&url='
    webdav_url = 'https://support.apperian.com/owncloud/remote.php/webdav'

    # Take the provided Direct Download link, unquote it, download the plist, and edit the bundle ID
    link = unquote(argv[1].replace(link_prefix, ''))
    r = requests.get(link)
    plist = plistlib.readPlistFromString(r.text)
    plist['items'][0]['metadata']['bundle-identifier'] += str(random.randrange(0, 1000))
    plistlib.writePlist(plist, 'manifest.plist')

    # Get the values to create folders in owncloud and upload files
    bundle_id = plist['items'][0]['metadata']['bundle-identifier']
    title = plist['items'][0]['metadata']['title']
    save_path = '/forced_bundle_id/%s/%s/%s' % (title, bundle_id, 'manifest.plist')

    # Open a session for owncloud
    s = requests.Session()
    s.auth = (USER, PASS)
    s.verify, s.stream, s.allow_redirects = True, True, True

    # Create the necessary folders, upload the manifest.plist, and create a public share link
    s.request('MKCOL', '%s/%s/%s' % (webdav_url, 'forced_bundle_id', title))
    s.request('MKCOL', '%s/%s/%s/%s' % (webdav_url, 'forced_bundle_id', title, bundle_id))
    with open('manifest.plist', 'rb') as f:
        s.request('PUT', webdav_url + save_path, data=f)
    share = s.post(
        'https://ftp.apperian.com/ocs/v1.php/apps/files_sharing/api/v1/shares',
        params={'format': 'json'},
        data={
            'path': save_path,
            'shareType': 3,
            'permissions': 1
        },
    ).json()

    if share['ocs']['meta']['status'] == 'ok':
        oc_dl = 'https://support.apperian.com/index.php/s/%s/download' % share['ocs']['modules']['token']
        link = link_prefix + quote(oc_dl, '')
    else:
        print "\n\n\n\nThere was a problem\n"
        print "Error Code %s" % share['ocs']['meta']['statuscode']
        print share['ocs']['meta']['message']
        exit(2)

    print '\n\n', '#' * 80, '\n', '#' * 80, '\n'
    print "Provide the below link to the customer:"
    print "They may have to accept a popup asking to open with the app store.\n"
    print link
    print '\n', '#' * 80, '\n', '#' * 80, '\n\n'
if len(argv) == 2:
    main()
else:
    print "Incorrect number of arguments"
    print 'You need to pass the direct download URL enclosed in quotes as a parameter EX:'
    print "python forced_bundle_id.py \"DOWNLOAD_URL\""
