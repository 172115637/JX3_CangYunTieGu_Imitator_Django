# coding: utf-8
# author: LinXin
import random

from settings.jx3_types import *
from settings.jx3_collections import recipe
from .player_attribute import Attribute
from .player_skill import skill_id_to_script
from scripts.buff import buff_data
import scripts

from typing import Dict, Union


class Player:

    def __init__(self, talents: Dict, recipes: Dict, target: Target):
        # ————————————————————怒气部分————————————————————
        self._rage = 0

        self.casted = None
        self.damage = 0
        # ————————————————————属性部分————————————————————
        self._attribute = Attribute(self)
        # ————————————————————气劲部分————————————————————
        self.buffs: Dict[int, buff] = {
        }
        # ————————————————————技能部分————————————————————
        self.talents = talents
        self.recipes = recipes
        # ————————————————————技能cd部分————————————————————
        self._cooldown = {
        }
        self._gcd_list = {
            0: 0,  # 'normal_24',  # 常规1.5s
            1: 0,  # 'normal_16',  # 常规1s
            2: 0,  # 'dundang_8',  # 盾挡进入的0.5s
            3: 0,  # 'hanxiao_0',  # 寒啸进入的0s
            4: 0,  # 'dundao_0',  # 盾刀234段进入的0s
            5: 0,  # 'xuedao_8',  # 血刀进入的0.5s
            6: 0,  # 'dunfei_16',  # 盾飞自身1s
            7: 0,  # 'xuenu_8',  # 血怒自身0.5s
        }
        # 当前时间
        self._timer = -1
        # ————————————————————体态部分————————————————————
        # 默认添加盾姿态buff
        self.AddBuff(8277, 1)
        # ————————————————————目标部分————————————————————
        self._target = target

    # ————————————————————怒气部分————————————————————

    @property
    def rage(self):
        return self._rage

    @rage.setter
    def rage(self, value):
        assert isinstance(value, int), '怒气必须为整数'
        self._rage = min(110, value)
        if self._rage < 0:
            self._rage = 0

    # ————————————————————属性部分————————————————————
    @property
    def Vitality(self):
        return self._attribute.Vitality

    @property
    def PhysicsAttackPower(self):
        return self._attribute.PhysicsAttackPower

    @property
    def PhysicsCriticalPercent(self):
        return self._attribute.PhysicsCriticalPercent

    @property
    def PhysicsCriticalDamagePowerPercent(self):
        return self._attribute.PhysicsCriticalDamagePowerPercent

    @property
    def OvercomePercent(self):
        return self._attribute.OvercomePercent

    @property
    def StrainPercent(self):
        return self._attribute.StrainPercent

    @property
    def SurplusValue(self):
        return self._attribute.SurplusValue

    @property
    def HastePercent(self):
        return self._attribute.HastePercent

    @property
    def ParryPercent(self):
        return self._attribute.ParryPercent

    @property
    def ParryPercentValue(self):
        return self._attribute.ParryPercentValue

    @property
    def ParryValue(self):
        return self._attribute.ParryValue

    # ————————————————————技能部分————————————————————

    def CastSkill(self, skill_id, skill_level):
        # 1. 获取到对应脚本
        # 2. 执行对应脚本的Apply方法
        # 3. 检查释放结果，记录释放信息

        # 技能效果
        if skill_id in skill_id_to_script:
            _skill = skill_id_to_script[skill_id]
        elif isinstance(skill_id, str):
            if hasattr(scripts, skill_id):
                _skill = getattr(scripts, skill_id)
                if not _skill:
                    return
            else:
                return
        else:
            return

        # 检查gcd
        gcd_type_list = _skill.nNeedGcdType
        for gcd_type in gcd_type_list:
            if gcd_type not in self._gcd_list:
                return
            if self._gcd_list[gcd_type] > 0:
                return

        # 检查cd
        cd_data: cooldown_data = _skill.tSkillCoolDown
        if skill_level not in cd_data:
            return
        cd_data = cd_data[skill_level]

        if skill_id in self._cooldown:
            max_cd = cd_data.nMaxStackNum * cd_data.nSingleCoolDown
            if not max_cd:
                return
            # 检查现有cd+一层cd是否大于总cd, 若为否则可以施展
            if self._cooldown[skill_id] + cd_data.nSingleCoolDown > max_cd:
                return

        # 检查怒气需求
        if self._rage < _skill.nNeedMinRage:
            return

        # 检查体态
        if self.IsHaveBuff(8277):
            n_state = 0
        else:
            n_state = 1
        if _skill.nNeedPosState is not None:
            if _skill.nNeedPosState != n_state:
                return

        state = _skill.Apply(self, self._target)
        # 技能伤害
        if state:
            dmg, isCritical = self.CallPhysicsDamage(skill_id, _damage_data=_skill.tSkillData[skill_level])
            self.damage += dmg

            # 记录技能
            if self.casted is None:
                self.casted = [{
                    'second': self._timer/16,
                    'frame': self._timer,
                    'name': _skill.tSkillName,
                    'desc': _skill.tDesc,
                    'rage': self._rage,
                    'damage': dmg,
                    'critical': isCritical,
                    'buff': {i: j for i, j in self.buffs.items()},
                    'tbuff': {i: j for i, j in self._target.buffs.items()}
                }]
            else:
                self.casted.append({
                    'second': self._timer/16,
                    'frame': self._timer,
                    'name': _skill.tSkillName,
                    'desc': _skill.tDesc,
                    'rage': self._rage,
                    'damage': dmg,
                    'critical': isCritical,
                    'buff': {i: j for i, j in self.buffs.items()},
                    'tbuff': {i: j for i, j in self._target.buffs.items()}
                })

    def GetSkillLevel(self, skill_id):
        """
        :param skill_id:
        :return:
        """
        if skill_id in self.talents.values():
            return 1

    def IsSkillRecipeActive(self, recipe_id):
        """
        :param recipe_id:
        :return:
        """
        if recipe_id not in recipe:
            return

        recipe_data = recipe.get(recipe_id)

        for skill_recipe in self.recipes.values():
            if recipe_data.index in skill_recipe:
                break
        else:
            # 没有找到该秘籍
            return

        return 1

    def CallPhysicsDamage(self, skill_id, *, nBaseDamage=None, nAttackRate=None, nWeaponDamagePercent=None, _damage_data: damage_data=None):
        """
        :param _damage_data:
        :param skill_id:
        :param nBaseDamage:
        :param nAttackRate:
        :param nWeaponDamagePercent:
        :return:
        """
        if not skill_id:
            if not nBaseDamage and not nAttackRate and not nWeaponDamagePercent:
                if not _damage_data:
                    return 0

        # 秘籍
        recipe_data = self.GetRecipeData(skill_id)

        # 有data的情况
        nBaseDamage = int(_damage_data.nDamageBase + 0.5 * _damage_data.nDamageRand)
        nAttackRate = _damage_data.nAttackRate
        nWeaponDamagePercent = _damage_data.nWeaponDamagePercent

        if not skill_id == 32745:
            nDamage = int(nBaseDamage + nAttackRate * self._attribute.PhysicsAttackPower + nWeaponDamagePercent)
        else:
            nDamage = int(nAttackRate * self._attribute.SurplusValue)

        if nDamage > 0:
            # 会心判定
            nCritical = self._attribute.PhysicsCriticalPercent
            nCritical += recipe_data['atRecipePhysicsCriticalPercent']
            if random.randint(1, 10000) <= nCritical * 10000:
                nFlag = True
            else:
                nFlag = False

            # 恋战
            if skill_id in ['DunDao_1', 13045, 13046, 13047, 13052, 13053, 13054, 13055, 13059, 13060, 13119, 13316, 25215]:
                self.CastSkill(13127, 1)
                if nFlag:
                    self.CastSkill(13128, 1)
        else:
            nFlag = False

        return nDamage, nFlag

    def GetRecipeData(self, skill_id):
        """
        返回某个技能的会心和伤害秘籍类加成\n
        :param skill_id:
        :return:
        """
        recipe_data = {
            'atRecipeDamagePercent': 0,
            'atRecipePhysicsCriticalPercent': 0
        }
        recipes = None

        # 真秘籍
        match skill_id:
            case 'DunDao_1' | 13059 | 13060 | 13119:
                recipes = [1860, 1861, 1862, 1863, 1864, 1865]
            case 13045:
                recipes = [1852, 1853, 1854, 1855]
            case 13052:
                recipes = [1830, 1831, 1832, 1833, 1834, 1835]
            case 13054:
                recipes = [1838, 1839, 1840, 1841, 1842, 1843]
            case 13055:
                recipes = [1846, 1847, 1848, 1849]
            case 13050:
                recipes = [1953, 1954, 1955, 1956]
            # case
        if recipes:
            for recipe_id in recipes:
                if recipe_id not in recipe:
                    continue
                slot = recipe[recipe_id].slot
                if slot not in recipe_data:
                    continue
                if self.IsSkillRecipeActive(recipe_id):
                    recipe_data[slot] += recipe[recipe_id].value

        # 奇穴秘籍

        return recipe_data

    # ————————————————————气劲部分————————————————————

    def AddBuff(self, buff_id, level, desc=None, lasting=None, attrib=None):
        """
        :param attrib:
        :param buff_id:
        :param level:
        :param desc:
        :param lasting:
        :return:
        """
        if not buff_id:
            return
        if buff_id not in buff_data:
            return
        else:
            _buff_data = buff_data[buff_id]

        if lasting is None:
            lasting = _buff_data.nMaxTime
        if desc is None:
            desc = _buff_data.Desc
        if attrib is None:
            attrib = _buff_data.Attrib

        if buff_id in self.buffs:
            _buff: buff = self.buffs.get(buff_id)
            if level < _buff.level:
                return
            if level == _buff.level:
                layer = _buff.layer + 1
                self.buffs[buff_id] = buff(buff_id, level, min(_buff_data.nMaxStackNum, layer), desc, lasting, _buff.script, _buff.attrib)
                return
            # 等级大于的情况
            self.buffs[buff_id] = buff(buff_id, level, 1, desc, lasting, _buff.script, _buff.attrib)

        else:
            self.buffs[buff_id] = buff(buff_id, level, 1, desc, lasting, _buff_data.Script, attrib)


    def IsHaveBuff(self, buff_id, buff_level=None) -> Union[buff, None]:
        """
        :param buff_id:
        :param buff_level:
        :return:
        """
        if not buff_id:
            return
        if buff_id not in self.buffs:
            return

        _buff = self.buffs[buff_id]
        if buff_level is not None:
            if _buff.level == buff_level:
                return _buff
            else:
                return
        else:
            return _buff

    def GetBuff(self, buff_id, buff_level=None) -> buff:
        """
        :param buff_id:
        :param buff_level:
        :return:
        """
        if not buff_id:
            return buff(0, 0, 0, '', 0, None, None)
        if buff_id not in self.buffs:
            return buff(0, 0, 0, '', 0, None, None)

        _buff = self.buffs[buff_id]
        if buff_level is not None:
            if _buff.level == buff_level:
                return _buff
            else:
                return buff(0, 0, 0, '', 0, None, None)
        else:
            return _buff

    def DelBuff(self, buff_id, buff_level=None, all_layer=False):
        """
        :param all_layer:
        :param buff_id:
        :param buff_level:
        :return:
        """
        if not buff_id:
            return
        if buff_id not in self.buffs:
            return

        _buff = self.buffs[buff_id]
        if buff_level is not None and _buff.level == buff_level or buff_level is None:
            if all_layer:
                new_layer = 0
            else:
                new_layer = max(0, _buff.layer - 1)
            if not new_layer:
                del self.buffs[buff_id]
                return 1
            else:
                self.buffs[buff_id] = buff(_buff.id, _buff.level, new_layer, _buff.desc, _buff.lasting, _buff.script, _buff.attrib)
                return 1
        else:
            return

    # ————————————————————时间部分————————————————————

    def Timer(self, value: int):
        """
        :return:
        """
        # 更新时间，记录用
        if value > self._timer:
            self._timer = value
        else:
            return

        # 减cd
        _del = []
        for skill_id, skill_cd in self._cooldown.items():
            skill_cd -= 1
            if skill_cd > 0:
                self._cooldown[skill_id] = skill_cd
            else:
                _del.append(skill_id)
        for skill_id in _del:
            del self._cooldown[skill_id]

        # 减gcd
        for gcd_type, gcd_value in self._gcd_list.items():
            gcd_value -= 1
            if gcd_value > 0:
                self._gcd_list[gcd_type] = gcd_value
            else:
                self._gcd_list[gcd_type] = 0

        # 减buff持续时间
        _del = []
        for buff_id, _buff_data in self.buffs.items():
            new_lasting = max(_buff_data.lasting - 1, 0)
            if not new_lasting:
                _del.append(buff_id)
            else:
                self.buffs[buff_id] = buff(*_buff_data[:-3], new_lasting, *_buff_data[-2:])
        for buff_id in _del:
            _script = self.buffs[buff_id].script
            # 先移除再调用！以免自循环buff被移除
            if buff_id in self.buffs:
                del self.buffs[buff_id]
            if _script is not None:
                self.CastSkill(_script, 1)



    def AddSkillCoolDown(self, skill_id, period):
        """
        :param skill_id:
        :param period:
        :return:
        """
        if not period:
            return
        if not skill_id:
            return
        if skill_id not in self._cooldown:
            self._cooldown[skill_id] = period
        else:
            self._cooldown[skill_id] += period

    def GetSkillCoolDown(self, skill_id) -> Union[int, None]:
        """
        :param skill_id:
        :return:
        """
        if not skill_id:
            return
        if skill_id not in self._cooldown:
            return 0
        else:
            return self._cooldown[skill_id]

    def AddPublicCoolDown(self, cooldown_type, period):
        """
        :param cooldown_type:
        :param period:
        :return:
        """
        if not period:
            return
        if cooldown_type not in GCD_TYPE:
            return
        self._gcd_list[cooldown_type] = period

    def ClearCDTime(self, skill_id, period=None):
        """
        :param skill_id:
        :param period:
        :return:
        """
        if not skill_id:
            return
        if skill_id not in self._cooldown:
            return
        else:
            cd = self._cooldown[skill_id]
            if period is None or cd <= period:
                del self._cooldown[skill_id]
            else:
                self._cooldown[skill_id] = cd - period