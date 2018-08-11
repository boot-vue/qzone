import requests
import os, threading
import json


# 每次要更新cookie,  相册url后部分,  照片url后部分(注意拼接相册id与设置分页大小)


# https://h5.qzone.qq.com/proxy/domain/photo.qzone.qq.com/fcgi-bin/fcg_list_album_v3?
# cookie: .....
# 获取所有的相册数据  主要是拿到: id name total
def parseAlbum(url, cookie):
    albums = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        'cookie': cookie}
    res_album = requests.get(
        'https://h5.qzone.qq.com/proxy/domain/photo.qzone.qq.com/fcgi-bin/fcg_list_album_v3?' + url,
        headers=headers).content.decode('utf-8')
    try:
        json_album = json.loads(res_album.split('(')[1].split(')')[0])
        if ('albumListModeSort' not in json_album['data']):
            print("登录状态失效,重新获取链接与cookie")
        else:
            for item in json_album['data']['albumListModeSort']:
                albums.append({'id': item['id'], 'name': item['name'], 'total': item['total']})
            return albums
    except:
        print("登录状态失效,重新获取链接与cookie")


# https://h5.qzone.qq.com/proxy/domain/photo.qzone.qq.com/fcgi-bin/cgi_list_photo?
# 遍历所有的相册下的所有图片  id name ,每页1000
def parsePhotos(albums, cookie):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        'cookie': cookie}
    if (not albums):
        return
    else:
        for item in albums:
            urls = []
            id = item['id']  # 相册id
            name = item['name']  # 相册name
            if (name == '说说和日志相册' or name == '手机相册'):
                continue
            photo_list = requests.get(
                'https://h5.qzone.qq.com/proxy/domain/photo.qzone.qq.com/fcgi-bin/cgi_list_photo?' +
                'g_tk=970489861&callback=shine0_Callback&t=472636949&mode=0&idcNum=4&hostUin=497921268&' +
                'topicId=' + id + '&noTopic=0&uin=497921268&pageStart=0&pageNum=1000&skipCmtCount=0&singleurl=1&batchId=&notice=0&appid=4&inCharset=utf-8' +
                '&outCharset=utf-8&source=qzone&plat=qzone&outstyle=json&format=jsonp&json_esc=1&question=&answer=&callbackFun=shine0&_=1533966634780',
                headers=headers).content.decode('utf-8')
            photo_data = json.loads(photo_list.split('(')[1].split(')')[0])
            photos = photo_data['data']['photoList']
            for it_photo in photos:
                if it_photo['raw']:
                    urls.append(it_photo['raw'])
                else:
                    urls.append(it_photo['origin_url'])
                with open('./' + name + '.txt', 'w+') as f:
                    f.write(it_photo['raw'] or it_photo['origin_url'] + '\n')
            # 开启线程下载(多线程有点问题,图片太多中途http请求好像会中断)
            thread = threading.Thread(target=download, args=(name, urls))
            thread.start()
            # download(name, urls)


# 下载 urls[ ] 图片链接,  name:文件夹名
def download(name, urls):
    print('开始下载  ' + name + ' 下的照片')
    if os.path.exists(name):
        pass
    else:
        os.mkdir(name)
    index = 0
    while index < len(urls):
        photo = requests.get(urls[index]).content
        img_name = '%s.jpg' % index
        with open('./' + name + '/' + img_name, 'wb') as f:
            f.write(photo)
        index = index + 1
    print(name + ' 下的照片下载完毕')


if __name__ == '__main__':
    # cookie每次要自行获取
    url = 'g_tk=970489861&callback=shine0_Callback&t=991992486&hostUin=497921268&uin=497921268&appid=4&inCharset=utf-8&outCharset=utf-8&source=qzone&plat=qzone&format=jsonp&notice=0&filter=1&handset=4&pageNumModeSort=40&pageNumModeClass=15&needUserInfo=1&idcNum=4&callbackFun=shine0&_=1533966302018'
    cookie = 'pgv_pvi=3678962688; ptui_loginuin=497921268; pt2gguin=o0497921268; RK=1UC9yWdwZe; ptcz=6c1b11124de886738ef664d4893662b86b7c7217b6e67e0c7965f2244fb7e0d3; pgv_pvid=9073299548; QZ_FE_WEBP_SUPPORT=1; cpu_performance_v8=0; __Q_w_s__QZN_TodoMsgCnt=1; pgv_si=s8893934592; _qpsvr_localtk=0.37554995097100563; ptisp=ctc; uin=o0497921268; skey=@kBZpbDcaP; p_uin=o0497921268; pt4_token=0cmykMAzUDg-2V*4gG4USagiCyVpTRZGHrv-*mZhR2g_; p_skey=LwVBEIsT41hQhtPbqv8LwkzFKsIYqoXqEVyL1z*UJTg_; Loading=Yes; pgv_info=ssid=s2065686180'
    albums = parseAlbum(url, cookie)  # 所有的相册
    parsePhotos(albums, cookie)  # 所有的照片url&&按相册下载
