from botocore.exceptions import ClientError
import json

class SesMailSender:
    def __init__(self, client):
        self.client = client

    def send_email(self, sender, destination, subject, text, html):
        try:
            response = self.client.send_email(
                Source=sender,
                Destination={'ToAddresses': destination.emails},
                Message={
                    'Subject': {'Data': subject},
                    'Body': {
                        'Text': {'Data': text},
                        'Html': {'Data': html}
                    }
                }
            )
            print(f"Email sent! Message ID: {response['MessageId']}")
        except ClientError as e:
            print(f"Error sending email: {e.response['Error']['Message']}")

    def send_templated_email(self, sender, destination, template_name, template_data):
        try:
            response = self.client.send_templated_email(
                Source=sender,
                Destination={'ToAddresses': destination.emails},
                Template=template_name,
                TemplateData=json.dumps(template_data)
            )
            print(f"Templated email sent! Message ID: {response['MessageId']}")
        except ClientError as e:
            print(f"Error sending templated email: {e.response['Error']['Message']}")

class SesDestination:
    def __init__(self, emails):
        self.emails = emails