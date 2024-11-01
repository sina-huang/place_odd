from typing import Union, Optional, Dict
from DrissionPage._pages.chromium_tab import ChromiumTab
from DrissionPage._elements.chromium_element import ChromiumElement
from logging import Logger


class Sportsbet_Page_Obj_Model:
    def __init__(self, page: ChromiumTab, logger: Logger) -> None:
        self.page = page
        self.logger = logger

    def open_svgs(self, page: ChromiumTab) -> None:
        try:
            xpath = "//*[@class[contains(., 'summary__IconWrapper-sc-')]]"
            dp_xpath = 'xpath:.' + xpath
            div_eles = page.eles(dp_xpath, timeout=5)
            if not div_eles:
                self.logger.warning("没有找到任何开打联赛的svg图标")
            else:
                if len(div_eles) > 2:
                    for div in div_eles[2:]:
                        div.scroll()
                        div.click()
        except Exception as e:
            self.logger.warning(f"打开开打联赛的svg图标失败{e}")

    def find_game_name_button(self, page: ChromiumTab, bet_info: dict, name: str = None) -> dict:
        # This function searches by game name and returns a dictionary containing ChromiumElement instances.
        # If no matching element is found, it returns an empty dictionary.
        place_bet_button = {}
        if not name:
            name = bet_info['betting_team_name'].lower()
        xpath = f"//p[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{name.lower()}')]"
        dp_xpath = 'xpath:.' + xpath

        try:
            game_p = page.ele(dp_xpath, timeout=3)
            if not game_p:
                self.logger.warning(f"没有找到比赛名称为{name}的按钮")
                return {}
        except Exception as e:
            self.logger.warning(f"没有找到比赛名称为{name}的按钮,报错{e}")
            return {}

        try:
            game_p.scroll()
            li_father = game_p.parent(2)
            if not li_father:
                self.logger.warning(f"没有找到比赛名称为{name}的按钮的父li元素")
                return {}
        except Exception as e:
            self.logger.warning(f"没有找到比赛名称为{name}的按钮的父li元素,报错{e}")
            return {}

        try:
            li_s = li_father.nexts()
            if not li_s:
                self.logger.warning(f"没有找到比赛名称为{name}的按钮的父li元素的兄弟li元素")
                return {}
        except Exception as e:
            self.logger.warning(f"没有找到比赛名称为{name}的按钮的父li元素的兄弟li元素,报错{e}")
            return {}

        for li in li_s:
            if "StyledHome1X2" in li.attr('class'):
                place_bet_button['home_team'] = li
            if "StyledAway1X2" in li.attr('class'):
                place_bet_button['guest_team'] = li
            if "StyledDraw1X2" in li.attr('class'):
                place_bet_button['draw'] = li

        return place_bet_button

    def find_league_ele(self, page: ChromiumTab, bet_info: dict) -> Optional[ChromiumElement]:
        home_team_name = bet_info['home_team_name'].strip()
        guest_team_name = bet_info['guest_team_name'].strip()
        game_name = home_team_name + ' - ' + guest_team_name
        xpath = f"//div[text()='{game_name}']"
        dp_xpath = 'xpath:.' + xpath
        print(dp_xpath)
        try:
            league_ele = page.ele(dp_xpath)
            if not league_ele:
                self.logger.warning(f"没有找到比赛名称为{game_name}的联赛元素")
                return None
        except Exception as e:
            self.logger.warning(f"没有找到比赛名称为{game_name}的联赛元素,报错{e}")
            return None

        try:
            league_father_ele = league_ele.parent(2)
            if league_father_ele:
                self.logger.info(f"找到比赛名称为{game_name}的联赛元素的父元素")
                return league_father_ele
        except Exception as e:
            self.logger.warning(f"没有找到比赛名称为{game_name}的联赛元素的父元素,报错{e}")
            return None

    def find_check_odd_div(self, page: ChromiumTab, bet_info: dict) -> Optional[ChromiumElement]:
        ele = self.find_league_ele(page, bet_info)
        xpath = "//div[contains(@class, 'BetslipInfo__Target-sc')]//span"
        dp_xpath = 'xpath:.' + xpath
        try:
            BetslipInfo_Targets = ele.next(dp_xpath)
            if BetslipInfo_Targets:
                return BetslipInfo_Targets
        except Exception as e:
            self.logger.warning(f"没有找到比赛名称为{game_name}的联赛元素的父元素的兄弟元素,报错{e}")
            return None

    def find_close_button(self, page: ChromiumTab, bet_info: dict) -> Optional[ChromiumElement]:
        ele = self.find_league_ele(page, bet_info)
        xpath = "//div[contains(@class, 'SingleBetSelection__Footer')]/button"
        dp_xpath = 'xpath:.' + xpath
        try:
            close_button = ele.next(dp_xpath)
            if close_button:
                return close_button
            else:
                self.logger.warning(f"没有找到比赛名称为{game_name}的联赛元素的父元素的兄弟元素的关闭按钮")
                return None
        except Exception as e:
            self.logger.warning(f"没有找到比赛名称为{game_name}的联赛元素的父元素的兄弟元素的关闭按钮,报错{e}")
            return None

    def find_input_box(self,page: ChromiumTab, bet_info: dict) -> Optional[ChromiumElement]:
        ele = self.find_league_ele(page, bet_info)
        xpath = "//div[contains(@class, 'BetInput__InputContainer')]"
        dp_xpath = 'xpath:.' + xpath
        try:
            input_box = page.ele(dp_xpath)
            if input_box:

                return input_box
            else:
                self.logger.warning(f"没有找到比赛名称为{game_name}的联赛元素的父元素的兄弟元素的关闭按钮")
                return None
        except Exception as e:
            self.logger.warning(f"没有找到比赛名称为{game_name}的联赛元素的父元素的兄弟元素的关闭按钮,报错{e}")

    def find_place_bet_button(self,page:ChromiumTab):
        xpath = "//div[contains(@class, 'BetslipFooter__StyledBetslipFooter')]//button"
        dp_xpath = 'xpath:.' + xpath
        try:
            ele = page.ele(dp_xpath)
            if not ele:
                self.logger.warning(f"没有找到下注按钮")
                return None
            else:
                self.logger.info(f"找到下注按钮")
                return ele

        except Exception as e:
            self.logger.warning(f"没有找到下注按钮,报错{e}")
            return None

