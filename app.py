import logging
import os
from slack_bolt import App
from slack_bolt.oauth.oauth_settings import OAuthSettings

# logging.basicConfig(level=logging.DEBUG)

app = App(
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET"),
    token=os.environ.get("SLACK_BOT_TOKEN"),

    # OAuth
    # oauth_settings=OAuthSettings(
    #     client_id=os.environ.get("SLACK_CLIENT_ID"),
    #     client_secret=os.environ.get("SLACK_CLIENT_SECRET"),
    #     scopes=["app_mentions:read", "channels:history",
    #             "im:history", "chat:write", "commands"],
    # )
)


@app.event("app_mention")
def reply_to_mention(event, client, logger):
    """
    You can listen to any Events API event using the event()
    listener after subscribing to it in your app configuration.

    Note: your app *must* be present in the channels where it
    is mentioned.

    Please see the 'Event Subscriptions' and 'OAuth & Permissions'
    sections of your app's configuration to add the following for
    this example to work:

    Event subscription(s):   app_mentioned, messages.channels
    Required scope(s):       app_mentions:read, chat:write

    Further Information & Resources
    https://slack.dev/bolt-python/concepts#event-listening
    https://api.slack.com/events
    """
    try:
        text = f"Thanks for the mention, <@{event['user']}>! How can I help?"
        client.chat_postMessage(channel=event['channel'], text=text)
    except Exception as e:
        logger.error(f"Error responding to app_mention: {e}")


@app.message("hello")
def reply_to_keyword(message, say, logger):
    """
    Messages can be listened for, using specific words and phrases.
    message() accepts an argument of type str or re.Pattern object
    that filters out any messages that don’t match the pattern.

    Note: your app *must* be present in the channels where this
    keyword or phrase is mentioned.

    Please see the 'Event Subscriptions' and 'OAuth & Permissions'
    sections of your app's configuration to add the following for
    this example to work:

    Event subscription(s):  message.channels
    Required scope(s):      channels:history, chat:write

    Further Information & Resources
    https://slack.dev/bolt-python/concepts#message-listening
    https://api.slack.com/messaging/retrieving
    """
    try:
        blocks = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Hi there! Here's a button to click!"
                },
                "accessory": {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Click Button",
                    },
                    "value": "button_value",
                    "action_id": "first_button"
                }
            }
        ]
        say(blocks=blocks)
    except Exception as e:
        logger.error(f"Error responding to message keyword 'hello': {e}")


@app.action("first_button")
def respond_to_button_click(action, ack, say, logger):
    """
    Interactivity is all about action taken by the user! Actions
    can be filtered using an `action_id`, which acts as unique
    identifier for interactive components on the Slack platform.

    Note: you *must* subscribe to Interactivity to receive actions.

    Please see the 'Event Subscriptions' and 'OAuth & Permissions'
    sections of your app's configuration to add the following for
    this example to work:

    Event subscription(s):  none
    Required scope(s):      chat:write

    Further Information & Resources
    https://slack.dev/bolt-python/concepts#action-listening
    https://api.slack.com/interactivity
    """
    ack()
    try:
        say("You clicked the button!")
    except Exception as e:
        logger.error(f"Error responding to 'first_button' button click: {e}")


@app.shortcut("launch_simple_modal")
def open_modal(ack, shortcut, client, logger):
    """
    Shortcuts are invokable entry points to apps. Global shortcuts
    are available from within search in Slack and message shortcuts
    are available in the context menus of messages.

    Note: you *must* subscribe to Interactivity to enable shortcuts.

    Please see the 'Event Subscriptions' and 'OAuth & Permissions'
    sections of your app's configuration to add the following for
    this example to work:

    Event subscription(s):  none
    Required scope(s):      commands

    Further Information & Resources
    https://slack.dev/bolt-python/concepts#shortcuts
    https://api.slack.com/interactivity/shortcuts
    """
    ack()

    try:
        client.views_open(
            trigger_id=shortcut["trigger_id"],
            view={
                "type": "modal",
                "title": {"type": "plain_text", "text": "My App"},
                "close": {"type": "plain_text", "text": "Close"},
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": """About the simplest modal you could conceive of :smile:\n\nMaybe <https://api.slack.com/reference/block-kit/interactive-components|*make the modal interactive*> or <https://api.slack.com/surfaces/modals/using#modifying|*learn more advanced modal use cases*>."""
                        }
                    },
                    {
                        "type": "context",
                        "elements": [
                            {
                                "type": "mrkdwn",
                                "text": "Psssst this modal was designed using <https://api.slack.com/tools/block-kit-builder|*Block Kit Builder*>"
                            }
                        ]
                    }
                ]
            })
    except Exception as e:
        logger.error(f"Error opening modal: {e}")


@app.event("app_home_opened")
def publish_home_view(client, event, logger):
    """
    The Home tab is a persistent, yet dynamic interface for apps.
    The user can reach the App Home from the conversation list
    within Slack or by clicking on the app's name in messages.

    Note: you *must* enable Home Tab (App Home > Show Tabs Section)
    to receive this event.

    Please see the 'Event Subscriptions' and 'OAuth & Permissions'
    sections of your app's configuration to add the following:

    Event subscription(s):  app_home_opened
    Required scope(s):      none

    Further Information & Resources
    https://slack.dev/bolt-python/concepts#app-home
    https://api.slack.com/surfaces/tabs
    """
    try:
        client.views_publish(
            user_id=event["user"],
            view={
                "type": "home",
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*Welcome home, <@{event['user']}> :house:*"
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "Learn how home tabs can be more useful and interactive <https://api.slack.com/surfaces/tabs/using|*in the documentation*>."
                        }
                    }
                ]
            }
        )
    except Exception as e:
        logger.error(f"Error publishing view to Home Tab: {e}")


if __name__ == "__main__":
    app.start(3000)  # POST http://localhost:3000/slack/events
