from botocore.exceptions import ClientError

class SesTemplate:
    def __init__(self, client):
        self.client = client
        self.template = None

    def create_template(self, name, subject, text, html):
        self.template = {
            'TemplateName': name,
            'SubjectPart': subject,
            'TextPart': text,
            'HtmlPart': html
        }
        try:
            self.client.create_template(Template=self.template)
        except ClientError as e:
            if e.response['Error']['Code'] == 'AlreadyExists':
                print(f"Template {name} already exists.")
            else:
                print(f"Error creating template: {e.response['Error']['Message']}")

    def delete_template(self):
        try:
            self.client.delete_template(TemplateName=self.template['TemplateName'])
            print("Template deleted.")
        except ClientError as e:
            print(f"Error deleting template: {e.response['Error']['Message']}")

    def name(self):
        return self.template['TemplateName']

    def verify_tags(self, tags):
        return all(key in tags for key in ['name', 'action'])