from platform_handlers.BaseHandler import BaseHandler
from DrissionPage import ChromiumPage, ChromiumOptions
import time
from pprint import pprint
from utils.Log import get_logger


class StakeHandler(BaseHandler):
    def __init__(self, info, message_queue, feedback_queue, config=None):
        self.platform_name = 'Stake'
        self.handler_id = info.get('handler_id', '未分配进程ID号')
        self.log_name = f'./Log/{self.platform_name}_{self.handler_id}.log'

        self.logger = get_logger(name=f'{self.platform_name}_{self.handler_id}', log_file=self.log_name,
                                 file_mode='w')

        super().__init__(info, message_queue, feedback_queue, config, platform_name=self.platform_name)


        self.xpath_templates = {
            "bet_button_on_game_page": "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{name}')]",
            "span_on_all_page": "//span[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{name}')]",
            "input_on_bet_page": "//div[@id='right-sidebar']//div[contains(@class,'footer')]//input",
            "confirm_bet_button_on_bet_page": "//div[@id='right-sidebar']//div[contains(@class,'footer')]//button"
        }



    def click_bet_button_by_team_name(self, bet_info):
        """
        step 1 : 拿到投注队伍名称
        step 2 : 根据队伍名称点击投注按钮
        """
        betting_team_name = bet_info['betting_team_name'].lower()
        print(betting_team_name)
        if bet_info['betting_team_name'].lower() == 'draw':
            brother_name = bet_info['game_name'].split('--')[0].strip().lower()
            brother_dict = {'betting_team_name': brother_name}
            brother_button = self.page_pom_obj.find_button_1(brother_dict)
            if not brother_button:
                self.logger.info(f"Draw订单，未找到下单按键的兄弟按钮：{brother_name}")
                return False

            button = self.page_pom_obj.find_button_2(brother_button)
            if not button:
                self.logger.info(f"Draw订单，未找到主页面中下单按键")
                return False
        else:
            # 如果不是平局，可以直接去找button
            button = self.page_pom_obj.find_button_1(bet_info)
            if not button:
                self.logger.info(f"Draw订单，未找到主页面中下单按键")
                return False

        # todo 判断是否可以点击，如果已经封盘则无法点击
        if button and button.states.is_enabled:

            button.click()
            self.logger.warning(f"点击下单按钮成功：{betting_team_name}")
            return True
        else:
            self.logger.info(f"按钮不可用或未找到：{betting_team_name}")
            return False

    def compare_and_verify_bet_odds(self, bet_info):
        # todo 先找到当前下单块，然后在下单块中找当前赔率


        # todo step-1 拿到下单页面中的赔率数据
        odd_span_ele = self.page_pom_obj.wait_spans_refresh(bet_info)
        if not odd_span_ele:
            print("赔率数据获取失败")
            return False
        try:
            odd = float(odd_span_ele.next().text)
        except Exception as e:
            print(f'赔率转换失败{e}')
            return False

        # 比较下单页面中的赔率数据
        spider_odds = bet_info['odds']
        if odd == spider_odds:
            print("赔率一致,达到下单条件")
            try:
                input_ele = self.page_pom_obj.find_input_ele()
                if input_ele:
                    self.logger.info(f"找到下单输入框，开始输入金额：1")
                    input_ele.input(1)
                else:
                    print("未找到下注输入框")
                    return False
            except Exception as e:
                print(f'input框无法输入,报错{e}')

            # 判断下单按钮是否可用
            button = self.page_pom_obj.check_button_is_available()
            if button:
                if button.states.is_enabled:
                    self.logger.info(f'下单按钮可用')
                    return True
                else:
                    self.logger.warning(f'下单按钮不可用')
                    return False
            else:
                return False

    def place_bet(self, bet_info):
        # 输入下单金额
        order_amount = bet_info['order_amount']
        input_ele = self.page_pom_obj.find_input_ele()
        if input_ele:
            self.logger.info(f"找到下单输入框，开始输入金额：{order_amount}")
            input_ele.clear()
            input_ele.input(order_amount)
        else:
            self.logger.info(f"未找到下单输入框")
            return False

        # 下单
        button = self.page_pom_obj.check_button_is_available()

        if button.states.is_enabled:
            self.logger.info(f'下单按钮可用')
            button.click()
        else:
            self.logger.warning(f'下单按钮不可用')
            return False

    def cancel_bet(self, bet_id):
        time.sleep(2)
        button = self.page_pom_obj.find_button_clean_all()
        if button:
            self.logger.info(f"取消所有订单")
            button.click()
            return True
        else:
            return False

    def prepare_page(self, page):
        pass



    def get_dp_xpath(self, key, **kwargs):
        """
        根据键名和参数，生成实际的 dp_xpath。
        :param key: XPath 模板的键名
        :param kwargs: 动态参数，用于替换 XPath 模板中的占位符,可以理解为 name
        :return: 实际的 dp_xpath 字符串
        """
        template = self.xpath_templates.get(key)
        if not template:
            print(f"未找到键名为 {key} 的 XPath 模板")
            return None
        # 使用 kwargs 替换模板中的占位符
        xpath = template.format(**kwargs)
        # 返回 dp_xpath 格式的字符串
        return f'xpath:.{xpath}'

