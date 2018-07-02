from slackclient import SlackClient


# TODO(dstone): do I need this class to inherit from something like slackclient.SlackClient?
# TODO(dstone): add documentation
class SlackTeamBot():
    def __init__(self, bot_api_token, oauth_api_token):
        self.bot_api_token = bot_api_token
        self.oauth_api_token = oauth_api_token
        # get the agents we'll use to do talking and access resources
        self.sc_bot = SlackClient(bot_api_token)
        self.sc_oauth = SlackClient(oauth_api_token)
        self.channel_list = self.sc_bot.api_call('channels.list')['channels']
        self.member_list = self.sc_bot.api_call("users.list")['members']
        self.user_names = None
        self.real_names = None
        self.channel_names = None

    def get_channel_names(self):
        if self.channel_names is None:
            self.channel_names = [channel['name'].lower() for channel in self.channel_list]
        return self.channel_names

    def get_user_names(self):
        if self.user_names is None:
            self.user_names = [member['name'].lower() for member in self.member_list]
        return self.user_names

    def get_real_names(self):
        if self.real_names is None:
            self.real_names = [member['real_name'].lower() for member in self.member_list]
        return self.real_names

    def get_user_id_from_user_name(self, user_name):
        name_to_check = user_name.lower().lstrip('@')
        user_names = self.get_user_names()
        real_names = self.get_real_names()
        if name_to_check in user_names:
            name_field = 'name'
        elif name_to_check in real_names:
            name_field = 'real_name'
        else:
            raise ValueError('Cannot find any user named (real or user name) {}!'.format(user_name))

        user_ids = [member['id'] for member in self.member_list if member[name_field].lower() == name_to_check]
        if len(user_ids) > 1:
            raise ValueError('Found more than one user matching the name you provided (!?).')
        else:
            user_id = user_ids[0]

        return user_id

    def get_channel_id_from_channel_name(self, channel_name):
        channel_to_check = channel_name.lower().lstrip('#')
        channel_names = self.get_channel_names()
        if channel_name not in channel_names:
            raise ValueError('Cannot find any channel named {}!'.format(channel_name))
        channel_ids = [channel['id'] for channel in self.channel_list if channel['name'].lower() == channel_to_check]
        if len(channel_ids) > 1:
            raise ValueError('Found more than one channel matching the name you provided (!?).')
        else:
            channel_id = channel_ids[0]

        return channel_id

    def get_message_objects(self, limit=None, channel_name=None, user_name=None):
        # TODO(dstone): make it so this grabs thread content and reactions as well
        if user_name is not None:
            user_id = self.get_user_id_from_user_name(user_name)
        else:
            user_id = None

        if channel_name is None:
            channel_ids = [channel['id'] for channel in self.channel_list]
        else:
            channel_ids = [self.get_channel_id_from_channel_name(channel_name)]

        latest, message_objects = None, []
        for channel_id in channel_ids:
            more_messages = True
            # TODO(dstone): this actually grabs by channel first, rather than by time stamp.
            # Need to order by time stamp at some point and return by that limit. Note 'channel' is required for the 'conversation.history' API call
            while more_messages and (limit is None or limit > 0):
                if limit is not None:
                    # restrict to 100 message maximum if still requesting more than that
                    limit_to_call = min(limit, 100)
                else:
                    # choose maximum allowable number of message_objects to request at a time
                    limit_to_call = 100
                conversation_history = self.sc_oauth.api_call("conversations.history",
                                                              channel=channel_id,
                                                              limit=limit_to_call,
                                                              latest=latest
                                                             )

                latest_messages = conversation_history['messages']
                latest = latest_messages[-1]['ts']
                more_messages = conversation_history['has_more']

                if user_id is not None:
                    # filter if you are requesting a specific user's messages
                    latest_messages = [message_object for message_object in latest_messages if message_object['user'] == user_id]
                # do this afterward to check for messages by user_id
                if limit is not None:
                    # only decrement by how many messages you actually got
                    limit = limit - len(latest_messages)
                message_objects.extend(latest_messages)

        return message_objects

    def get_messages(self, **kwargs):
        message_objects = self.get_message_objects(**kwargs)
        return [message['text'] for message in message_objects]

    def get_messages_for_user(self, user_name, **kwargs):
        kwargs['user_name'] = user_name
        message_objects = self.get_message_objects(**kwargs)
        return [message['text'] for message in message_objects]# if message['user'] == user_id]
