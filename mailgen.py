import os
import csv
from PIL import Image, ImageDraw, ImageFont
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

list_of_names = []

# Email configuration
SMTP_SERVER = 'your-smtp-server.com'
SMTP_PORT = 587
SMTP_USERNAME = 'your-email@example.com'
SMTP_PASSWORD = 'your-email-password'

def delete_old_data():
    for i in os.listdir("generated-certificates/"):
        os.remove("generated-certificates/{}".format(i))

def cleanup_data():
    with open('name-data.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            list_of_names.append(row)

def generate_certificate(name, email):
    custom_font = "CinzelDecorative-Bold.ttf"  # Path to your custom font file
    font_size = 80
    font_color = (71, 71, 71)

    certificate_template = Image.open("certificate-template.jpg")
    draw = ImageDraw.Draw(certificate_template)

    # Load the custom font and use it
    font = ImageFont.truetype(custom_font, font_size)

    # Specify the position and color
    position = (715, 618)
    draw.text(position, name, font=font, fill=font_color)

    certificate_template.save("generated-certificates/{}.jpg".format(name))

    # Send the certificate to the recipient's email
    send_certificate(name, email)

def send_certificate(name, recipient_email):
    msg = MIMEMultipart()
    msg['From'] = SMTP_USERNAME
    msg['To'] = recipient_email
    msg['Subject'] = 'Certificate of Completion'

    body = f"Dear {name},\n\nPlease find your certificate attached."
    msg.attach(MIMEText(body, 'plain'))

    # Attach the certificate image
    certificate_filename = f"generated-certificates/{name}.jpg"
    with open(certificate_filename, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f"attachment; filename= {name}.jpg")
    msg.attach(part)

    # Connect to the SMTP server and send the email
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(SMTP_USERNAME, SMTP_PASSWORD)
    text = msg.as_string()
    server.sendmail(SMTP_USERNAME, recipient_email, text)
    server.quit()

def main():
    delete_old_data()
    cleanup_data()

    for person in list_of_names:
        name = person['Name']
        email = person['Email']
        generate_certificate(name, email)
        print(f"Generated and sent certificate to {name} at {email}")

if __name__ == '__main__':
    main()
