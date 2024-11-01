from platform_handlers.BaseHandler import BaseHandler
from utils.Log import get_logger


class RollbitHandler(BaseHandler):
    def __init__(self, info, message_queue, feedback_queue, config=None):
        self.platform_name = 'Rollbit'
        self.handler_id = info.get('handler_id', '未分配进程ID号')
        self.log_name = f'./Log/{self.platform_name}_{self.handler_id}.log'

        self.logger = get_logger(name=f'{self.platform_name}_{self.handler_id}', log_file=self.log_name,
                                 file_mode='a')

        super().__init__(info, message_queue, feedback_queue, config, platform_name=self.platform_name)
        # 这里可以添加 RollbitHandler 特有的初始化代码

    def click_bet_button_by_team_name(self, bet_info):
        return True

    def compare_and_verify_bet_odds(self, bet_info):
        return True

    def place_bet(self, bet_info):
        print(f'[{self.platform_name}--{self.handler_id}] 下单成功')
        pass

    def cancel_bet(self, bet_id):
        print(f'[{self.platform_name}--{self.handler_id}] 取消订单')
        pass

    def prepare_page(self, page):
        pass



