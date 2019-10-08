import smtplib

def generateConfirmationEmail(recipient, registrationKey, name):
    gmail_user = '<gmail_username'>
    gmail_pwd = '<gmail_password'>
    FROM = '<gmail_username'>
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = 'Verify your email from King Pin'
    TEXT = 'Hi ' + name + ",\n\nPlease follow this link in order to verify your email address.\nhttp://<domain>.com/verify/" + registrationKey + "\nIf you did not ask to verify this address, you can ignore this email.\n\nThanks,\nThe KingPin team",
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print "sent"
    except Exception, e:
    	print e
    	pass