import praw
import re
import datetime
import json

def response():
    reddit = praw.Reddit(user_agent='Leauge Subreddit Headline Reader (by /u/flaminwhale)',
    client_id="xpGSLkCmB14z_A",
    client_secret="5yX47a2q7O_fj2VLMG747n5J1Z8")
    headlineList = []
    for submission in reddit.subreddit('boston').top(limit=100, time_filter='day'):
        #ignore content not likely to be a news headline
        if not re.search(r'i.redd.it|imgur|flickr|youtube|i.reddituploads|gyfcat|www.reddit.com', submission.url):
            headlineList.append(
                {
                    'uid': submission.id,
                    'updateDate': datetime.datetime.utcnow().isoformat() + 'Z',
                    'titleText': '/r/boston news',
                    'mainText': submission.title,
                    'redirectionUrl': submission.url
                }
            )
        # stop once we've read all of the 'most popular' stuff, as marked by an arbitrary cutoff score
        if submission.score < 30:
            break

    return {
        'statusCode': '200',
        'body': json.dumps(headlineList),
        'headers': {
            'Content-Type': 'application/json',
        },
    }

def lambda_handler(event, context):
    return response()
