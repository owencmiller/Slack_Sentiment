# Slack_Sentiment
A Sentiment Analysis User Bot for Slack

### Creation

* Create a User Bot in the Slack interface
* Set desired name for the bot, we will be using SentimentBot
* Set the API and Bot tokens
        
        export SLACK_API_TOKEN='your Oauth api token'
        export SLACK_BOT_TOKEN='your Bot User Oauth token'

* Add the Bot User to your desired public channel


### Commands

These commands can be typed directly into Slack. Use @SentimentBot before each command.

        help     - view available commands
        last [n] - analyze the previous n messages
        this [message] - analyze the succeeding message

