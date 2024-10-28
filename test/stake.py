import time

import requests
import sys
from settings import ads_open_url
from DrissionPage import ChromiumPage, ChromiumOptions
# 测试用，
xapth_1 = '//button[@aria-label="Udinese Calcio"]'




def initialize_browser(debug_port, game_name):
    xpath = {
        'main': {
            'root': './/div[@data-layout id="main-content"]',
        },
        'game_button': f'//button[@aria-label="{game_name}"]',
        # 左侧边栏，平时不可见
        'sidebar': {
            'root': '//div[@id="right-sidebar"]',
            'menu': {
                'header': {},
                'betlist': {
                    'inherit': '//div[@id ="right-sidebar"]',
                    'root': './/div[contains(@class, "betlist-scrollY")]',
                    'bet_blocks': {
                        'inherit': '//div[@id ="right-sidebar"]',
                        'root': '//div[contains(@class, "animation-wrapper")]',  # todo 这里可以找到下单的块,多个而非单个
                        'block': {
                            'inherit': '//div[@id ="right-sidebar"]//div[contains(@class, "animation-wrapper")]',
                            'top': '//div[contains(@class, "header")]',
                            'close_button': '//div[contains(@class, "header")]//button',  # todo 关闭块按钮
                            'odds': '//div[contains(@class,"content")]//span[contains(@class,"odds-payout")]//span',
                            'team_name': '//div[contains(@class,"content")]//span[contains(@class,"outcome-name")].text()',
                            'input': '//div[contains(@class,"content")]//div[contains(@class,"footer")]//input',
                        }
                    },

                },
                'footter': {
                    'inherit': '//div[@id ="right-sidebar"]',
                    'root': '//div[contains(@class,"footer")]',
                    'button': '//div[contains(@class,"footer")]/button'  # todo 下单按钮
                }
            }
        }
    }
    try:
        chrome_option = ChromiumOptions()
        chrome_option.set_local_port(debug_port)
        chrome = ChromiumPage(addr_or_opts=chrome_option)
        page = chrome.new_tab("https://stake.com/sports/live/soccer")

        time.sleep(5)
        button = page.ele(splicing_xpath(xpath['game_button'])).click()

        betlist_xpath = splicing_xpath(xpath['sidebar']['menu']['betlist']['inherit'])
        betlist=page.ele(betlist_xpath)

        bet_blocks = xpath['sidebar']['menu']['betlist']['bet_blocks']
        print(bet_blocks)

        bet_block = betlist.eles(splicing_xpath(bet_blocks['root']))[0]
        print(bet_block)


        bet_block_odds = bet_block.ele(splicing_xpath(bet_blocks['block']['odds'])).text
        bet_block_input = bet_block.ele(splicing_xpath(bet_blocks['block']['input'])).input('1')

        print(bet_block_odds)


        footer = xpath['sidebar']['menu']['footter']

        footer_inherit = footer['inherit']
        footer_button = footer['button']
        button_xpath = splicing_xpath(footer_inherit+footer_button)
        time.sleep(3)
        button = page.ele(button_xpath).click()



        button_betting = footer['button']



        time.sleep(10)
    except Exception as e:
        print(e)

def splicing_xpath(xpath):
    print('xpath:.'+ xpath)
    return  'xpath:.'+ xpath

game_name ='Stade Rennais FC'
# 启动 ads 服务，获取 debug_port
resp = requests.get(ads_open_url).json()
if resp["code"] != 0:
    sys.exit()
debug_port = int(resp["data"]["debug_port"])
initialize_browser(debug_port,game_name)






