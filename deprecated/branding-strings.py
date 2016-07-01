#!/usr/bin/python2.7
# -*-coding:utf-8 -*-
# Author    : Chris McLean


import subprocess

subprocess.call(['open', '-a', 'TextEdit',
                 '/Users/sroche/git/EASEweb/web/hub/application.json'])

print """
Let's create the BrandApp.py command...

First, edit the application.json file and input the org psk.

Next, answer the questions below...
"""

ipa_path = '/Users/sroche/Desktop/branding/branded_apps/'
branding_path = '/Users/sroche/git/EASENewAppCatalog/branding/'  # EASEweb package assets
web_assets = '/Users/sroche/git/EASEweb/web/hub/'
line = '=' * 40 

# Get variable info from user
company = raw_input('What company is this for? ')
ipa_input_path = ipa_path + raw_input("What is the input .ipa? ")
ipa_output_path = ipa_path + raw_input("What is the output .ipa?")
branding_assets = branding_path + raw_input("Where are the branding assets located? ")
org_id = raw_input("What is the org id?")
output_zip_path = branding_path + raw_input("What is the output .zip package? ")

print line
print """
BrandApp.py string complete! The BrandApp.py command to run is:

python BrandApp.py -ipa %s -oipa %s -p %s -a %s -c %s -z %s
""" % (ipa_input_path, ipa_output_path, web_assets, branding_assets, org_id, output_zip_path)

print line
print 'Now answer the questions below to create the deploy.py command...'
print

# deploy.py string...
server = ['https://na01ws.apperian.com', 'https://eu01ws.apperian.eu', 'https://btws.apperian.eu',
          'https://telusws.amtelus.com']

print 'What server is the org on?'
print '1. NA'

zip_package_location = raw_input("Where is the .zip package located? ")

#.zip output
zip_package_path = '/Users/sroche/git/EASENewAppCatalog/branding/'
full_zip_package_path = "".join((zip_package_path, zip_package_location))

print
"Deploy.py string complete! The deploy.py command to run is..."

print "python ./deploy.py --server %s --catalog-zip %s --platform-type-id 1 --username " \
      "help@apperian.com --password *ByHbqIA@vo@Fa, --org %s" \
      % (server[0], zip_package_path, org_id)
