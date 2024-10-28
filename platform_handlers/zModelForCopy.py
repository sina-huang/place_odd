from platform_handlers.BaseHandler import BaseHandler


class RollbitHandler(BaseHandler):
    def __init__(self, info):
        super().__init__(info)

    def __str__(self):
        return 'RollbitHandler对象'


    def place_bet(self,info):
        print('Rollbit收到',info)

    def prepare_page(self):
        pass
        # return info