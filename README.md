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
You'll have to get the tokens for all these APIs yourself.

*Do not commit this file to your repo*. Note that it is included in the `.gitignore` for this reason.

## Customizations from the original repo

* Single and multiple image querying (see `plugins/query_images.py`)
* More coming...
