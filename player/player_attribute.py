# coding: utf-8
# author: LinXin
# 负责属性计算

from settings.jx3_types import Player
from settings.jx3_collections import special_stones, LEVEL_CONST, LEVEL_RATE, global_params
from scripts.buff import buff_data
from scripts.slot import attribute_value

from typing import Dict
from math import ceil


class Attribute:

    def __init__(self, player: Player):
        # 这里要先做一步转换成基础值
        self.base_attributes = {
            'Vitality': 0,
            'Agility': 0,
            'Strength': 0,
            'PhysicsAttackPowerBase': 0,
            'PhysicsCriticalStrike': 0,
            'PhysicsCriticalDamagePower': 0,
            'PhysicsOvercome': 0,
            'Strain': 0,
            'SurplusValue': 0,
            'Haste': 0,
            'Parry': 0,
            'ParryValue': 0,
            'WeaponDamage': 0,
        }

        self.origin_data = {
            "Vitality": 54352, "Agility": 206, "Spirit": 206, "Spunk": 206, "Strength": 206,
            "PhysicsAttackPowerBase": 30, "PhysicsAttackPower": 2206,
            "PhysicsCriticalStrikeRate": 0.0016661897039651498,
            "PhysicsCriticalDamagePowerPercent": 1.75, "PhysicsOvercomePercent": 0.019180260103659894,
            "StrainPercent": 0.21642477665984033, "HastePercent": 0.03273090028113543,
            "SurplusValue": 10742,
            "MaxHealth": 852122, "PhysicsShieldPercent": 0.24553729808378877,
            "LunarShieldPercent": 0.06063283141456105,
            "ToughnessDefCriticalPercent": 0.0321282075741677, "DecriticalDamagePercent": 0,
            "DodgePercent": 0.0030349756467679956, "ParryPercent": 0.4960989495868723,
            "ParryValue": 187298,
            "ActiveThreatCoefficient": 12823, "MeleeWeaponAttackSpeed": 24, "MeleeWeaponDamage": 2233,
            "MeleeWeaponDamageRand": 1488, "EquipList": {
                "HAT": {"id": "7_94050", "stone": "", "enchant": "", "enhance": 11557, "strength": 6,
                        "embedding": [6, 6]},
                "BELT": {"id": "7_90783", "stone": "", "enchant": "", "enhance": 11561, "strength": 6,
                         "embedding": [6, 6]},
                "SHOES": {"id": "7_90812", "stone": "", "enchant": "", "enhance": 11612, "strength": 6,
                          "embedding": [6, 6]},
                "WRIST": {"id": "7_90740", "stone": "", "enchant": "", "enhance": 11605, "strength": 6,
                          "embedding": [6, 6]},
                "JACKET": {"id": "7_90870", "stone": "", "enchant": "", "enhance": 11616, "strength": 6,
                           "embedding": [6, 6]},
                "RING_1": {"id": "8_34446", "stone": "", "enchant": "", "enhance": 11662, "strength": 6,
                           "embedding": []},
                "RING_2": {"id": "8_34222", "stone": "", "enchant": "", "enhance": 11662, "strength": 6,
                           "embedding": []},
                "BOTTOMS": {"id": "7_90350", "stone": "", "enchant": "", "enhance": 11550, "strength": 6,
                            "embedding": [6, 6]},
                "PENDANT": {"id": "8_34252", "stone": "", "enchant": "", "enhance": 11654, "strength": 6,
                            "embedding": [6]},
                "NECKLACE": {"id": "8_34312", "stone": "", "enchant": "", "enhance": 11652, "strength": 6,
                             "embedding": [6]},
                "PRIMARY_WEAPON": {"id": "6_34334", "stone": 5599, "enchant": "", "enhance": "", "strength": 6,
                                   "embedding": [6, 6, 6]},
                "SECONDARY_WEAPON": {"id": "6_32591", "stone": "", "enchant": "", "enhance": 11667, "strength": 6,
                                     "embedding": [6]}},
                "Title": "test"}

        self._player = player
        self._get_origin_attributes_value()

    def _get_origin_attributes_value(self):
        """
        将配装器json转化为各类基础属性用于计算\n
        :param origin_data:
        :return:
        """
        # ---------------------------检查属性规范----------------------------
        slots = ['EquipList']
        for slot in slots:
            if slot not in self.origin_data:
                return

        tEquipList = self.origin_data['EquipList']
        # -----------------------------基础体质-----------------------------
        nVitalityBase = self.origin_data['Vitality']
        # 配装器活血 pass

        # -----------------------------基础身法-----------------------------
        # 配装器活脉 pass
        nAgilityBase = self.origin_data['Agility']
        # -----------------------------基础力道-----------------------------
        nStrengthBase = self.origin_data['Strength']
        # ----------------------------主属性五彩石---------------------------
        # 五彩石
        if not tEquipList['PRIMARY_WEAPON']:
            return
        stone_id = tEquipList['PRIMARY_WEAPON']['stone']
        if stone_id in special_stones:
            slot, value = special_stones.get(stone_id)
            match slot:
                case 'atVitalityBasePercentAdd':
                    nVitalityBase = ceil(nVitalityBase / (1 + (value / 1024)))
                case 'atStrengthBasePercentAdd':
                    nStrengthBase = ceil(nStrengthBase / (1 + (value / 1024)))
                case 'atAgilityBasePercentAdd':
                    nAgilityBase = ceil(nAgilityBase / (1 + (value / 1024)))

        # -----------------------------基础攻击-----------------------------
        nPhysicsAttackPowerBase = self.origin_data['PhysicsAttackPowerBase']
        # 不包含力道转化
        # 这里注意要用面板力道去减！
        nPhysicsAttackPowerBase -= int(self.origin_data['Strength'] * 0.15)
        # -----------------------------基础会心-----------------------------
        fPhysicsCriticalStrike = self.origin_data['PhysicsCriticalStrikeRate']
        nCriticalRate = global_params['fCriticalStrikeParam'] * (LEVEL_RATE * 120 - LEVEL_CONST)
        nPhysicsCriticalStrikeBase = int(fPhysicsCriticalStrike * nCriticalRate + 0.5)
        # 不包含身法转化
        nPhysicsCriticalStrikeBase -= int(self.origin_data['Agility'] * 0.64)
        # -----------------------------基础会效-----------------------------
        fPhysicsCriticalDamagePower = self.origin_data['PhysicsCriticalDamagePowerPercent'] - 1.75
        nCriticalPowerRate = global_params['fCriticalStrikePowerParam'] * (LEVEL_RATE * 120 - LEVEL_CONST)
        nPhysicsCriticalDamagePowerBase = int(fPhysicsCriticalDamagePower * nCriticalPowerRate + 0.5)
        # -----------------------------基础破防-----------------------------
        fPhysicsOvercome = self.origin_data['PhysicsOvercomePercent']
        nOvercomeRate = global_params['fOvercomeParam'] * (LEVEL_RATE * 120 - LEVEL_CONST)
        nPhysicsOvercomeBase = int(fPhysicsOvercome * nOvercomeRate + 0.5)
        # 不包含力道转化
        nPhysicsOvercomeBase -= int(self.origin_data['Strength'] * 0.3)
        # -----------------------------基础无双-----------------------------
        fStrain = self.origin_data['StrainPercent']
        nStrainRate = global_params['fInsightParam'] * (LEVEL_RATE * 120 - LEVEL_CONST)
        nStrainBase = int(fStrain * nStrainRate + 0.5)
        # -----------------------------基础破招-----------------------------
        nSurplusValueBase = self.origin_data['SurplusValue']
        # -----------------------------基础加速-----------------------------
        fHaste = self.origin_data['HastePercent']
        nHasteRate = global_params['fHasteRate'] * (LEVEL_RATE * 120 - LEVEL_CONST)
        nHasteBase = int(fHaste * nHasteRate + 0.5)
        # -----------------------------基础招架-----------------------------
        fParry = self.origin_data['ParryPercent'] - 0.03
        nParryRate = global_params['fParryParam'] * (LEVEL_RATE * 120 - LEVEL_CONST)
        nParryBase = int((nParryRate * fParry / (1 - fParry)) + 0.5)
        # 默认铁骨, 后续再改
        # 不包含体质转化
        nParryBase -= int(self.origin_data['Vitality'] * 0.15)
        # -----------------------------基础拆招-----------------------------
        nParryValueBase = self.origin_data['ParryValue']
        # 默认铁骨, 后续再改
        # 不包含体质转化
        nParryValueBase -= int(self.origin_data['Vitality'] * 2.25)
        # -----------------------------武器伤害-----------------------------
        nWeaponDamage = self.origin_data['MeleeWeaponDamage'] + int(0.5 * (self.origin_data['MeleeWeaponDamageRand']))

        self.base_attributes = {
            'Vitality': nVitalityBase,
            'Agility': nAgilityBase,
            'Strength': nStrengthBase,
            'PhysicsAttackPowerBase': nPhysicsAttackPowerBase,
            'PhysicsCriticalStrike': nPhysicsCriticalStrikeBase,
            'PhysicsCriticalDamagePower': nPhysicsCriticalDamagePowerBase,
            'PhysicsOvercome': nPhysicsOvercomeBase,
            'Strain': nStrainBase,
            'SurplusValue': nSurplusValueBase,
            'Haste': nHasteBase,
            'Parry': nParryBase,
            'ParryValue': nParryValueBase,
            'WeaponDamage': nWeaponDamage,
        }

        # print()



    def _get_buff_attribute_value(self, slots) -> Dict[str, int]:

        for buff in self._player.buffs.values():
            if not buff.attrib:
                continue
            for attrib_data in buff.attrib:
                attrib_data = attribute_value[attrib_data]
                if attrib_data.slot in slots:
                    slots[attrib_data.slot] += attrib_data.value * buff.layer

        return slots

    @property
    def Vitality(self):
        slots = {
            'atVitalityBasePercentAdd': 0
        }
        # 活血
        if self._player.GetSkillLevel('活血') == 1:
            slots['atVitalityBasePercentAdd'] += 102
        # 五彩石
        tEquipList = self.origin_data['EquipList']
        if not ['PRIMARY_WEAPON']:
            return
        stone_id = tEquipList['PRIMARY_WEAPON']['stone']
        if stone_id in special_stones:
            slot, value = special_stones.get(stone_id)
            if slot == 'atVitalityBasePercentAdd':
                slots['atVitalityBasePercentAdd'] += value

        value = self.base_attributes['Vitality']
        value += int(value * (slots['atVitalityBasePercentAdd'] / 1024))

        return value

    @property
    def Agility(self):
        slots = {
            'atAgilityBasePercentAdd': 0
        }
        # 活脉
        if self._player.GetSkillLevel('活脉') == 1:
            slots['atAgilityBasePercentAdd'] += 102
        # 五彩石
        tEquipList = self.origin_data['EquipList']
        if not ['PRIMARY_WEAPON']:
            return
        stone_id = tEquipList['PRIMARY_WEAPON']['stone']
        if stone_id in special_stones:
            slot, value = special_stones.get(stone_id)
            if slot == 'atAgilityBasePercentAdd':
                slots['atAgilityBasePercentAdd'] += value

        value = self.base_attributes['Agility']
        value += int(value * (slots['atAgilityBasePercentAdd'] / 1024))

        return value

    @property
    def Strength(self):
        slots = {
            'atStrengthBasePercentAdd': 0
        }

        # 五彩石
        tEquipList = self.origin_data['EquipList']
        if not ['PRIMARY_WEAPON']:
            return
        stone_id = tEquipList['PRIMARY_WEAPON']['stone']
        if stone_id in special_stones:
            slot, value = special_stones.get(stone_id)
            if slot == 'atStrengthBasePercentAdd':
                slots['atStrengthBasePercentAdd'] += value

        value = self.base_attributes['Strength']
        value += int(value * (slots['atStrengthBasePercentAdd'] / 1024))

        return value

    @property
    def PhysicsAttackPower(self):
        slots = {
            'atPhysicsAttackPowerBase': 0,
            'atPhysicsAttackPowerPercent': 0,
        }
        slots = self._get_buff_attribute_value(slots)

        value = self.base_attributes['PhysicsAttackPowerBase']
        value += slots['atPhysicsAttackPowerBase']
        # 力道转化
        value += int(self.Strength * 0.15)
        # 百分比
        value += int(value * slots['atPhysicsAttackPowerPercent'] / 1024)
        # 体质转化
        # 默认铁骨
        value += int(self.Vitality * 0.04)

        return value

    @property
    def PhysicsCriticalPercent(self):
        slots = {
            'atPhysicsCriticalStrikeBaseRate': 0
        }

        slots = self._get_buff_attribute_value(slots)

        value = self.base_attributes['PhysicsCriticalStrike']
        # 身法转化
        value += int(self.Agility * 0.64)

        # 转化为百分比
        value /= global_params['fCriticalStrikeParam'] * (LEVEL_RATE * 120 - LEVEL_CONST)
        value += slots['atPhysicsCriticalStrikeBaseRate']

        return value

    @property
    def PhysicsCriticalDamagePowerPercent(self):
        slots = {
        }
        slots = self._get_buff_attribute_value(slots)
        value = self.base_attributes['PhysicsCriticalDamagePower']

        # 转化为百分比
        value /= global_params['fCriticalStrikePowerParam'] * (LEVEL_RATE * 120 - LEVEL_CONST)
        value += 1.75
        return value

    @property
    def PhysicsOvercomePercent(self):
        slots = {
        }
        slots = self._get_buff_attribute_value(slots)
        value = self.base_attributes['PhysicsOvercome']
        # 力道转化
        value += int(self.Strength * 0.3)

        # 转化为百分比
        value /= global_params['fOvercomeParam'] * (LEVEL_RATE * 120 - LEVEL_CONST)
        return value

    @property
    def StrainPercent(self):
        slots = {
        }
        slots = self._get_buff_attribute_value(slots)
        value = self.base_attributes['Strain']

        # 转化为百分比
        value /= global_params['fInsightParam'] * (LEVEL_RATE * 120 - LEVEL_CONST)
        return value

    @property
    def SurplusValue(self):
        slots = {
            'atSurplusValueAddPercent': 0,
        }
        slots = self._get_buff_attribute_value(slots)
        value = self.base_attributes['SurplusValue']

        value += int(value * slots['atSurplusValueAddPercent'] / 1024)

        return value

    @property
    def HastePercent(self):
        slots = {
        }
        slots = self._get_buff_attribute_value(slots)
        value = self.base_attributes['Haste']

        # 转化为百分比
        value /= global_params['fHasteRate'] * (LEVEL_RATE * 120 - LEVEL_CONST)
        return

    @property
    def ParryPercent(self):
        # atParryBaseRate
        slots = {
            'atParryBaseRate': 0,
        }

        slots = self._get_buff_attribute_value(slots)
        value = self.ParryPercentValue


        # 转化为百分比
        value = value / (value + (global_params['fParryParam'] * (LEVEL_RATE * 120 - LEVEL_CONST)))
        # 百分比增益
        value += slots['atParryBaseRate']
        # 心法默认
        value += 0.03

        return value

    @property
    def ParryPercentValue(self):
        slots = {
            'atParryPercent': 0,
        }
        slots = self._get_buff_attribute_value(slots)
        value = self.base_attributes['Parry']

        # 增益值
        value += int(value * slots['atParryPercent'] / 1024)
        # 体质转化
        value += int(self.Vitality * 0.15)

        return value

    @property
    def ParryValue(self):
        slots = {
            'atParryValuePercent': 0,
        }
        slots = self._get_buff_attribute_value(slots)
        value = self.base_attributes['ParryValue']

        # 增益值
        value += int(value * slots['atParryValuePercent'] / 1024)

        # 体质转化
        value += int(self.Vitality * 2.25)

        return value

    @property
    def WeaponDamage(self):
        slots = {
        }
        slots = self._get_buff_attribute_value(slots)
        value = self.base_attributes['WeaponDamage']

        return value

