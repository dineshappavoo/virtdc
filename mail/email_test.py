#!/usr/bin/env python
# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText

def send_support_mail():
	# Open a plain text file for reading.  For this example, assume that
	# the text file contains only ASCII characters.
	fp = open('/var/lib/virtdc/mail/textfile.py', 'rb')
	# Create a text/plain message
	msg = MIMEText(fp.read())
	fp.close()

	from_address = 'virtdc-support@virtdc.org'
	to_address = ['dinesh.appavoo@utdallas.edu','imaginejhm@gmail.com','rxw130330@utdallas.edu','qxd130530@utdallas.edu','rkn130030@utdallas.edu']
	msg['Subject'] = 'Test mail from virtdc application support'
	msg['From'] = from_address
	msg['To'] = ",".join(to_address)

	# Send the message via our own SMTP server, but don't include the
	# envelope header.
	s = smtplib.SMTP('localhost')
	s.sendmail(from_address, to_address, msg.as_string())
	s.quit()
if __name__ == "__main__":
   # stuff only to run when not called via 'import' here
	send_support_mail()
