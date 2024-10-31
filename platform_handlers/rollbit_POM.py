import time

class Rollbit_Page_Obj_Model:
    def __init__(self,page,logger):
        self.page = page
        self.logger = logger

    def find_shadow_root(self):
        try:
            xpath = "//div[@id='bt-inner-page']"
            dp_xpath = 'xpath:.' + xpath
            sr = self.page.ele(dp_xpath).shadow_root
            if sr:
                self.logger.info("Shadow root 元素被找到")
                return sr
            else:
                self.logger.info("Shadow root 元素未找到")
                return None
        except Exception as e:
            self.logger.error(f"找Shadow root 时出错: {e}")

    def find_button_1(self,sr, bet_info,name=None):
        # 获取投注队伍名称
        if not name:
            name = bet_info['betting_team_name'].lower()
        try:
            xpath = f"//span[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{name}')]"
            dp_xpath = 'xpath:.' + xpath
            if sr.ele(dp_xpath, timeout=20):
                print("找到按钮1")
                return sr.ele(dp_xpath, timeout=20)
            else:
                print("未找到按钮1")
                return None
        except Exception as e:
            self.logger.error(f"找button 1 时出错: {e}")

    def find_button_1_brother(self, sr, bet_info, brother_name):
        brother_ele = self.find_button_1(sr=sr, bet_info=bet_info, name=brother_name)
        if brother_ele:
            try:
                xpath = ".//ancestor::*[@data-editor-id='outcomePlate']"
                dp_xpath = 'xpath:.' + xpath
                father_ele = brother_ele.ele(dp_xpath, timeout=5)
                print("按钮1的父亲节点", father_ele)
                if not father_ele:
                    # print(brother_ele)
                    self.logger.warning(f"未找到按钮1的父节点")
                    return None
            except Exception as e:
                self.logger.error(f"找button 1 的兄弟元素出错: {e}")
                return None

            try:
                father_brother_ele = father_ele.next()
                if not father_brother_ele:
                    self.logger.warning(f"未找到按钮1的父亲的兄弟节点")
                    return None
            except Exception as e:
                self.logger.error(f"找按钮1的父亲节点的兄弟节点出错: {e}")
                return None

            try:
                xpath = "//span[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'draw')]"
                dp_xpath = 'xpath:.' + xpath
                draw_button = father_brother_ele.ele(dp_xpath, timeout=5)
                if not draw_button:
                    self.logger.warning(f"未找到按钮1的父亲的兄弟节点的draw按钮")
                    return None
            except Exception as e:
                self.logger.error(f"找按钮1的父亲的兄弟节点的draw按钮出错: {e}")
                return None

            return draw_button

    def find_check_odds(self,sr,bet_info):
        home_team_name = bet_info['home_team_name'].lower().strip()
        guest_team_name = bet_info['guest_team_name'].lower().strip()

        name = home_team_name+ ' vs ' + guest_team_name
        div = None

        try:
            xpath = f"//div[translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz') = '{name}']"
            dp_xpath = 'xpath:.' + xpath
            div = sr.ele(dp_xpath, timeout=10)
            if not div:
                self.logger.warning(f"未找到找下单区域的比赛名称")
                return None
        except Exception as e:
            self.logger.error(f"找下单区域的比赛名称出错: {e}")

        try:
            father_div = div.parent(2)
            if not father_div:
                self.logger.warning(f"未找到下单区域的比赛名称的父节点")
                return None
        except Exception as e:
            self.logger.error(f"找下单区域的比赛名称的父节点出错: {e}")
            return None

        try:
            father_brother_div = father_div.next()
            if not father_brother_div:
                self.logger.warning(f"未找到下单区域的比赛名称的父亲的兄弟节点")
                return None
            else:
                return father_brother_div
        except Exception as e:
            self.logger.error(f"找下单区域的比赛名称的父亲的兄弟节点出错: {e}")

    def find_place_bet_button(self,sr):
        xpath = "//span[translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz') = 'place bet']"
        dp_xpath = 'xpath:.' + xpath
        try:
            place_bet_span = sr.ele(dp_xpath, timeout=10)
            if not place_bet_span:
                self.logger.warning(f"未找到下单区域的place bet按钮的span")
                return None
        except Exception as e:
            self.logger.error(f"找下单区域的place bet按钮的span出错: {e}")
            return None

        try:
            place_bet_button = place_bet_span.parent(1)
            if not place_bet_button:
                self.logger.warning(f"未找到下单区域的place bet按钮")
                return None
            else:
                return place_bet_button
        except Exception as e:
            self.logger.error(f"找下单区域的place bet按钮出错: {e}")
            return None

    def find_input_element(self,sr):
        xpath = "//input"
        dp_xpath = 'xpath:.' + xpath
        try:
            input_element = sr.ele(dp_xpath, timeout=10)
            if not input_element:
                self.logger.warning(f"未找到下单区域的input元素")
                return None
            else:
                self.logger.info("找到下单区域的input元素")
                return input_element
        except Exception as e:
            self.logger.error(f"找下单区域的input元素出错: {e}")

    def find_close_element(self,sr,bet_info):
        home_team_name = bet_info['home_team_name'].lower().strip()
        guest_team_name = bet_info['guest_team_name'].lower().strip()
        name = home_team_name+ ' vs ' + guest_team_name
        xpath = f"//div[translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz') = '{name}']"
        dp_xpath = 'xpath:.' + xpath
        try:
            div = sr.ele(dp_xpath, timeout=10)
            if not div:
                self.logger.warning(f"未找到关闭按钮的div")
                return None
        except Exception as e:
            self.logger.error(f"找关闭按钮的div出错: {e}")
            return None

        try:
            div_father = div.parent(3)
            if not div_father:
                self.logger.warning(f"未找到关闭按钮的div的父节点")
                return None
        except Exception as e:
            self.logger.error(f"找关闭按钮的div的父节点出错: {e}")
            return None

        try:
            div_father_brother = div_father.prev()
            if not div_father_brother:
                self.logger.warning(f"未找到关闭按钮的div的父亲的兄弟节点")
                return None
            else:
                return div_father_brother
        except Exception as e:

            self.logger.error(f"找关闭按钮的div的父亲的兄弟节点出错: {e}")
            return None
