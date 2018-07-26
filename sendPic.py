# -*- coding:utf-8 -*-
import smtplib
import logging
import time
import matplotlib.pyplot as plt
import pandas as pd
import random

from function import getNdatAgo
from function import draw

from sqlalchemy import create_engine
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from configparser import ConfigParser

cf = ConfigParser()
cf.read('./gpst.conf')
email = cf.get("base", "email")
dbHost = cf.get("db", "dbHost")
dbPort = cf.get("db", "dbPort")
dbUser = cf.get("db", "dbUser")
dbPass = cf.get("db", "dbPass")
dbName = cf.get("db", "dbName")

logger = logging.getLogger("django")

engine = create_engine(
    "mysql://" + dbUser + ":" + dbPass + "@" + dbHost + ":" + dbPort + "/" + dbName + "?charset=utf8")
conn = engine.connect()

class EmailHandler(object):
    def __init__(self, smtpserver='localhost'):
        self.smtp = smtplib.SMTP('localhost')
        self.smtpserver = smtpserver

    def generateAlternativeEmailMsgRoot(self, strFrom, listTo, listCc, strSubJect, strMsgText, strMsgHtml, listImagePath):
        # Create the root message and fill in the from, to, and subject headers
        msgRoot = MIMEMultipart('related')
        msgRoot['Subject'] = strSubJect
        msgRoot['From'] = strFrom
        msgRoot['To'] = ",".join(listTo)
        if listCc:
            msgRoot['Cc'] = ",".join(listCc)
        msgRoot.preamble = 'This is a multi-part message in MIME format.'

        msgAlternative = MIMEMultipart('alternative')
        msgRoot.attach(msgAlternative)

        msgContent = strMsgText.replace("\n","<br>") if strMsgText else ""
        msgContent += "<br>" + strMsgHtml if strMsgHtml else ""

        # We reference the image in the IMG SRC attribute by the ID we give it below
        if listImagePath and len(listImagePath)>0:
            msgHtmlImg = msgContent + "<br>"
            for imgcount in range(0, len(listImagePath)):
                msgHtmlImg += '<img src="cid:image{count}"><br>'.format(count=imgcount)
                msgHtmlImg += 'haha</br>'
            msgText = MIMEText(msgHtmlImg, 'html')
            msgAlternative.attach(msgText)
            # print(msgHtmlImg)

            # This example assumes the image is in the current directory
            for i,imgpath in enumerate(listImagePath):
                fp = open(imgpath, 'rb')
                msgImage = MIMEImage(fp.read())
                fp.close()

                # Define the image's ID as referenced above
                msgImage.add_header('Content-ID', '<image{count}>'.format(count=i))
                msgRoot.attach(msgImage)
                print("msgText:"+ msgHtmlImg)
        else:
            msgText = MIMEText(msgContent, 'html')
            msgAlternative.attach(msgText)

        return msgRoot

    # Send the email (this example assumes SMTP authentication is required)
    def sendemail(self, strFrom, listTo, strSubJect, strMsgText, strMsgHtml=None, listImagePath=None, listCc=None):
        msgRoot = self.generateAlternativeEmailMsgRoot(strFrom, listTo, listCc, strSubJect, strMsgText, strMsgHtml, listImagePath)

        try:
            self.smtp = smtplib.SMTP("localhost")
            self.smtp.sendmail(strFrom, listTo, msgRoot.as_string())
            self.smtp.quit()
            print("Send mail success {0}".format(strSubJect))
        except Exception as e:
            print("ERROR:Send mail failed {0} with {1}".format(strSubJect, str(e)))

    def sendPicMail(self, listTo, title, codeList, strFrom='root@us-west-2.compute.internal', ):
        msgRoot = MIMEMultipart('related')
        msgRoot['Subject'] = title
        msgRoot['From'] = strFrom
        msgRoot['To'] = ",".join(listTo)
        msgRoot.preamble = 'This is a multi-part message in MIME format.'

        msgAlternative = MIMEMultipart('alternative')
        msgRoot.attach(msgAlternative)

        tDate = time.strftime("%Y-%m-%d", time.localtime())
        nDate = getNdatAgo(tDate, 100)
        msgContent = "<br>"
        #msgHtmlImg = "<br>"
        i = random.uniform(0, 1000)
        j = random.uniform(1000,2000)
        for code in codeList:
            draw(code)
            msgHtmlImg = code + ":</br>"
            msgHtmlImg += '<img src="cid:image{count}"><br>'.format(count=i)
            msgHtmlImg += '<img src="cid:image{countN}"><br>'.format(countN=j)
            msgHtmlImg += '-------------------------------------------------------------<br>'
            msgText = MIMEText(msgHtmlImg, 'html')
            msgAlternative.attach(msgText)
            print(msgText)

            #添加图片
            fp = open('./'+code+'.png', 'rb')
            s = fp.read()
            #print ("S1:" + s)
            msgImage = MIMEImage(s)
            fp.close()
            msgImage.add_header('Content-ID', '<image{count}>'.format(count=i))
            msgRoot.attach(msgImage)

            fp1 = open('./' + code + '-latest.png', 'rb')
            s2 = fp1.read()
            #print("S2："+ s2)
            msgImage1= MIMEImage(s2)
            fp1.close()
            msgImage1.add_header('Content-ID', '<image{countN}>'.format(countN=j))
            msgRoot.attach(msgImage1)

            i += 1
            j += 1

        try:
            self.smtp = smtplib.SMTP("localhost")
            self.smtp.sendmail(strFrom, listTo, msgRoot.as_string())
            self.smtp.quit()
            print("Send mail success :".format())
            print("content:" + msgRoot.as_string())
        except Exception as e:
            print("ERROR:Send mail failed  with {0}".format(str(e)))

if __name__ == "__main__":
    strFrom = 'root@us-west-2.compute.internal'
    strTo = [email]
    strSubJect = 'test email - text with image'
    eh = EmailHandler()
    imgpath = "./cropper.png"
    imgpath2 = "./picture.png"
    text = "300451 10内出现5&55交叉点 近100日55日均线朝下，最低价21.23，最高34.15"
    tDate = time.strftime("%Y-%m-%d", time.localtime())
    title = tDate + "-报表"
    eh.sendemail(strFrom,strTo, title, text, "<h2>test html content</h2>", [imgpath,imgpath2])