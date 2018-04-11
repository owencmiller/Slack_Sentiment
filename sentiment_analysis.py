import json
import os
import time
import re
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from slackclient import SlackClient

slack_client = SlackClient(os.environ.get("SLACK_BOT_TOKEN"))
sentiment_bot_id = None
sc = SlackClient(os.environ["SLACK_API_TOKEN"])


RTM_READ_DELAY = 1  # 1 second delay
EXAMPLE_COMMAND = "help"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"

def parse_bot_commands(slack_events):
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == sentiment_bot_id:
                return message, event["channel"]
    return None, None


def parse_direct_mention(message_text):
    matches = re.search(MENTION_REGEX, message_text)
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)


def handle_command(command, channel):
    default_response = "Unknown input. Try *{}*.".format(EXAMPLE_COMMAND)
    response = None

    if len(command.split()) > 1:
        output = command.split(' ', 1)[1]
    else:
        output = ''
    sid = SentimentIntensityAnalyzer()
    if command.startswith("help"):
        response = 'Welcome to the Sentiment Analysis App for Slack!\n'
        response += 'Usage:\thelp - display this message\n'
        response += '\t\t\t\tthis your_message - analysis on your message\n'
        response += '\t\t\t\tlast n - analysis on the previous n messages\n'

    elif command.startswith("this"):
        ss = sid.polarity_scores(output)
        
        

    elif command.startswith("last"):
        response = ''
        count = int(output)
        history = sc.api_call("channels.history", channel=channel, count=count+1)
        if count > len(history["messages"]):
            response += 'Count is too high'
        else:
            del history["messages"][0]
            
            messages = [history["messages"][i]["text"] for i in range(count)]
            polarity_scores = [sid.polarity_scores(message) for message in messages]
            neg_scores = [score['neg'] for score in polarity_scores]
            pos_scores = [score['pos'] for score in polarity_scores]
            compound_scores = [score['compound'] for score in polarity_scores]
            
            avg_neg = sum(neg_scores) / len(neg_scores)
            avg_pos = sum(pos_scores) / len(pos_scores)
            avg_compound = sum(compound_scores) / len(compound_scores)
            
            response += 'Sentiment over the last {0} messages -\n'.format(count)
            response += 'Average Negativity: {0}\n'.format(avg_neg)
            response += 'Average Positivity: {0}\n'.format(avg_pos)
            response += 'Average Compound: {0}\n'.format(avg_compound)

    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response
    )


if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Sentiment Bot connected and running!")
        sentiment_bot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel = parse_bot_commands(slack_client.rtm_read())
            if command:
                handle_command(command, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")


