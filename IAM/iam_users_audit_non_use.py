# Report on AWS IAM users the last time they used the console or API access

# Code is designed to be run on AWS Lambda but van be run via command line given the environment variables are set

from __future__ import print_function
import boto3
import os
import json
import pprint
import datetime

pp = pprint.PrettyPrinter(indent=4)

# For testing in desktop
profile = "testing"

if "REGION" in os.environ:
    region = os.environ['REGION']
else:
    region = "us-east-1"
if "DEBUG" in os.environ:
    dbg = os.environ['DEBUG']
else:
    dbg = "yes"
d = dbg.lower()
if (d == "yes") or (d == "true"):
    debug = True

def lambda_handler(event, context):
    total = 0

    if event != {}:
        client = boto3.client('iam', region_name=region)
    else:
        boto3.setup_default_session(profile_name=profile)
        client = boto3.client('iam', region_name=region)

    response = client.list_users(
    )

    print("%s\n" % (datetime.datetime.now()))

    # Filter and list users who match criteria
    for u in response['Users']:
        user = u['UserName']
        createdt = u['CreateDate']

        # Get access keys for this account
        userr = client.get_user(
            UserName=user
        )
        userdata = userr['User']
        if 'PasswordLastUsed' in userdata:
            lastpw = userdata['PasswordLastUsed']
        else:
            lastpw = "[Never]"

        print("%s Password last used: %s, [User created: %s]" % (user, lastpw, createdt))

        # Get list of keys for this user
        rk = client.list_access_keys(
            UserName=user,
        )

        if 'AccessKeyMetadata' in rk:
            for a in rk['AccessKeyMetadata']:
                ak = a['AccessKeyId']
        # Get last time access keys was used
                k = client.get_access_key_last_used(
                    AccessKeyId=ak
                )
                keydata = k['AccessKeyLastUsed']
                if 'LastUsedDate' in keydata:
                    print("   Access key last used: %s" % (keydata['LastUsedDate']))

    return True



if __name__ == "__main__":
    # use this for testing on desktop (PyCharm)

    event = {}
    context = ''

    result = lambda_handler(event, context)

