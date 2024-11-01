from platform_handlers.BaseHandler import BaseHandler
import time
from utils.Log import get_logger

# 测试导入包
from DrissionPage import ChromiumPage, ChromiumOptions
from settings import ADS
import requests



class RollbitHandler(BaseHandler):
    def __init__(self, info, message_queue, feedback_queue, config=None):
        self.platform_name = 'Rollbit'
        self.handler_id = info.get('handler_id', '未分配进程ID号')
        self.log_name = f'./Log/{self.platform_name}_{self.handler_id}.log'

        self.logger = get_logger(name=f'{self.platform_name}_{self.handler_id}', log_file=self.log_name,
                                 file_mode='w')

        super().__init__(info, message_queue, feedback_queue, config, platform_name=self.platform_name)

        self.sr = None

    def click_bet_button_by_team_name(self, bet_info):
        if not self.sr:
            self.sr = self.page_pom_obj.find_shadow_root()
        # todo 这里需要判断是不是买平局
        if bet_info['betting_team_name'].lower() == 'draw':
            brother_name = bet_info['game_name'].split('--')[0].strip().lower()
            button = self.page_pom_obj.find_button_1_brother(sr=self.sr, bet_info=bet_info,brother_name=brother_name)
        else:
            button = self.page_pom_obj.find_button_1(self.sr,bet_info)

        # 检查button是否存在
        if button:
            button.click()
            self.logger.info(f'[主页面下单] 点击按钮成功')
            return True
        else:
            self.logger.warning(f'[主页面下单] 未找到按钮')
            return False

    def compare_and_verify_bet_odds(self, bet_info):
        odds_ele = self.page_obj.find_check_odds(sr=self.sr,bet_info=bet_info)
        # todo 核对赔率值是否被覆盖了。
        if odds_ele:
            if not odds_ele.status.is_covered:
                self.logger.info(f'赔率没有被覆盖')
                try:
                    odds = float(odds_ele.text)
                except Exception as e:
                    self.logger.error(f'获取下单界面的赔率无法转换为数值{e}')
                    return False
            else:
                self.logger.info(f'赔率被覆盖')
                return False
        else:
            self.logger.warning(f'未找到赔率元素')
            return False

        #  todo 核对赔率值与爬虫赔率值是否相同。
        if odds == bet_info['odds']:
            print("赔率一致,达到下单条件")
            # todo 进行下单按钮是否可以点击的检查
            try:
                place_bet_button = self.page_obj.find_place_bet_button(sr=self.sr)
                if place_bet_button:
                    if place_bet_button.states.is_enabled:
                        self.logger.info(f'下单按钮可以点击')
                        return True
                    else:
                        self.logger.warning(f'下单按钮不可点击')
                        return False
                else:
                    return False
            except Exception as e:
                self.logger.error(f'下单按钮是否可以点击的检查失败{e}')
        else:
            return False

    def place_bet(self, bet_info):
        # todo 输入金额
        order_amount = bet_info['order_amount']
        input_ele = self.page_obj.find_input_element(sr=self.sr)
        if input_ele:
            input_ele.input(order_amount)
            self.logger.info(f'输入金额{order_amount}')
        else:
            return False
        # todo 点击下单
        place_bet_button = self.page_obj.find_place_bet_button(sr=self.sr)
        if place_bet_button:
            place_bet_button.click()
        else:
            return False

    def cancel_bet(self, bet_id):
        print(f'[{self.platform_name}--{self.handler_id}] 取消订单')
        bet_info = self.pending_bets.get(bet_id, {}).get('message')
        close_ele = self.page_obj.find_close_button(sr=self.sr,bet_id=bet_info)
        if close_ele:
            close_ele.click()
            return True
        else:
            return False



    def prepare_page(self,page):
        try:
            self.sr = self.page_pom_obj.find_shadow_root()
        except Exception as e:
            self.logger.error(f'获取sr失败{e}')






