__author__ = 'sroche'
import csv

users, installed = [], []
prefix = 'AGCO'

with open('%s_InstalledApplications.csv' % prefix, 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        tmp = row[5].split('.')
        row[5] = tmp[0]
        installed.append(row)

with open('%s_UserDetails.csv' % prefix, 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        users.append(row)

merged = [[x[0], x[1], y[2], x[3], x[4], x[5], x[6]] for x in installed for y in users if x[0] == y[0] and x[1] == y[1]]

with open('%s_merged.csv' % prefix, 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(merged)