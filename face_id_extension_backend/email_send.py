import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import os
from dotenv import load_dotenv
load_dotenv()

# Email credentials
sender_email = os.getenv("SENDER_EMAIL")  # Your email
receiver_email = os.getenv("RECIEVER_EMAIL")  # Receiver's email
password = os.getenv("EMAIL_PASSWORD")  # Your email account app password

# Create the email
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = "DASHBOARD"

# Add body to email
body = """
<html>
  <body>
    <p>This is the dashboard email.</p>
    <p>Here's the image:</p>
    <img src="cid:image1">
  </body>
</html>
"""
message.attach(MIMEText(body, "html"))

# Attach the image
image_path = "plots/piechart.png"  # Replace with the path to your image
with open(image_path, 'rb') as img_file:
    image = MIMEImage(img_file.read())
    image.add_header('Content-ID', '<image1>')
    image.add_header('Content-Disposition', 'inline', filename=os.path.basename(image_path))
    message.attach(image)

# Set up the SMTP server
try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()  # Secure the connection
    server.login(sender_email, password)

    # Send the email
    server.send_message(message)
    print("Email sent successfully!")

    # Close the server connection
    server.quit()

except Exception as e:
    print(f"Failed to send email: {e}")