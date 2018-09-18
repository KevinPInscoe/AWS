#
# Create an AWS Tag Word Cloud for you instances
#

# kevin@inscoe.org

import boto3
import pprint
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

pp = pprint.PrettyPrinter(indent=4)

profiles = ['gemini', 'bordetello', 'dev-test', 'prod', 'pre-stage']

def all_tags(profiles, tagname):
    r = []
    tags=[]

    for p in profiles:
        r = get_cost_tags(p, tagname)
        tags.extend(r)

    return (tags)

def get_cost_tags(p, tagname):
    tags = []
    next = ""
    boto3.setup_default_session(profile_name=p, region_name='us-east-1')
    client = boto3.client('ec2')
    while next != "END":
        if next != "":
            response = client.describe_instances(
                NextToken=next
            )
        else:
            response = client.describe_instances()

        acct = response['Reservations'][0]['OwnerId']
        acct.replace(" ", "")
        for r in response['Reservations']:
            for i in r['Instances']:
                if 'Tags' in i:
                    for tag in i['Tags']:
                        if tag['Key'] == tagname:
                            tagvalue = tag['Value']
                            tags.append(tagvalue)
        if 'NextToken' in response:
            next = response['NextToken']
        else:
            next = 'END'

    return tags


if __name__ == "__main__":
    tagname = "Project"
    tags = []
    tags = all_tags(profiles, tagname)
    words = ''
    for tag in tags:
        words = words + " " + str(tag)

    print(words)

    stopwords = set(STOPWORDS)

    wordcloud = WordCloud(width=800, height=800,
        background_color='white',
        stopwords=stopwords,
        min_font_size=10).generate(words)

    # plot the WordCloud image
    plt.figure(figsize=(8, 8), facecolor=None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)

    plt.show()


