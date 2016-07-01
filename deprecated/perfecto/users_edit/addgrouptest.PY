import urllib2
from xml.dom.minidom import parseString
import webbrowser
import logging
import os




#***********************
cloud ="nespresso"
adminUserName="admint"
adminPassword="admin"
group="TestGroup2"
role2=""

#***********************
if not os.path.exists("c:\\log_results\\"):
        os.makedirs("c:\\log_results\\")

logger = logging.getLogger('myapp')
hdlr = logging.FileHandler('c:\\log_results\\addrole.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.INFO)

logger.info("starting to add roles:" + group + role2 + " on : " + cloud)

userListUrl="https://"+ cloud + ".perfectomobile.com/services/users?operation=list&user=" + adminUserName + "&password=" + adminPassword + "&groups=TestGroup1" + "&responseFormat=xml"
logger.info("gettign user list from:" + userListUrl)
usock = urllib2.urlopen(userListUrl)
siteXml = usock.read()
usock.close()
dom = parseString(siteXml)


#** getting all the username element and the user element in the xml
name = dom.getElementsByTagName('user')
for p in name:
    username_raw= p.getElementsByTagName("username")
    username= username_raw[0].firstChild.toxml()
    logger.info("got username: " + username)
    cloudUrl="https://"+ cloud + ".perfectomobile.com/services/users/" + username +  "?operation=update&user=" + adminUserName + "&password=" + adminPassword + "&groups=" + group
    logger.info("using cloud url:" + cloudUrl)
    urllib2.urlopen(cloudUrl)

logger.info("adding role:" + group + role2 + "completed without errors")
logger.info("opennign log folder")
os.startfile("c:\\log_results\\")
print "completed"
    
    
