#%%
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

#%%

message = Mail(
    from_email='jorge@pokeymj.pw',
    to_emails='jorge.girazabal@gmail.com',
    subject='Sending with Twilio SendGrid is Fun',
    html_content='<strong>and easy to do anywhere, even with Python</strong>')
try:
    sg = SendGridAPIClient("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")
    response = sg.send(message)
    print("SUCCESS")
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print("ERROR")
    print(e.message)


#%%
from src.app import Session
from src.models import Baby


db = Session()

baby = db.query(Baby).filter(Baby.parent_ids.contains([1])).one()
db.close()
