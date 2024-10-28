

from platform_handlers.BaseHandler import BaseHandler
from DrissionPage import ChromiumPage, ChromiumOptions

class StakeHandler(BaseHandler):
    def __init__(self, info,message_queue):
        super().__init__(info,message_queue)

    def __str__(self):
        return 'StakeHandler对象'

    def place_bet(self, bet_info):
        print('Stake收到',bet_info)
        pass

    def prepare_page(self,page):
        pass
