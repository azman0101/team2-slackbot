import os
import time
from slackclient import SlackClient

from chatterbot import ChatBot

chatbot = ChatBot(
    'marvin',
    trainer='chatterbot.trainers.ChatterBotCorpusTrainer'
)

# Train based on the english corpus
chatbot.train("chatterbot.corpus.french")
chatbot.train('chatterbot.corpus.french.greetings')
chatbot.train('chatterbot.corpus.french.trivia')

# starterbot's ID as an environment variable
#BOT_ID = os.environ.get("BOT_ID")

BOT_NAME = 'marvin'

# constants
AT_BOT = None

DO = "do"
MAKE = "make"
COFFEE = "coffee"

# instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

list = slack_client.api_call("channels.list")

def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = "Error: Does not compute."
    if command is DO:
        response = "Do it yourself ..."
    elif command is MAKE:
        response = "Make it yourself ..."
    elif command is COFFEE:
        response = "Here you go :coffee:"
    else:
        # Get a response to an input statement
        statement = chatbot.get_response(command)
        response = statement.text

    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)

def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None


if __name__ == "__main__":
    api_call = slack_client.api_call("users.list")
    if api_call.get('ok'):
        # retrieve all users so we can find our bot
        users = api_call.get('members')
        for user in users:
            if 'name' in user and user.get('name') == BOT_NAME:
                print("Bot ID for '" + user['name'] + "' is " + user.get('id'))
                AT_BOT = "<@" + user.get('id') + ">"
    else:
        print("could not find bot user with the name " + BOT_NAME)
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
