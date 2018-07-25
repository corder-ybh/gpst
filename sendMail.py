# -*- coding: UTF-8 -*-

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import Encoders
import os

#subject 标题 text 内容 files:[]
def sendMail(mailTo, mailFrom, subject, text, files, subtype='plain', server="localhost") :
    assert type(mailTo) == list
    assert type(files) == list

    msg = MIMEMultipart('related')
    msg['From'] = mailFrom
    msg['To'] = COMMASPACE.join(mailTo)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.preamble = 'This is a multi-part message in MIME format.'

    msgAlternative = MIMEMultipart('alternative')
    msg.attach(msgAlternative)

    msgContent = text.replace("\n", "<br>") if text else ""
    msgContent += "<br>" + text if text else ""

    msgHtmlImg = msgContent + "<br>"


    #如果 text 是 html，则需要设置 _subtype='html'
    #默认情况下 _subtype='plain',即纯文本
    #msg.attach(MIMEText(text, _subtype='html',_charset='utf-8'))
    msg.attach(MIMEText(text, _subtype=subtype, _charset='utf-8'))

    for f in files :
        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(f, "rb").read())
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment;filename="%s"' % os.path.basename(f))
        msg.attach(part)

    smtp = smtplib.SMTP(server)
    smtp.sendmail(mailFrom, mailTo, msg.as_string())
    smtp.close()

if __name__ == '__main__' :
    text = ''
    sendMail(['924993083@qq.com'], 'MonitorBase <notify@monitor.base>', 'Send Mail', text,[],'html')