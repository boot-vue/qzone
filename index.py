from bs4 import BeautifulSoup
import requests
import os
import json


def parseAlbum():
    album = 'https://h5.qzone.qq.com/proxy/domain/photo.qzone.qq.com/fcgi-bin/fcg_list_album_v3?g_tk=587783151&callback=shine0_Callback&t=931567003&hostUin=497921268&uin=497921268&appid=4&inCharset=utf-8&outCharset=utf-8&source=qzone&plat=qzone&format=jsonp&notice=0&filter=1&handset=4&pageNumModeSort=40&pageNumModeClass=15&needUserInfo=1&idcNum=4&callbackFun=shine0&_=1533879399580'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        'cookie': 'QZ_FE_WEBP_SUPPORT=1; pgv_pvi=9063821312; ptui_loginuin=497921268; pt2gguin=o0497921268; RK=HUC9zWdBY8; ptcz=16c88e8f46d79e6cd9d9902c285546385d95b9c823780f849bff9e260feb51f1; pgv_pvid=2791074576; o_cookie=497921268; pac_uid=1_497921268; Loading=Yes; cpu_performance_v8=2; pgv_info=ssid=s5270845209; pgv_si=s9520270336; _qpsvr_localtk=0.20803666371411; ptisp=ctc; uin=o0497921268; skey=@yrRYuRF9N; p_uin=o0497921268; pt4_token=vSVNtuzi1g5BFcEx8ggLAW8xwoQLCZZui-Y-QNUECLc_; p_skey=SRT7QFNyuOdtp*0lZoh9Kl*zN8o2Y--MC5BWEnv13-4_'}
    res_album = requests.get(album, headers=headers).content.decode('utf-8')
    json_album = json.loads(res_album.split('(')[1].split(')')[0])
    print(json_album['data']['albumListModeSort'])


if __name__ == '__main__':
    parseAlbum()
