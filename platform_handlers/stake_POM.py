import time
class Stake_Page_Obj_Model:
    def __init__(self,page,logger):
        self.page = page
        self.logger = logger

    def find_button_1(self,bet_info):
        name = bet_info['betting_team_name'].lower()
        xpath = f"//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{name}')]"
        dp_xpath = 'xpath:.' + xpath
        ele = self.page.ele(dp_xpath, timeout=2)
        if ele:
            self.logger.info(f'找到了按钮1--用于主页面下单')
        else:
            self.logger.info(f'没有找到按钮1--用于主页面下单')
        return self.page.ele(dp_xpath, timeout=2)

    def find_button_2(self,button_brother):
        return button_brother.nexts().filter.attr('aria-label', 'Draw')[0] or button_brother.prevs().filter.attr('aria-label', 'Draw')[0]


    def wait_spans_refresh(self, bet_info):
        """
        在span列表中，找需要的那个span，这里设计刷新问题
        """
        betting_team_name = bet_info['betting_team_name'].lower()
        xpath = f"//span[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{betting_team_name}')]"
        dp_xpath = 'xpath:.' + xpath


        start_time = time.time()
        while time.time() - start_time < 3:
            spans_num = self.page.eles(dp_xpath)
            if len(spans_num) > 2:
                for el in spans_num:
                    class_attr = el.attr('class')

                    if class_attr is not None and 'outcome-name' in class_attr:
                        self.logger.info(f'找到了记录赔率的span，{el}')
                        return el
                    else:
                        # print(f'{class_attr}没有找到需要的span，{tag}')
                        continue

        self.logger.warning(f'span的数量最终没有大于2')
        return None

    def find_input_ele(self):
        try:
            xpath = "//div[@id='right-sidebar']//div[contains(@class,'footer')]//input"
            dp_xpath = 'xpath:.' + xpath
            return self.page.ele(dp_xpath, timeout=2)
        except Exception as e:
            self.logger.error(f'没有找到输入框，{e}')

    def check_button_is_available(self,need_click=False):
        try:
            xpath = "//div[@id='right-sidebar']//div[contains(@class,'footer')]//button"
            dp_xpath = 'xpath:.' + xpath
            button = self.page.ele(dp_xpath, timeout=2)
            return button

        except Exception as e:
            self.logger.info(f'找不到下单按钮,报错{e}')
            return False

    def find_button_clean_all(self):
        try:
            xpath = "//button[contains(text(), 'Clear All')]"
            dp_xpath = 'xpath:.' + xpath
            return self.page.ele(dp_xpath, timeout=2)
        except Exception as e:
            self.logger.error(f'没有找到清除按钮，{e}')

