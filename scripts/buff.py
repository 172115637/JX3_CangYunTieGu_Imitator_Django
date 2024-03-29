# coding: utf-8
# author: LinXin
from collections import namedtuple


_buff_data = namedtuple('buff_data', ['dwID', 'nMaxTime', 'nMaxStackNum', 'Desc', 'Script', 'Attrib'])


buff_data = {
    994: _buff_data(994, 1*16, 1, '倒地', None, None),
    8232: _buff_data(8232, 16*3, 1, '盾刀二段标记buff', None, None),
    8245: _buff_data(8245, 10*16, 3, '血怒防御buff', 'XueNuDisappear', None),
    8248: _buff_data(8248, 25*16, 1, '虚弱', None, [52]),
    8249: _buff_data(8249, 25*16, 1, '流血', 'LiuXueDisappear', None),
    8253: _buff_data(8253, 8*16, 1, '雄峦', None, None),
    8262: _buff_data(8262, 16*4, 1, '盾刀三段标记buff', None, None),
    8263: _buff_data(8263, 16*3, 1, '盾刀四段标记buff', None, None),
    8267: _buff_data(8267, 8*16, 10, '恋战', None, [48]),
    8271: _buff_data(8271, 8*16, 125, '寒甲_300AP', None, [46]),
    8272: _buff_data(8272, 8*16, 5, '坚铁', None, [1]),
    8276: _buff_data(8276, 15*16, 1, '怒炎', 'NuYanMajorDisappear', None),
    8277: _buff_data(8277, 999999*16, 1, '切换至盾姿态', None, None),
    8278: _buff_data(8278, 999999*16, 1, '切换至刀姿态', None, None),
    8320: _buff_data(8320, 8.25*16, 1, '恋战_会心后停止叠加cd', None, None),
    8321: _buff_data(8321, 8.25*16, 1, '坚铁_招架后停止叠加cd', None, None),
    8337: _buff_data(8337, 999999*16, 1, '临川列山阵', None, [67, 68, 69]),
    8382: _buff_data(8382, 1*16, 1, '血怒连按第二层需求buff', None, None),
    8383: _buff_data(8383, 1*16, 1, '血怒连按第三层需求buff', None, None),
    8384: _buff_data(8384, 1*16, 1, '血怒连按需求buff', None, None),
    8386: _buff_data(8386, 10*16, 3, '血怒加强后防御buff', 'XueNuDisappear', None),
    8391: _buff_data(8391, 15*16, 1, '盾飞', 'DunHuiChangeState', None),
    8397: _buff_data(8397, 15*16, 1, '盾威', None, None),
    8398: _buff_data(8398, 16*6, 1, '卷云', None, None),
    8418: _buff_data(8418, 6*16, 1, '激昂', None, None),
    8423: _buff_data(8423, 2*16, 1, '从容', 'CongRongDisappear', [49]),
    8424: _buff_data(8424, 8*16, 1, '坚定', None, None),
    8437: _buff_data(8437, 8*16, 1, '寒甲', 'HanJiaDisappear', None),
    8448: _buff_data(8448, 11*16, 1, '盾挡（千山）', None, None),
    8462: _buff_data(8462, 2*16, 1, '招架后寒甲内置cd', None, None),
    8499: _buff_data(8499, 11*16, 1, '盾挡', None, None),
    8504: _buff_data(8504, 10*16, 125, '振奋', None, None),
    8738: _buff_data(8738, 16*12, 1, '缓深', None, None),
    8873: _buff_data(8873, 0.5*16, 1, '盾飞0.5s内无法施展盾猛', None, None),
    9052: _buff_data(9052, 999999*16, 1, '绝刀耗怒增伤标记buff', None, None),
    9889: _buff_data(9889, 10*16, 1, '蔑视', None, [51]),
    13352: _buff_data(13352, 0.375*16, 1, '盾飞延迟切姿态', 'DunFeiChangeState', None),
    13934: _buff_data(13934, 3*16, 1, '戍卫', None, None),
    14964: _buff_data(14964, 999999*16, 1, '崇云', None, [74]),
    15413: _buff_data(15413, 8*16, 1, '御帽', None, None),
    15414: _buff_data(15414, 30*16, 1, '御帽内置cd', None, None),
    15453: _buff_data(15453, 10*16, 1, '伤腕内置cd', None, None),
    15455: _buff_data(15455, 8*16, 1, '伤腰', None, None),
    15456: _buff_data(15456, 30*16, 1, '伤腰内置cd', None, None),
    15955: _buff_data(15955, 999999*16, 1, '龙皇雪风阵', None, [70, 71, 72]),
    15961: _buff_data(15961, 7.5*16, 1, '龙皇雪风五阵', None, [73]),
    17772: _buff_data(17772, 8*16, 125, '寒甲_3万AP', None, [47]),
    17885: _buff_data(17885, 12*16, 15, '铁骨', None, [55, 57]),
    17886: _buff_data(17886, 12*16, 20, '铁骨', None, [56, 58]),
    18222: _buff_data(18222, 12*16, 5, '严阵', None, [50]),
    21308: _buff_data(21308, 999999*16, 1, '割裂', None, None),
    24755: _buff_data(24755, 4*16, 1, '怒炎标记buff', 'NuYanDisappear', None),
    24756: _buff_data(24756, 4*16, 1, '怒炎重置绝刀标记', None, None),
    24767: _buff_data(24767, 3*16, 1, '御腕', None, [65, 66]),
    24791: _buff_data(24791, 25*16, 1, '御腕内置cd', None, None),
    24774: _buff_data(24774, 10*16, 1, '伤鞋内置cd', None, None),
    # 以下是自定义功能的buff
    50000: _buff_data(50000, 25*16, 50, '盾飞跳数监控', None, None),
    50001: _buff_data(50001, 25*16, 1, '盾飞后监控虚弱是否被流血覆盖', None, None),
    50002: _buff_data(50002, 0.125*16, 1, '盾飞延迟获得虚弱', 'DunFeiAddXuRuo', None),
    50003: _buff_data(50003, 1*16, 1, '盾飞伤害子技能1秒cd', 'DunFeiAttack', None),
    50004: _buff_data(50004, 0.625*16, 1, '盾猛延迟造成击倒', 'DunMengJiDao', None),
    50005: _buff_data(50005, 2*16, 1, '流血_无炼狱无割裂', 'LiuXueInterval_1', None),
    50006: _buff_data(50006, 1*16, 1, '流血_有炼狱无割裂', 'LiuXueInterval_2', None),
    50007: _buff_data(50007, 2*16, 1, '流血_无炼狱有割裂', 'LiuXueInterval_3', None),
    50008: _buff_data(50008, 1*16, 1, '流血_有炼狱有割裂', 'LiuXueInterval_4', None),
    50009: _buff_data(50009, 999999*16, 3, '崇云_次数检测', None, None),
    50010: _buff_data(50010, 1, 1, '盾击无视防御目标标记buff', None, [53]),
    50011: _buff_data(50011, 1.5*16, 1, '卷雪刀内置cd', 'JuanXueDao', None),
    50012: _buff_data(50012, 15*16, 1, '乱天狼模拟内置cd', 'Halo_LingXue_5', None),
    50013: _buff_data(50013, 7*16, 1, '乱天狼模拟起手时间', 'Halo_LingXue_5', None),
    50014: _buff_data(50014, 8*16, 1, '寒甲AP期望buff', 'HanJiaDisappear', None),
}


