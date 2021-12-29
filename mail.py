import sys
import os
import re
from config import mail_username as sender, mail_password

from smtplib import (
    SMTP_SSL as SMTP,
)  # this invokes the secure SMTP protocol (port 465, uses SSL)

# from smtplib import SMTP                  # use this for standard SMTP protocol   (port 25, no encryption)

# old version
# from email.MIMEText import MIMEText
from email.mime.text import MIMEText


def send(to, subject, content):

    msg = MIMEText(content, "html")
    msg["Subject"] = subject
    msg["From"] = sender  # some SMTP servers will do this automatically, not all

    conn = SMTP("smtp.gmail.com", 465)
    conn.set_debuglevel(False)
    conn.login(sender, mail_password)
    try:
        conn.sendmail(sender, to, msg.as_string())
    finally:
        conn.quit()
