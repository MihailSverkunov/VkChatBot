import random

from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

from _token import token

GROUP_ID = 207897461

class Bot:
    def __init__(self, group_id, token):
        self.token = token
        self.group_id = group_id
        self.vk = VkApi(token=token)
        self.long_poll = VkBotLongPoll(vk=self.vk, group_id=group_id)
        self.api = self.vk.get_api()

    def run(self):
        for event in self.long_poll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                self._on_new_message(event)

    def _on_new_message(self, event):

        if(self.api.groups.isMember(access_token=self.token,
                                    group_id=self.group_id,
                                    user_id=event.message.from_id)):
            self._send_message(event=event,
                               message=f'Привет, бро! Ты случайно не писал мне: "{event.message.text}"?'
                               )
        else:
            self._send_message(event=event, message='Привет, незнакомец!')


    def _send_message(self, event, message):
        random_id = random.randint(0, 2 ** 12)
        self.api.messages.send(token=self.token,
                               message=message,
                               peer_id=event.message.peer_id,
                               random_id=random_id
                               )

if __name__ == '__main__':
    bot = Bot(GROUP_ID, token)

    bot.run()