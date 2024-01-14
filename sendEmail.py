import boto3
from botocore.exceptions import ClientError
import sys
import simrepsConfig

dynamodb = boto3.resource('dynamodb',
                           region_name=simrepsConfig.aws_region,
                           aws_access_key_id=simrepsConfig.aws_access_key_expanded,
                           aws_secret_access_key=simrepsConfig.aws_secret_key_expanded
                        )
ses = boto3.client('ses',
                    region_name=simrepsConfig.aws_region,
                    aws_access_key_id=simrepsConfig.aws_access_key_expanded,
                    aws_secret_access_key=simrepsConfig.aws_secret_key_expanded)

emTable = dynamodb.Table('simrepsEmail')

def main(userName):
    try:
        print(userName + ' should have gotten a response')
    except:
        print('there is something wrong with the username')    
    
    #get the email address from dynamo email table
    response = emTable.get_item(Key={'userName':str(userName)},AttributesToGet=['email'])
    try:
        print('here is the email db response',response)
    except:
        print('something is wrong with response')

    SENDER = 'simrepsanalysis@bio-rad.com'
    RECIPIENT = response['Item']['email']

    AWS_REGION = simrepsConfig.aws_region
    SUBJECT = "Your SiMREPs Files Have Been Uploaded"
    #BODY_TEXT = ("Amazon SES Test (Python)\r\n"
    # "This email was sent with Amazon SES using the "
    # "AWS SDK for Python (Boto)."
    #)
    BODY_HTML = """<html>
            <head></head>
            <body>
              <h1>Your SiMREPs Files Are Ready</h1>
              <p>Your file list can be filtered, retrieved and/or analyzed at <a href='https://smd.lsg-applications.com/'>SiMREPs App</a><p>
            </body>
            </html>
            """
    CHARSET = "UTF-8"
    try:
        #Provide the contents of the email.
        response = ses.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    }#,
    #                'Text': {
    #                    'Charset': CHARSET,
    #                    'Data': BODY_TEXT,
    #                },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
            # If you are not using a configuration set, comment or delete the
            # following line
            #ConfigurationSetName=CONFIGURATION_SET,
        )
    # Display an error if something goes wrong.
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])

#if __name__ =='__main__':
#    main(sys.argv[1],sys.argv[2])