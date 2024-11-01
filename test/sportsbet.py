from __future__ import annotations
from platform_handlers.BaseHandler import BaseHandler
import time
from utils.Log import get_logger

# 测试导入包
from DrissionPage import ChromiumPage, ChromiumOptions
from settings import ADS
import requests
from typing import Optional, Union
from DrissionPage._elements.chromium_element import ShadowRoot, ChromiumElement
from DrissionPage._pages.chromium_tab import ChromiumTab

from DrissionPage._pages.chromium_tab import ChromiumTab
from DrissionPage._elements.chromium_element import ChromiumElement
from logging import Logger
from typing import Union, Optional


def open_svg(page):
    pass
    print(type(page))
    xpath = "//*[@class[contains(., 'summary__IconWrapper-sc-')]]"
    dp_xpath = 'xpath:.' + xpath
    time.sleep(2)
    div_eles = page.eles(dp_xpath)
    if len(div_eles) > 2:
        divs = div_eles[2:]
        for div in divs:
            div.scroll()
            div.click()



def find_game_name_button(page: ChromiumTab, bet_info: dict, name: str = None) -> Optional[dict[ChromiumElement]]:
    if not name:
        name = bet_info['betting_team_name'].lower()
    xpath = f"//p[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{name.lower()}')]"
    dp_xpath = 'xpath:.' + xpath
    try:
        game_p = page.ele(dp_xpath)
        if not game_p:
            return None
        game_p.scroll()
        li_father = game_p.parent(2)
        if not li_father:
            return None
        li_s = li_father.nexts()
        print(li_s)
        place_bet_button = {}
        for li in li_s:
            if "StyledAway1X2" in li.attr('class'):
                place_bet_button['home_team'] = li
            if "StyledAway1X2" in li.attr('class'):
                place_bet_button['guest_team'] = li
            if "StyledDraw1X2" in li.attr('class'):
                place_bet_button['draw'] = li

        place_bet_button['draw'].click()

    except Exception as e:
        print(e)
    return place_bet_button


def find_league_ele(page: ChromiumTab, bet_info: dict) -> Optional[ChromiumElement]:
    home_team_name = bet_info['home_team_name'].strip()
    guest_team_name = bet_info['guest_team_name'].strip()
    game_name = home_team_name + ' - ' + guest_team_name
    xpath = f"//div[text()='{game_name}']"
    dp_xpath = 'xpath:.' + xpath
    try:
        league_ele = page.ele(dp_xpath)
        print("league_ele",league_ele)
    except Exception as e:
        print(e)

    try:
        league_father_ele = league_ele.parent(2)
        print("league_father_ele",league_father_ele)
    except Exception as e:
        print(e)

    try:
        xpath ="//div[contains(@class, 'BetslipInfo__Target-sc')]"
        dp_xpath = 'xpath:.' + xpath
        BetslipInfo_Targets = league_father_ele.next(dp_xpath)
        print("BetslipInfo_Targets",BetslipInfo_Targets)
    except Exception as e:
        print(e)

    try:
        xpath ="//span"
        dp_xpath = 'xpath:.' + xpath
        odd = BetslipInfo_Targets.ele(dp_xpath)
        print(odd.text)
    except Exception as e:
        print(e)


    try:
        xpath ="/div"
        dp_xpath = 'xpath:.' + xpath
        team = BetslipInfo_Targets.ele(dp_xpath)
        print(team.text)
    except Exception as e:
        print(e)

    # try:
    #     xpath = "//div[contains(@class, 'SingleBetSelection__Footer')]/button"
    #     dp_xpath = 'xpath:.' + xpath
    #     ele = league_father_ele.next(dp_xpath)
    #     print(ele)
    #     if ele:
    #         ele.click()
    # except Exception as e:
    #     print(e)

    try:
        xpath = "//div[contains(@class, 'BetInput__InputContainer')]"
        dp_xpath = 'xpath:.' + xpath
        input_box = page.ele(dp_xpath)
        print(input_box)
        if input_box:
            input_box.input(1)
    except Exception as e:
        print(e)


def find_input_box(page):
    xpath = "//input"
    dp_xpath = 'xpath:.' + xpath
    try:
        input_box = page.ele(dp_xpath)
        if not input_box:
            return None
        else:
            print(input_box)
            input_box.input(1)
    except Exception as e:
        print(e)

def find_place_bet_button(page):
    xpath= "//div[contains(@class, 'BetslipFooter__StyledBetslipFooter')]//button"
    dp_xpath = 'xpath:.' + xpath
    try:
        ele = page.ele(dp_xpath)
        if ele:
            print(ele)
            ele.click()
    except Exception as e:
        print(e)






if __name__ == '__main__':
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

    bet_info = {
        'betting_team_name': 'AS Monaco FC',
        'home_team_name': 'AS Monaco FC',
        'guest_team_name': 'Angers SCO',

    }

    open_svg(page)
    find_game_name_button(page, bet_info)
    a = find_league_ele(page,bet_info)
    # find_input_box(page)
    find_place_bet_button(page)
