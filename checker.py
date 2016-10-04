import requests
import os
import smtplib
import subprocess
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate

pages = {
    'cics': {
        'url': "https://www.cics.umass.edu/current-students/career-development",
        'email': ['skatkuri@cs.umass.edu', 'stipirineni@cs.umass.edu'],
    },
    'umass-general': {
        'url': "http://www.umass.edu/umfa/job-board",
        'email': ['skatkuri@cs.umass.edu', 'stipirineni@cs.umass.edu', 'amathihalli@umass.edu', 'cmummidi@umass.edu']
    }
    # 'oncampus': "http://www.umass.edu/umfa/job-board?field_job_title_tid=All&field_work_study_non_work_study_value=All&field_hiring_period_value=All&field_on_off_campus_value=on&keys="
}

from_email = 'monitor'


for name, link in pages.items():
    subject = ''
    body = 'How is your life today?'
    res = requests.get(link['url'])
    cur_state = res.text
    suffix = '-new'
    with open(name + suffix, 'w') as fout:
        fout.write(cur_state.encode('utf-8'))
    if not os.path.exists(name): 
        subject = 'No previous state found for %s. Creating it now.' % name
    else:
        cmd = 'diff %s %s' % (name, name + suffix)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, shell=True)
        stdout, stderr = p.communicate()
        if stdout:
            subject = 'Change detected on %s' % name
            body = 'Diff of change:<br><br> %s' % stdout

    p = subprocess.Popen('mv %s %s' % (name + suffix, name),
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = p.communicate()
    if subject:
        smtp = smtplib.SMTP()
        smtp.connect()
        msg = MIMEMultipart()
        msg["From"] = "Monitor"
        msg["To"] = ','.join(link['email'])
        msg['Date'] = formatdate(localtime=True)
        msg["Subject"] = subject
        # receivers = to_email + [x[1] for x in settings.ADMINS]
        receivers = link['email']
        msg.attach(MIMEText(body, 'html'))
        smtp.sendmail(from_email, receivers, msg.as_string())
        smtp.close()
