# Bolt for Python Demo App (November 2020)

This is a basic example app showing off just some of the functionality available in [Bolt for Python](https://slack.dev/bolt-python/tutorial/getting-started). 

Local development requires a public URL where Slack can send requests. In this guide, we'll be using [`ngrok`](https://ngrok.com/download). Checkout [this guide](https://api.slack.com/tutorials/tunneling-with-ngrok) for setting it up.

Before we get started, make sure you have a development workspace where you have permissions to install apps. If you don’t have one setup, go ahead and [create one](https://slack.com/create). You also need to [create a new app](https://api.slack.com/apps?new_app=1) if you haven’t already.

## Install Dependencies

```
pip install -r requirements.txt
```

## Add Scopes & Install App to Workspace

In your [**App Config**](https://api.slack.com/apps), after selecting your app, navigate to **OAuth & Permissions**. Add the `channels:read`, `app_mentions:read`, `commands` and `chat:write` permissions. 

Click **Install App** to install the app to your workspace and generate a bot token. This bot token will be used in your app as the `SLACK_BOT_TOKEN` environment variable.

## Setup Environment Variables

This app requires that you setup environment variables. 

You can get these values by navigating to your [**App Config**](https://api.slack.com/apps) and visiting the **Basic Information** and **OAuth & Permissions** pages.

```
export SLACK_BOT_TOKEN=YOUR_SLACK_BOT_TOKEN
export SLACK_SIGNING_SECRET=YOUR_SLACK_SIGNING_SECRET
```

If using OAuth, you'll use the following:

```
export SLACK_SIGNING_SECRET=YOUR_SLACK_SIGNING_SECRET
export SLACK_CLIENT_ID=YOUR_SLACK_CLIENT_ID
export SLACK_CLIENT_SECRET=YOUR_SLACK_CLIENT_SECRET
export SLACK_SCOPES=YOUR_SLACK_SCOPES
```

## Run the App

Start the app with the following command:

```
python app.py
```

This will start the app on port `3000`.

## Create Public URL with ngrok

Using `ngrok`, we can access the app on an external network and create a **Redirect URL** for OAuth and **Request URL** for Event Subscriptions and Interactivity:

```
ngrok http 3000
```

The above should output a forwarding address for `http` and `https`. The `https` address should look something like the following:

```
Forwarding   https://3cb89939.ngrok.io -> http://localhost:3000
```

## Subscribe to Events

On the **Events Subscriptions** page, after opting in, the **Request URL** should be set to your `ngrok` forwarding address with the `slack/events` path appended.

The **Request URL** should look something like this:

```
https://3cb89939.ngrok.io/slack/events
````

Click **Subscribe to bot events** and add `app_home_opened`, `app_mentioned`, and `message.channels` to the events your app is subscribed to.  

## Subscribe to Interactivity
On the **Interactivity & Shortcuts** page, after opting in, the **Request URL** should be set to the same `ngrok` forwarding address that you used in the **Event Subscriptions** page above.

## Enable Home Tab

In the **App Home** page, navigate to the **Show Tabs** section and enable the **Home Tab**. 

## Define Redirect URL for OAuth (optional)

On the **OAuth & Permissions** page, add a **Redirect URL**. This **Redirect URL** should be set to your `ngrok` forwarding address with the `slack/oauth_redirect` path appended.

The **Redirect URL** should look something like this:

```
https://3cb89939.ngrok.io/slack/oauth_redirect
```