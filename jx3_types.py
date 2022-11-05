# coding: utf-8
# author: LinXin
from collections import namedtuple


skill_script = namedtuple('skill_script', ['tSkillData', 'tSkillCoolDown', 'tSkillName', 'tDesc', 'nNeedGcdType', 'nNeedMinRage', 'Apply'])

damage_data = namedtuple('skill_damage', ['nDamageBase', 'nDamageRand', 'nAttackRate', 'nWeaponDamagePercent'])

cooldown_data = namedtuple('cooldown_data', ['nSingleCoolDown', 'nMaxStackNum'])

buff = namedtuple('buff', ['id', 'level', 'layer', 'desc', 'lasting'])

GCD_TYPE = {
    0: 'normal_24',     # 常规1.5s
    1: 'normal_16',     # 常规1s
    2: 'dundang_8',     # 盾挡进入的0.5s
    3: 'hanxiao_0',     # 寒啸进入的0s
    4: 'dundao_0',      # 盾刀234段进入的0s
    5: 'xuedao_8',      # 血刀进入的0.5s
    6: 'dunfei_16',     # 盾飞自身1s
    7: 'xuenu_8',       # 血怒自身0.5s
}


class Player:

    def __init__(self): ...
    # ————————————————————怒气部分————————————————————
    @property
    def rage(self): return ...
    @rage.setter
    def rage(self, value): ...
    # ————————————————————属性部分————————————————————
    @property
    def Vitality(self): return ...
    @property
    def PhysicsAttackPower(self): return ...
    @property
    def PhysicsCriticalPercent(self): return ...
    @property
    def PhysicsCriticalDamagePowerPercent(self): return ...
    @property
    def OvercomePercent(self): return ...
    @property
    def StrainPercent(self): return ...
    @property
    def SurplusValue(self): return ...
    @property
    def HastePercent(self): return ...
    @property
    def ParryPercent(self): return ...
    @property
    def ParryPercentValue(self): return ...
    @property
    def ParryValue(self): return ...

    # ————————————————————技能部分————————————————————

    def CastSkill(self, skill_id, skill_level):
        """
        :param skill_id:
        :param skill_level:
        :return:
        """

    def GetSkillLevel(self, skill_id):
        """
        :param skill_id:
        :return:
        """

    def IsSkillRecipeActive(self, recipe_id, recipe_level):
        """
        :param recipe_id:
        :param recipe_level:
        :return:
        """
        pass

    # ————————————————————气劲部分————————————————————
    def AddBuff(self, buff_id, level, desc=None, lasting=None):
        """
        :param buff_id:
        :param level:
        :param desc:
        :param lasting:
        :return:
        """

    def IsHaveBuff(self, buff_id, buff_level=None):
        """
        :param buff_id:
        :param buff_level:
        :return:
        """

    def DelBuff(self, buff_id, buff_level=None):
        """
        :param buff_id:
        :param buff_level:
        :return:
        """
    # ————————————————————时间部分————————————————————

    def Timer(self):
        """
        :return:
        """

    def AddSkillCoolDown(self, skill_id, period):
        """
        :param skill_id:
        :param period:
        :return:
        """

    def AddPublicCoolDown(self, cooldown_type, period):
        """
        GCD_TYPE = {\n
        0: 'normal_24',     # 常规1.5s\n
        1: 'normal_16',     # 常规1s\n
        2: 'dundang_8',     # 盾挡进入的0.5s\n
        3: 'hanxiao_0',     # 寒啸进入的0s\n
        4: 'dundao_0',      # 盾刀234段进入的0s\n
        5: 'xuedao_8',      # 血刀进入的0.5s\n
        6: 'dunfei_16',     # 盾飞自身1s\n
        7: 'xuenu_8',       # 血怒自身0.5s\n
    }\n
        :param cooldown_type:
        :param period:
        :return:
        """

    def ClearCDTime(self, skill_id, period):
        """
        :param skill_id:
        :param period:
        :return:
        """