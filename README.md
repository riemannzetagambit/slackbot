[![PyPI](https://badge.fury.io/py/slackbot.svg)](https://pypi.python.org/pypi/slackbot) [![Build Status](https://secure.travis-ci.org/lins05/slackbot.svg?branch=master)](http://travis-ci.org/lins05/slackbot)

A chat bot for [Slack](https://slack.com) inspired by [llimllib/limbo](https://github.com/llimllib/limbo) and [will](https://github.com/skoczen/will).


## Setup

Follow all details over at the original repo that I forked, done by [lins05](https://github.com/lins05/slackbot). Then
come back here.

## Setting this up for your Slack channel

You'll need to make a file at `slackbot.authentication.py` that has at least the following structure:
```
SLACK_API_TOKEN = '**************'

IMGUR_CLIENT_ID = '**************'
IMGUR_CLIENT_SECRET = '**************'
IMGUR_REFRESH_TOKEN = '**************'
```
You'll have to get the tokens for all these APIs yourself. It is a good idea to have new ones issued every few months so
these don't go stale/turn into a security concern.

*Do not commit this file to your repo*. Note that it is included in the `.gitignore` for this reason.

After you've filled out the authentication information, simply `cd` into the `slackbot` dir and run `python run.py` on
any machine you'd like to host the bot (for me I am running this in a screen session on an AWS instance, but I should
daemonize it).

## Customizations from the original repo

* Single and multiple image querying (see `plugins/query_images.py` and other plugins contained in the `plugins/*`
  directory)
  - `<words> bomb me <N>` produces `N` random images from imgur matching seach query `words`
  - `show me <words>` produces a single random image from imgur matching search query `words`
  - Various cheeky responses matching certain regex patterns for a user pinging `diogenes` (or whatever you name your
    bot)
* More coming...


## TODO
These are mostly being used as learning experiences for me, so I'll add things of academic interest here as I go
* Implement NLP sentiment analysis of users' messages
* Dockerize the whole thing so anyone can deploy on whatever cloud service they want
