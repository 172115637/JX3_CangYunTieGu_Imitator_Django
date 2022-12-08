from django.http import JsonResponse
import json


def portal(request):
    # 接收到的数据参数，可能需要考虑以下参数
    # 奇穴、魔盒配装JSON、睁眼、增益、寒甲环境

    options = {}
    # 是否开启增益
    if 'gain' in request.GET and request.GET['gain']:
        options['gain'] = request.GET['gain']
        print(options['gain'])
    data = {
        "username": "fullbook",
        "age": 25
    }
    return JsonResponse(data)
