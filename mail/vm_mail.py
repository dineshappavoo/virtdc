#!/usr/bin/env python
# Import smtplib for the actual sending function
import smtplib
import time
import datetime
# Import the email modules we'll need
from email.mime.text import MIMEText

#==============================================================================
# Variables
#==============================================================================

# Some descriptive variables
#name                = "virtdc"
#version             = "0.1.0"
#long_description    = """virtdc is a set of API's/tools written to create virtual machines for cloud users efficiently."""
#url                 = "https://github.com/dineshappavoo/virtdc"
#license             = ""

#==============================================================================

#-------------------------------------------------------------------------------
#Send email to the support team or user
#	$virsh migrate web1 qemu+ssh://desthost/system
#-------------------------------------------------------------------------------


to_address = ''

def send_support_mail(subject, content):
	try:
        #Activity Log
        vmmail_log = open('/var/lib/virtdc/logs/activity_logs/vmmail.log', 'a+')
		# Create a text/plain message
		msg = MIMEText(content)

		from_address = 'virtdc-support@virtdc.org'
		to_address = ['dinesh.appavoo@utdallas.edu'] #['dinesh.appavoo@utdallas.edu','imaginejhm@gmail.com','rxw130330@utdallas.edu','qxd130530@utdallas.edu','rkn130030@utdallas.edu']

		msg['Subject'] = subject
		msg['From'] = from_address
		msg['To'] = ",".join(to_address)

		# Send the message via our own SMTP server, but don't include the
		# envelope header.
		s = smtplib.SMTP('localhost')
		s.sendmail(from_address, to_address, msg.as_string())
		s.quit()
		vmmail_log.write(str(datetime.datetime.now()) +'Mail to support ::'+str(to_address)+' :: Successfully sent\n')

	except Exception, e:
		print str(datetime.datetime.now()) +'Mail to support ::'+str(to_address)+' :: Failed\n'
		vmmail_log.write(str(datetime.datetime.now()) +'Mail to support ::'+str(to_address)+' :: Failed\n')


if __name__ == "__main__":
	# stuff only to run when not called via 'import' here
	# Open a plain text file for reading.  For this example, assume that
	# the text file contains only ASCII characters.
	fp = open('/var/lib/virtdc/mail/textfile.py', 'rb')
	send_support_mail('Guest creation error - DineshTest1',fp.read())
