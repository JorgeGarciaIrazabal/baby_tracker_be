from typing import List, Union

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def send_email(to: Union[List[str], str], subject: str, content: str):
    import os
    message = Mail(
        from_email=os.environ["EMAIL_SENDER_ADDRESS"],
        to_emails=to,
        subject=subject,
        html_content=content)
    try:
        sg = SendGridAPIClient(
            os.environ["SENDGRID_API_KEY"])
        response = sg.send(message)
        print("SUCCESS")
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print("ERROR")
        print(e.message)
