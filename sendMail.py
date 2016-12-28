#!/usr/bin/env python
#encoding:utf8
import os
import time
import sys
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import os
import time
import smtplib

reload(sys)
sys.setdefaultencoding('utf-8')
# config-start
# 日志文件名
logFileName = "manager-log.txt"
# 数据库配置
interval = 60 * 10 #  设置间隔多少秒进行一次数据库查询和数据获取 , 单位是秒
# config-end


def _format_addr(s):
	name, addr = parseaddr(s)
	return formataddr(( \
		Header(name, 'utf-8').encode(), \
		addr.encode('utf-8') if isinstance(addr, unicode) else addr))

def sendEmail(content):
	from_addr = ""
	password = ""
	to_addr = ""
	smtp_server = ""
	msg = MIMEText(content, 'plain', 'utf-8')
	msg['From'] = _format_addr(u'腾讯云服务器<%s>' % from_addr)
	msg['To'] = _format_addr(u'管理员 <%s>' % to_addr)
	msg['Subject'] = Header(u'免费厂商', 'utf-8').encode()
	server = smtplib.SMTP(smtp_server, 25)
	server.set_debuglevel(1)
	server.login(from_addr, password)
	server.sendmail(from_addr, [to_addr], msg.as_string())
	server.quit()


def log(content):
	file = open("logmail.log","a+")
	file.write(content + "\r\n")
	file.close()

def task():
	command = "cat sqlmap.log | grep -E \"GET http|Payload:|Tencent:\" > mailContent.txt"
	#print command
	os.system(command)

	contentFile = open("mailContent.txt","r")
	content = ""
	for line in contentFile:
		content += line
	#print content
	print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
	if content == "":
		log(u"文件为空...忽略 , 等待下一下发送")
		print u"文件为空...忽略 , 等待下一下发送"
	else:
		log(content)
		sendEmail(content)
		os.system("cat sqlmap.log >> sqlmap.log.bak")
		os.system("echo \"\" > sqlmap.log")
		os.system("echo \"\" > mailContent.txt")

def timer(n):  
	while True:
		log("-------------------")
		print "--------------------------"
		log(time.strftime('%Y-%m-%d %X',time.localtime()))
		print time.strftime('%Y-%m-%d %X',time.localtime())
		task()
		time.sleep(n)

if __name__ == '__main__':
	timer(interval)
