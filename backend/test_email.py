import smtplib
from email.mime.text import MIMEText

smtp_user = "b2b.lead.intelligence@gmail.com"
smtp_password = "ahwrexdueiuazsgr"

print("Testing Gmail SMTP connection...")
print(f"Email: {smtp_user}")
print(f"Password: {smtp_password[:4]}****")

try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    print("✅ STARTTLS successful")
    
    server.login(smtp_user, smtp_password)
    print("✅ Gmail login successful!")
    
    # Send test email
    msg = MIMEText("This is a test email from HPCL Lead Intelligence!")
    msg['Subject'] = "Test Email - HPCL System"
    msg['From'] = smtp_user
    msg['To'] = smtp_user
    
    server.send_message(msg)
    print("✅ Test email sent successfully!")
    
    server.quit()
    
except Exception as e:
    print(f"❌ Error: {e}")