import smtplib
from email.mime.text import MIMEText
import base64
import sqlite3
import os

# Email configuration
smtp_server = "smtp.gmail.com"
smtp_port = 587  # For TLS
sender_email = "fall2023sde@gmail.com"  # Your Gmail address
sender_password = "bdea bekv mhlb ddcr"  # Your App Password - 2FA needed for this to work

# Database connection
connection = sqlite3.connect(os.path.join(os.getcwd(), os.path.dirname(__file__), "mail_data.db"))
cursor = connection.cursor()

# Query the database to get recipient email addresses with the specified condition
query = "SELECT email, currentCases, pastCases FROM mailList WHERE (currentCases - pastCases) >= 1000"
cursor.execute(query)
recipient_data = cursor.fetchall()

# Email content
subject = "Covid Rise Alert !!!"

# Load the image from local storage
image_path = '/Users/sai/Desktop/Final Version/covid.jpeg'
with open(image_path, 'rb') as image_file:
    image_data = base64.b64encode(image_file.read()).decode('utf-8')

stripo_template = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html dir="ltr" xmlns="http://www.w3.org/1999/xhtml" xmlns:o="urn:schemas-microsoft-com:office:office"><head><meta charset="UTF-8"><meta content="width=device-width, initial-scale=1" name="viewport"><meta name="x-apple-disable-message-reformatting"><meta http-equiv="X-UA-Compatible" content="IE=edge"><meta content="telephone=no" name="format-detection"><title></title><!--[if (mso 16)]>
    <style type="text/css">
    a {{text-decoration: none;}}
    </style>
    <![endif]--><!--[if gte mso 9]><style>sup {{ font-size: 100% !important; }}</style><![endif]--><!--[if gte mso 9]>
<xml>
    <o:OfficeDocumentSettings>
    <o:AllowPNG></o:AllowPNG>
    <o:PixelsPerInch>96</o:PixelsPerInch>
    </o:OfficeDocumentSettings>
</xml>
<![endif]--><!--[if mso]>
 <style type="text/css">
     ul {{
  margin: 0 !important;
  }}
  ol {{
  margin: 0 !important;
  }}
  li {{
  margin-left: 47px !important;
  }}

 </style><![endif]
--></head><body class="body"><div dir="ltr" class="es-wrapper-color"><!--[if gte mso 9]>
            <v:background xmlns:v="urn:schemas-microsoft-com:vml" fill="t">
                <v:fill type="tile" color="#f6f6f6"></v:fill>
            </v:background>
        <![endif]--><table class="es-wrapper" width="100%" cellspacing="0" cellpadding="0"><tbody><tr><td class="esd-email-paddings" valign="top"><table class="esd-header-popover es-header" cellspacing="0" cellpadding="0" align="center"><tbody><tr><td class="esd-stripe" align="center"><table class="es-header-body" width="600" cellspacing="0" cellpadding="0" bgcolor="#ffffff" align="center"><tbody><tr><td class="es-p20t es-p20r es-p20l esd-structure" align="left"><table class="es-right" cellspacing="0" cellpadding="0" align="right"><tbody><tr><td class="esd-container-frame" width="560" align="left"><table width="100%" cellspacing="0" cellpadding="0"><tbody><tr>
    <td align="center" class="esd-block-text es-m-txt-c">
        <p style="white-space:nowrap">Covid Cases have increased by <span style="color: red; font-weight: bold;">{difference}</span> in your state. <br>​</p><p style="white-space:nowrap">Please take precautions !!!</p>
    </td>
</tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table><table class="es-content" cellspacing="0" cellpadding="0" align="center"><tbody><tr><td class="esd-stripe" align="center"><table class="es-content-body" width="600" cellspacing="0" cellpadding="0" bgcolor="#ffffff" align="center"><tbody><tr><td class="es-p20t es-p20r es-p20l esd-structure" align="left"><table width="100%" cellspacing="0" cellpadding="0"><tbody><tr><td class="esd-container-frame" width="560" valign="top" align="center"><table width="100%" cellspacing="0" cellpadding="0"><tbody><tr>
    <td align="center" class="esd-block-image es-m-txt-l" style="font-size: 0">
        <a target="_blank">
            <img class="img-5981" src="https://fbpiyiv.stripocdn.email/content/guids/CABINET_102321ef6bca82626580e1093966cc0e1e3c1abda952af6f807983d17ff620f0/images/istockphoto13309962131024x1024.jpg" alt="" style="border-radius:0" width="560">
        </a>
    </td>
</tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table><table class="es-content" cellspacing="0" cellpadding="0" align="center"><tbody><tr><td class="esd-stripe" align="center"><table class="es-content-body" width="600" cellspacing="0" cellpadding="0" bgcolor="#ffffff" align="center"><tbody><tr><td class="esd-structure es-p20t es-p20b es-p20r es-p20l" align="left"><table class="es-right" cellspacing="0" cellpadding="0" align="right"><tbody><tr><td class="esd-container-frame" width="560" align="left"><table width="100%" cellspacing="0" cellpadding="0"><tbody><tr><td class="esd-empty-container" style="display: none;" align="center"></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table></div></body></html>
"""

# Create a connection to the SMTP server
with smtplib.SMTP(smtp_server, smtp_port) as server:
    # Start TLS encryption
    server.starttls()

    # Login to your Gmail account
    server.login(sender_email, sender_password)

    # Send the email to each recipient
    for recipient in recipient_data:
        email = recipient[0]
        current_cases = recipient[1]
        past_cases = recipient[2]
        difference = current_cases - past_cases

        # Create the email message with inline styles and Stripo HTML template
        message = MIMEText(
            f"{stripo_template.format(difference=difference)}", 'html')

        message["From"] = sender_email
        message["To"] = email
        message["Subject"] = subject

        server.sendmail(sender_email, email, message.as_string())
        print(f"Email sent to {email}")

print("All emails sent successfully.")

