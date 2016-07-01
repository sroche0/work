import urllib
import csv
import urllib2
import plistlib
from sys import argv


def main(url):
    url_list = []
    if '.csv' in url:
        with open(url, 'rb') as f:
            reader = csv.reader(f)
            for row in reader:
                url_list.append(row[0])
    else:
        url_list.append(url)

    for i in url_list:
        if 'itms' in i:
            link = urllib.unquote(i)
            link = link.replace('itms-services://?action=download-manifest&url=', '')
            r = urllib2.urlopen(link).read()
            plist = plistlib.readPlistFromString(r)

            dl_url = plist['items'][0]['assets'][0]['url']
            file_name = '{}.ipa'.format(link.replace('https://', '').split('/')[4])
        else:
            dl_url = urllib.unquote(i)
            file_name = '{}.apk'.format(dl_url.replace('https://', '').split('/')[4])

        urllib.urlretrieve(dl_url, file_name)
        # print '\nDownload URL is below:', str(dl_url), '\n'

if __name__ == '__main__':
    main(argv[1])
