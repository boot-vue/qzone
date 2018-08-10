from bs4 import BeautifulSoup
import requests
import os
import json


# album: https://h5.qzone.qq.com/proxy/domain/photo.qzone.qq.com/fcgi-bin/fcg_list_album_v3
# cookie: .....
def parseAlbum(album_url, cookie):
    album = album_url
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        'cookie': cookie}
    res_album = requests.get(album, headers=headers).content.decode('utf-8')
    json_album = json.loads(res_album.split('(')[1].split(')')[0])
    if ('t' in json_album['data']):
        print("操作太快了,稍后再试")
    else:
        print(json_album['data']['albumListModeSort'])


if __name__ == '__main__':
    parseAlbum(
        'https://h5.qzone.qq.com/proxy/domain/photo.qzone.qq.com/fcgi-bin/fcg_list_album_v3?g_tk=2096679417&callback=shine0_Callback&t=659747349&hostUin=497921268&uin=497921268&appid=4&inCharset=utf-8&outCharset=utf-8&source=qzone&plat=qzone&format=jsonp&notice=0&filter=1&handset=4&pageNumModeSort=40&pageNumModeClass=15&needUserInfo=1&idcNum=4&callbackFun=shine0&_=1533893913216',
        'QZ_FE_WEBP_SUPPORT=1; pgv_pvi=9063821312; ptui_loginuin=497921268; pt2gguin=o0497921268; RK=HUC9zWdBY8; ptcz=16c88e8f46d79e6cd9d9902c285546385d95b9c823780f849bff9e260feb51f1; pgv_pvid=2791074576; o_cookie=497921268; pac_uid=1_497921268; Loading=Yes; __Q_w_s__QZN_TodoMsgCnt=1; pgv_si=s909514752; _qpsvr_localtk=0.6815060152235186; ptisp=ctc; uin=o0497921268; skey=@7OYHcjacj; p_uin=o0497921268; pt4_token=SJq-X2ib2KuLOmo2po*JSeJOxCjTPDRxSuOyA8CCGCE_; p_skey=aQ4VdLOuzNVwyBSfQJwg4Rv3MKD7ucHNWMH9wHKMJU8_; pgv_info=ssid=s8142719742; cpu_performance_v8=11')
