from platform_handlers.stake_POM import Stake_Page_Obj_Model
from platform_handlers.rollbit_POM import Rollbit_Page_Obj_Model

POM = {
    'Stake': Stake_Page_Obj_Model,
    'Rollbit': Rollbit_Page_Obj_Model,
}


def get_page_obj_factor(name):
    try:
        if name == "Stake":
            return Stake_Page_Obj_Model
        elif name == "Rollbit":
            return Rollbit_Page_Obj_Model
    # elif name == "Sportbet":
    #     return Sportbet_Page_Obj_Model
    except Exception as e:
        print(f"未找到POM对象：{name}")