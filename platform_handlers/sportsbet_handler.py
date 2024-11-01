from platform_handlers.BaseHandler import BaseHandler
from utils.Log import get_logger
from typing import Union, Optional, Dict


class SportsbetHandler(BaseHandler):
    def __init__(self, info, message_queue, feedback_queue, config=None):
        self.platform_name = 'Rollbit'
        self.handler_id = info.get('handler_id', '未分配进程ID号')
        self.log_name = f'./Log/{self.platform_name}_{self.handler_id}.log'

        self.logger = get_logger(name=f'{self.platform_name}_{self.handler_id}', log_file=self.log_name,
                                 file_mode='a')

        super().__init__(info, message_queue, feedback_queue, config, platform_name=self.platform_name)
        # 这里可以添加 RollbitHandler 特有的初始化代码

    def click_bet_button_by_team_name(self, bet_info:dict)->bool:
        button = None
        button_dict = self.page_obj.find_game_name_button(page=self.page, bet_info=bet_info)
        if not button_dict:
            return False

        if bet_info['betting_team_name'].lower() == 'draw':
            button = button_dict.get('draw')
        if bet_info['betting_team_name'].lower() == bet_info['home_team_name'].lower():
            button = button_dict.get('home_team')
        if bet_info['betting_team_name'].lower() == bet_info['guest_team_name'].lower():
            button = button_dict.get('guest_team')

        if button:
            button.click()
            return True
        return False

    def compare_and_verify_bet_odds(self, bet_info:dict, ) -> Union[bool]:
        # this function have three steps
        # first: get the odd value from webpage,then compare with the spider odd.
        # second: get the input element ,then input a number
        # three: check the place button is enabled or not
        spider_odd = bet_info['betting_odds']
        odd_div_ele = self.page_obj.find_check_odd_div(page=self.page, bet_info=bet_info)
        if not odd_div_ele:
            return False
        try:
            odd = float(odd_div_ele.text)
            if odd == spider_odd:
                input_el = self.page_obj.find_input_box(page=self.page, bet_info=bet_info)
                if not input_el:
                    self.logger.warning(f'find input box fail')
                    return False
                input_el.input(1)
                place_bet_button = self.page_obj.find_place_bet_button(page=self.page)
                if not place_bet_button:
                    self.logger.warning(f'find place bet button fail')
                    return False
                if place_bet_button.is_enabled():
                    self.logger.info(f'place bet button is enabled')
                    return True
                else:
                    self.logger.warning(f'place bet button is disabled')
                    return False
        except Exception as e:
            self.logger.error(f'compare_and_verify_bet_odds error: {e}')
            return False

    def place_bet(self, bet_info:dict) -> Optional[bool]:
        order_amount = bet_info['order_amount']
        input_ele = self.page_obj.find_input_box(sr=self.sr)
        if not input_ele:
            self.logger.warning(f'find input box fail')
            return False
        try:
            input_ele.input(order_amount)
            self.logger.info(f'input order amount: {order_amount} success')
        except Exception as e:
            self.logger.warning(f'input order amount: {order_amount} fail, error: {e}')
            return False

        place_bet_button = self.page_obj.find_place_bet_button(page=self.page)
        if not place_bet_button:
            self.logger.warning(f'find place bet button fail')
            return False
        if place_bet_button.is_enabled():
            self.logger.info(f'place bet button is enabled')
            try:
                place_bet_button.click()
                self.logger.info(f'place bet success')
                return True
            except Exception as e:
                self.logger.warning(f'place bet fail, error: {e}')
                return False
        return False

    def cancel_bet(self, bet_id):
        bet_info = self.pending_bets.get(bet_id, {}).get('message')
        close_button = self.page_obj.find_close_button(page=self.page,bet_info=bet_info)
        if not close_button:
            self.logger.warning(f'find close button fail')
            self.logger.error(f'cancel bet fail, bet_id: {bet_id}')
            return False
        try:
            close_button.click()
            self.logger.info(f'cancel bet success, bet_id: {bet_id}')
            return True
        except Exception as e:
            self.logger.warning(f'cancel bet fail, error: {e}')
            return False

    def prepare_page(self, page):
        self.page_obj.open_svgs(page)