def open_ads_browser():
    ads_id = 'knbvol0'
    ads_open_url = ADS['ads_open_url'] + ads_id
    resp = requests.get(ads_open_url).json()
    time.sleep(2)
    if resp["code"] != 0:
        print(
            f'[ads 启动失败] ads_id: {ads_id},处理办法: 需要取配置两个ads浏览器请求直接的时间间隔，如果间隔太短，ads浏览器会启动失败')
    debug_port = int(resp["data"]["debug_port"])

    chrome_option = ChromiumOptions()
    chrome_option.set_local_port(debug_port)

    chrome = ChromiumPage(addr_or_opts=chrome_option)
    page = chrome.new_tab('https://sportsbet.io/sports/soccer/inplay')

    return page

if __name__ == '__main__':
    # todo
    from utils.Log import get_logger
    from DrissionPage import ChromiumPage, ChromiumOptions
    from settings import ADS
    import requests
    import time
    logger = get_logger(name=__name__, log_file='log.log')
    page = open_ads_browser()
    bet_info = {
        'betting_team_name': 'Luton Town',
        'home_team_name': 'Luton Town',
        'guest_team_name': 'West Bromwich Albion',
        'betting_odds':0.5

    }


    pom = Sportsbet_Page_Obj_Model(page,logger)
    pom.open_svgs(page)
    game_name_button = pom.find_game_name_button(page, bet_info)
    # game_name_button.click()
    print(game_name_button)

    button = game_name_button['home_team'].click()

    ele1 = pom.find_check_odd_div(page, bet_info)
    print(ele1.text)

