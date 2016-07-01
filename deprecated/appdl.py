import urllib
import csv
import urllib2
try:
    import requests
except ImportError:
    print 'This script relies on the requests module. This can be installed by running "pip install requests"'
    exit(1)
import plistlib
import sys


def main(url):
    url_list = []

    # Check what type of arg was passed
    if '.csv' in url:
        with open(url, 'rb') as f:
            reader = csv.reader(f)
            for row in reader:
                url_list.append(row[0])
    else:
        url_list.append(url)

    # Format and print the progress bar
    bar = 53
    if len(url_list) >= 10:
        bar += 1

    print '-' * bar
    print "{:<7}{:<13}{:<13}{}".format('App', 'Name', 'Size', 'Progress')
    print '-' * bar

    # Iterate through the urls that were passed into the script and download them
    # Files will be named by their PSK in EASE.
    for i, v in enumerate(url_list):
        if 'itms' in v:
            link = urllib.unquote(v)
            link = link.replace('itms-services://?action=download-manifest&url=', '')
            r = urllib2.urlopen(link).read()
            plist = plistlib.readPlistFromString(r)

            dl_url = plist['items'][0]['assets'][0]['url']
            file_name = '{}.ipa'.format(link.replace('https://', '').split('/')[4])
        else:
            dl_url = urllib.unquote(v)
            file_name = '{}.apk'.format(dl_url.replace('https://', '').split('/')[4])

        dl = requests.get(dl_url, stream=True)

        # Format headers of progress bar and print info about file size and place in the run
        file_size = int(dl.headers["content-length"])
        status = "{}/{:<5}{:<13}{:<10}".format(i + 1, len(url_list), file_name,
                                               str(round((float(file_size) / float(1000**2)), 2)) + 'mb')
        sys.stdout.write(status)
        sys.stdout.write(' ' * (33 - len(status)))
        sys.stdout.flush()

        file_size_dl, last = 0, 0
        with open(file_name, 'wb') as f:
            for chunk in dl.iter_content(4096):
                file_size_dl += 4096
                f.write(chunk)

                # Check if progress bar needs to be updated for file being downloaded
                dl_status = int(float(file_size_dl) / float(file_size) * 100)
                if dl_status % 5 == 0:
                    if dl_status != last:
                        sys.stdout.write('#')
                        sys.stdout.flush()
                        last = int(dl_status)
            print

            # print '\nDownload URL is below:', str(dl_url), '\n'

if __name__ == '__main__':
    main(sys.argv[1])
