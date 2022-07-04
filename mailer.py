from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
import smtplib
import ssl
import csv
import sys
from datetime import date

with open('membership_list.csv') as csv_file:
    csv_reader = csv.reader(csv_file)
    rows = list(csv_reader)

limit = int(sys.argv[1]) if len(sys.argv) > 1 else 3
smtp_server = "smtp.gmail.com"
port = 587  # For starttls
sender_email = "sender@example.com"  # TODO: replace with your email address
sender_name = 'Sender Name'  # TODO: replace with your name
password = 'xxxJJJsss'  # TODO: replace with your 16-digit-character password

## Attachments in general
## Replace filename to your attachments. Tested and works for png, jpeg, txt, pptx, csv
## filename = 'test.csv' # TODO: replace your attachment filepath/name
## with open(filename, 'rb') as fp:
## attachment = MIMEApplication(fp.read())
## attachment.add_header('Content-Disposition', 'attachment', filename=filename)
## msg.attach(attachment)

context = ssl.create_default_context()


def sendMail():
    # Send email here
    # initialise message instance
    msg = MIMEMultipart()
    msg["Subject"] = "Test email notification 14 on {}".format(date.today().strftime("%Y-%m-%d"))
    msg["From"] = sender_email

    with open('src/open_house_invite.html', 'r') as file:  # r to open file in READ mode
        html = file.read()
    body_html = MIMEText(html.format(row[0], sender_name, sender_name), 'html')  # parse values into html text
    msg.attach(body_html)  # attaching the text body into msg
    msg['To'] = row[1]

    # Image
    # img_name = 'src/mezcla.png'
    # with open(img_name, 'rb') as fp:
    #     img = MIMEImage(fp.read())
    # img.add_header('Content-Disposition', 'attachment', filename=img_name)
    # msg.attach(img)
##
    server.sendmail(sender_email, row[1], msg.as_string())


# Try to log in to server and send email
try:
    server = smtplib.SMTP(smtp_server, port)
    server.ehlo()  # check connection
    server.starttls(context=context)  # Secure the connection
    server.ehlo()  # check connection
    server.login(sender_email, password)

    counter = 0
    for row in rows:
        if counter >= limit:
            break  # break here
        print('Sent mail to %s', (row[1]))
        sendMail()
        counter += 1

except Exception as e:
    # Print any error messages to stdout
    print(e)
finally:
    server.quit()
