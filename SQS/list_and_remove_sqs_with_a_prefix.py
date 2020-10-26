__author__ = "Kevin P. Inscoe"
__copyright__ = "CC BY 4.0"
__credits__ = ["Kevin P. Inscoe"]
__license__ = "This work is licensed under a Creative Commons Attribution 4.0 International License."
__version__ = "4.0"
__maintainer__ = "https://kevininscoe.com"
__email__ = "kevin.inscoe@gmail.com"

import boto3
import pprint

pp = pprint.PrettyPrinter(indent=4)
region = "us-east-1"
profile = "pistons"

sqs_prefix = "demo-queues-"

# Assumes ~/.aws/credentials file exists and is being updated by okta-aws cli tool
boto3.setup_default_session(profile_name=profile, region_name=region)

sqs = boto3.client('sqs')

results = []

params = {
    'QueueNamePrefix': sqs_prefix,
    'MaxResults': 1000
}

while params.get('NextToken') != '':
    response = sqs.list_queues(**params)
    if 'QueueUrls' in response:
        results.extend(response['QueueUrls'])
        if 'NextToken' in response:
            params['NextToken'] = response['NextToken']
        else:
            params['NextToken'] = ''
    else:
        params['NextToken'] = ''
        print("No SQS queues found that start with %s" % (sqs_prefix))

for q in results:
    response = sqs.delete_queue(
        QueueUrl=q
    )
    status = response['ResponseMetadata']['HTTPStatusCode']
    print("Deleting %s ... %s" % (q, status))

print("\n%s queues found" % (len(results)))

