import boto3
import logging
import requests
from botocore.exceptions import WaiterError, ClientError

from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, get_single_project
from ses_identity import SesIdentity
from ses_template import SesTemplate
from message_queue import MessageQueue

from email_1 import EMAIL_SUBJECT, EMAIL_BODY_TEXT, EMAIL_BODY_HTML
from email_2 import EMAIL_SUBJECT2, EMAIL_BODY_TEXT2, EMAIL_BODY_HTML2 
from email_3 import EMAIL_SUBJECT3, EMAIL_BODY_TEXT3, EMAIL_BODY_HTML3

def get_project_status(project_id):
    response = requests.get(f"{get_single_project}/{project_id}")
    if response.status_code == 200:
        data = response.json()
        return data.get('status'), data.get('email')
    return None, None

def usage_demo():
    print("-" * 88)
    print("Welcome to the Amazon Simple Email Service (Amazon SES) email demo!")
    print("-" * 88)

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    ses_client = boto3.client(
        "ses",
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )
    ses_identity = SesIdentity(ses_client)
    ses_template = SesTemplate(ses_client)
    message_queue = MessageQueue(ses_client)

    email_server = "ntutlab321projects@gmail.com"
    
    # Get project ID from user input
    project_id = input("Enter the project ID: ")
    
    # Get project status and email
    status, recipient_email = get_project_status(project_id)
    
    if not status or not recipient_email:
        print("Failed to get project status or email. Exiting.")
        return
    
    print(f"Project status: {status}")
    print(f"Recipient email: {recipient_email}")
    
    # Verify recipient email
    if ses_identity.get_identity_status(recipient_email) != "Success":
        print(f"Warning: The address '{recipient_email}' is not verified with Amazon SES.")
        verify = input("Do you want to verify this email? (y/n): ")
        if verify.lower() == 'y':
            ses_identity.verify_email_identity(recipient_email)
            print(f"Verification email sent to {recipient_email}. Please check the inbox and complete verification.")
        else:
            print("Exiting as the email is not verified.")
            return

    message_queue.start_processing()

    # Send email based on project status
    if status == "Model training ready":
        message_queue.add_message_with_attachment(
            email_server,
            [recipient_email],
            EMAIL_SUBJECT,
            EMAIL_BODY_TEXT,
            EMAIL_BODY_HTML,
            "Image.png"
        )
    elif status == "Model training in process":
        message_queue.add_message_with_attachment(
            email_server,
            [recipient_email],
            EMAIL_SUBJECT2,
            EMAIL_BODY_TEXT2,
            EMAIL_BODY_HTML2,
            "Image.png"
        )
    elif status == "Model training completed":
        message_queue.add_message_with_attachment(
            email_server,
            [recipient_email],
            EMAIL_SUBJECT3,
            EMAIL_BODY_TEXT3,
            EMAIL_BODY_HTML3,
            "Image.png"
        )
    else:
        print(f"Unknown status: {status}. No email sent.")

    # Wait for all emails to be sent
    message_queue.wait_for_completion()
    message_queue.stop_processing()

    print("All emails have been sent. Check your inbox!")
    print("Thanks for watching!")
    print("-" * 88)

if __name__ == "__main__":
     usage_demo()