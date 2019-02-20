# coding=utf-8
#from lxml import etree
#from urllib.parse import unquote
import re

testStr = '''<!DOCTYPE html PUBLIC "-//WAPFORUM//DTD XHTML Mobile 1.0//EN" "http://www.wapforum.org/DTD/xhtml-mobile10.dtd"><html xmlns="http://www.w3.org/1999/xhtml"><!--STATUS OK--><!--STATIC http://static.tieba.baidu.com/tb/mobile/wfrs20120222_62351 --><head><meta name="keywords" content="贴吧,百度贴吧,论坛,兴趣,社区,BBS" /><meta name="description" content="百度贴吧——全球最大的中文社区。贴吧的使命是让志同道合的人相聚。不论是大众话题还是小众话题，都能精准地聚集大批同好网友，展示自我风采，结交知音，搭建别具特色的“兴趣主题“互动平台。贴吧目录涵盖游戏、地区、文学、动漫、娱乐明星、生活、体育、电脑数码等方方面面，是全球最大的中文交流平台，它为人们提供一个表达和交流思想的自由网络空间，并以此汇集志同道合的网友。" /><meta http-equiv="Content-Type" content="application/xhtml+xml; charset=UTF-8"/><meta http-equiv="Content-Type" content="text/html; charset=utf-8; X-Wap-Proxy-Cookie=none" /><style type="text/css">body{font-size:small;line-height:1.4em;margin:1px;}form{margin:0;padding:0;}a{text-decoration: none;};a img{border:none;}.light{color:#c60a00;}html{-webkit-text-size-adjust:none;} .bc{background-color:#EFF2FA;}.g{color:#AAA;}.b{color:#008000;}.p,.h{padding:5px 0 5px 5px;margin-bottom:1px}p{margin:0;color:#008000}.i{margin-bottom:3px;}table{width:100%;border-collapse:collapse;border-spacing:0}.q{width:95%;}.r{text-align:right;}img{border:none;}.x{background-color:#E5E5E5;}.x a:visited{color: #551A8B;}.b2{background-color:#F9F2DB}#insert_smile{background:none;border:none;font-size:small;color:blue;}.advertise{display: block;color: red;}.advertise_top{}.advertise_top_0{}.post_client_down{font-size: 12px;margin-left: 20px;color: red;}.post_top_client{color: #c60a00;}</style><title>百度贴吧——全球最大的中文社区</title></head><body><div><a name="top"></a><div class="bc">李毅吧&#160;第1页<br/><table><td>全部&#160;|&#160;<a href="/mo/q---C3F1786E09CF261FC1E78643F7431237%3AFG%3D1--1-3-0--2--wapp_1547294334085_433/m?kw=%E6%9D%8E%E6%AF%85&amp;lm=4&amp;lp=5001&amp;pinf=1_2_0">精品</a>&#160;|&#160;<a href="#post">发贴</a></td><td class="r"><a href="/mo/q---C3F1786E09CF261FC1E78643F7431237%3AFG%3D1--1-3-0--2--wapp_1547294334085_433/m?kw=%E6%9D%8E%E6%AF%85&amp;lm=&amp;lp=5003">刷新</a></td></table></div><div class="i"><a href="/mo/q---C3F1786E09CF261FC1E78643F7431237%3AFG%3D1--1-3-0--2--wapp_1547294334085_433/m?kz=5995791822&amp;is_bakan=0&amp;lp=5010&amp;pinf=1_2_0">1.&#160;【妹子团1月招募】发放红包、专属印记、贴吧结婚！</a>[<span class="light">顶</span>]    <p>点0&#160;回362&#160;梓雨宸&#160;18:09</p></div><div class="i x"><a href="/mo/q---C3F1786E09CF261FC1E78643F7431237%3AFG%3D1--1-3-0--2--wapp_1547294334085_433/m?kz=5994937711&amp;is_bakan=0&amp;lp=5010&amp;pinf=1_2_0">2.&#160;【公告】帝吧招募2019首批吧务，物质奖励丰富收获荣誉</a>[<span class="light">顶</span>]    <p>点0&#160;回469&#160;24开K&#160;19:58</p></div><div class="i"><a href="/mo/q---C3F1786E09CF261FC1E78643F7431237%3AFG%3D1--1-3-0--2--wapp_1547294334085_433/m?kz=5983738416&amp;is_bakan=0&amp;lp=5010&amp;pinf=1_2_0">3.&#160;【公告】目前在帝吧会被删帖的帖子类型，被删帖之后的处理方式</a>[<span class="light">顶</span>]    <p>点0&#160;回69&#160;爱就1437&#160;1-11</p></div><div class="i x"><a href="/mo/q---C3F1786E09CF261FC1E78643F7431237%3AFG%3D1--1-3-0--2--wapp_1547294334085_433/m?kz=5949934464&amp;is_bakan=0&amp;lp=5010&amp;pinf=1_2_0">4.&#160;【帝吧相亲大会】第5届帝吧相亲大会正式开始，非诚勿扰</a>[<span class="light">顶</span>]    <p>点0&#160;回1115&#160;关爱韩关河&#160;16:59</p></div><div class="i"><a href="/mo/q---C3F1786E09CF261FC1E78643F7431237%3AFG%3D1--1-3-0--2--wapp_1547294334085_433/m?kz=6005721352&amp;is_bakan=0&amp;lp=5010&amp;pinf=1_2_0">5.&#160;分享一些南方大型花 卉交易市场的不同品种。</a>    <p>点0&#160;回0&#160;&#160;19:58</p></div><div class="i x"><a href="/mo/q---C3F1786E09CF261FC1E78643F7431237%3AFG%3D1--1-3-0--2--wapp_1547294334085_433/m?kz=5297519610&amp;is_bakan=0&amp;lp=5010&amp;pinf=1_2_0">6.&#160;你们玩的高频彩是不是这个样子的</a>    <p>点9&#160;回9&#160;dwqawm062840e&#160;19:58</p></div><div class="i"><a href="/mo/q---C3F1786E09CF261FC1E78643F7431237%3AFG%3D1--1-3-0--2--wapp_1547294334085_433/m?kz=6005715072&amp;is_bakan=0&amp;lp=5010&amp;pinf=1_2_0">7.&#160;女朋友闻见烟味恶心怎么办</a>    <p>点0&#160;回4&#160;伏特加丿&#160;19:58</p></div><div class="i x"><a href="/mo/q---C3F1786E09CF261FC1E78643F7431237%3AFG%3D1--1-3-0--2--wapp_1547294334085_433/m?kz=6005641749&amp;is_bakan=0&amp;lp=5010&amp;pinf=1_2_0">8.&#160;这是哄女票的最新方式？</a>    <p>点0&#160;回12&#160;指尖墨陌&#160;19:58</p></div><div class="i"><a href="/mo/q---C3F1786E09CF261FC1E78643F7431237%3AFG%3D1--1-3-0--2--wapp_1547294334085_433/m?kz=6004605999&amp;is_bakan=0&amp;lp=5010&amp;pinf=1_2_0">9.&#160;虚心请教，之前斗鱼有个主播叫铃原爱蜜莉的，有一个毛衣系列很火</a>    <p>点0&#160;回40&#160;&#160;19:58</p></div><div class="i x"><a href="/mo/q---C3F1786E09CF261FC1E78643F7431237%3AFG%3D1--1-3-0--2--wapp_1547294334085_433/m?kz=6005224239&amp;is_bakan=0&amp;lp=5010&amp;pinf=1_2_0">10.&#160;女生的朋友圈，发现直男们简直蠢到无法呼吸了！【转】</a>    <p>点0&#160;回62&#160;小郡主芊芊&#160;19:58</p></div><div class="i"><a href="/mo/q---C3F1786E09CF261FC1E78643F7431237%3AFG%3D1--1-3-0--2--wapp_1547294334085_433/m?kz=6004588140&amp;is_bakan=0&amp;lp=5010&amp;pinf=1_2_0">11.&#160;女人真的是耐寒的动物</a>    <p>点0&#160;回72&#160;小懂090全讯网&#160;19:58</p></div><div class="i x"><a href="/mo/q---C3F1786E09CF261FC1E78643F7431237%3AFG%3D1--1-3-0--2--wapp_1547294334085_433/m?kz=6003710343&amp;is_bakan=0&amp;lp=5010&amp;pinf=1_2_0">12.&#160;是东莞大哥造的吗</a>    <p>点0&#160;回51&#160;a409862202&#160;19:58</p></div><div class="i"><a href="/mo/q---C3F1786E09CF261FC1E78643F7431237%3AFG%3D1--1-3-0--2--wapp_1547294334085_433/m?kz=6005461204&amp;is_bakan=0&amp;lp=5010&amp;pinf=1_2_0">13.&#160;我选第二个有错吗</a>    <p>点0&#160; 回46&#160;Skyalone_wolf&#160;19:58</p></div><div class="i x"><a href="/mo/q---C3F1786E09CF261FC1E78643F7431237%3AFG%3D1--1-3-0--2--wapp_1547294334085_433/m?kz=6005664039&amp;is_bakan=0&amp;lp=5010&amp;pinf=1_2_0">14.&#160;女朋友要和教练去看电影，我炸了</a>    <p>点0&#160;回55&#160;吃不到的青苹果&#160;19:58</p></div><div class="i"><a href="/mo/q---C3F1786E09CF261FC1E78643F7431237%3AFG%3D1--1-3-0--2--wapp_1547294334085_433/m?kz=5978193552&amp;is_bakan=0&amp;lp=5010&amp;pinf=1_2_0">15.&#160;有没有特别污而且有内涵的情侣网名&#160;跪求</a>    <p>点0&#160;回107&#160;蜗居的蟹蟹40&#160;19:58</p></div><div class="i x"><a href="/mo/q---C3F1786E09CF261FC1E78643F7431237%3AFG%3D1--1-3-0--2--wapp_1547294334085_433/m?kz=5981478885&amp;is_bakan=0&amp;lp=5010&amp;pinf=1_2_0">16.&#160;挑战整个吧的QQ等级，还有谁比我更高？</a>    <p>点0&#160;回992&#160;非诚百科&#160;19:58</p></div><div class="i"><a href="/mo/q---C3F1786E09CF261FC1E78643F7431237%3AFG%3D1--1-3-0--2--wapp_1547294334085_433/m?kz=6005650640&amp;is_bakan=0&amp;lp=5010&amp;pinf=1_2_0">17.&#160;奶奶从集市里买买了一头小母狗这 ，后来这条母狗生了4胎2黄1黑</a>    <p>点0&#160;回4&#160;zhou852927111&#160;19:58</p></div><div class="i x"><a href="/mo/q---C3F1786E09CF261FC1E78643F7431237%3AFG%3D1--1-3-0--2--wapp_1547294334085_433/m?kz=6003476145&amp;is_bakan=0&amp;lp=5010&amp;pinf=1_2_0">18.&#160;不懂就问，女生穿成这样你该怎么办</a>    <p>点0&#160;回91&#160;lfiyc&#160;19:57</p></div><div class="i"><a href="/mo/q---C3F1786E09CF261FC1E78643F7431237%3AFG%3D1--1-3-0--2--wapp_1547294334085_433/m?kz=6001526212&amp;is_bakan=0&amp;lp=5010&amp;pinf=1_2_0">19.&#160;你会怎么选</a>    <p>点0&#160;回85&#160;M78Mebius&#160;19:57</p></div><div class="i x"><a href="/mo/q---C3F1786E09CF261FC1E78643F7431237%3AFG%3D1--1-3-0--2--wapp_1547294334085_433/m?kz=6005721782&amp;is_bakan=0&amp;lp=5010&amp;pinf=1_2_0">20.&#160;老哥们，找个人</a>    <p>点0&#160;回0&#160;zyclctime&#160;19:57</p></div><form action="/mo/q---C3F1786E09CF261FC1E78643F7431237%3AFG%3D1--1-3-0--2--wapp_1547294334085_433/m" method="get"><div class="bc p">        <a accesskey="6" href="/mo/q---C3F1786E09CF261FC1E78643F7431237%3AFG%3D1--1-3-0--2--wapp_1547294334085_433/m?kw=%E6%9D%8E%E6%AF%85&amp;lp=5011&amp;lm=&amp;pn=20">下一页</a>&#160;第1/910680页<input type="text" name="pnum" size="5" value="910680"/><input type="hidden" name="lm" value=""/><input type="hidden" name="tnum" value="18213584"/><input type="hidden" name="kw" value="李毅"/><input type="hidden" name="lp" value="5009"/><input type="hidden" name="pinf" value="1_2_0"/><input type="submit" name="sub" value="跳页"/></div></form>    <div class="bc p"><a href="/mo/q---C3F1786E09CF261FC1E78643F7431237%3AFG%3D1--1-3-0--2--wapp_1547294334085_433/m?tn=bdAlbLst&amp;word=%E6%9D%8E%E6%AF%85&amp;lp=3001&amp;pinf=1_2_0">本吧图库</a>                &#160;|&#160;<a href="/mo/q---C3F1786E09CF261FC1E78643F7431237%3AFG%3D1--1-3-0--2--wapp_1547294334085_433/m?tn=bdBIW&amp;word=%E6%9D%8E%E6%AF%85&amp;lp=5016">关于本吧</a></div>        <a name="post"></a>
<div class="d h">
            <form action="/mo/q---C3F1786E09CF261FC1E78643F7431237%3AFG%3D1--1-3-0--2--wapp_1547294334085_433/submit" method="post">
            <div>
                标题:
                                <br/><input type="text" name="ti" id="ti" maxlength="500" class="q" /><br/>
                内容:<span class="g">[选填]</span><br/>
                <input type="text" name="co" maxlength="5000" class="q" /><br/>
                <input type="hidden" name="src" value="2"/><input type="hidden" name="word" value="李毅"/>
                <input type="hidden" name="tbs" value="fd8f86abe3a9ca461547294334"/>
                <input type="hidden" name="ifpost" value="0"/>
                <input type="hidden" name="ifposta" value="0"/>
                <input type="hidden" name="post_info" value="1"/>
                <input type="hidden" name="tn" value="baiduWiseSubmit"/>
                <input type="hidden" name="fid" value="59099"/>
                <input type="hidden" name="verify" value=""/>
                <input type="hidden" name="verify_2" value=""/>
                <input type="hidden" name="pinf" value="1_2_0"/>
                <input type="hidden" name="pic_info" value=""/>
                <input type="hidden" name="no_post_pic" value="0"/>

                                                <input type="submit" name="sub1" value="发贴"/>
                                                        <br/>参与本吧讨论请先<a href="http://wappass.baidu.com/passport/?login&amp;u=http%3A%2F%2Ftieba.baidu.com%2Fmo%2Fq---%2Csz%40320_240-1-3%2Fm%3Fkw%3D%25E6%259D%258E%25E6%25AF%2585%26pn%3D0&amp;ssid=&amp;from=&amp;uid=C3F1786E09CF261FC1E78643F7431237%3AFG%3D1&amp;pu=&amp;auth=&amp;originid=2&amp;mo_device=1&amp;bd_page_type=1&amp;tn=bdIndex&amp;regtype=1&amp;tpl=tb">登录</a>
                            </div>
        </form>
    </div>
        <form action="/mo/q---C3F1786E09CF261FC1E78643F7431237%3AFG%3D1--1-3-0--2--wapp_1547294334085_433/m" method="get"><div class="d"><input type="text" name="word" value="" class="q grey" id="word"/><br/><input type="hidden" name="tn6" value="bdISP"/><input type="hidden" name="tn4" value="bdKSW"/><input type="hidden" name="tn7" value="bdPSB"/><input type="hidden" name="lp" value="5015"/><input type="submit" name="sub4" value="进吧"/> <input type="submit" name="sub6" value="进i贴吧"/> <input type="submit" name="sub7" value="搜贴"/></div></form>        <a href="http://wappass.baidu.com/passport/?login&amp;u=http%3A%2F%2Ftieba.baidu.com%2Fmo%2Fq---C3F1786E09CF261FC1E78643F7431237%253AFG%253D1--1-3-0--2--wapp_1547294334085_433%2Furs%3Fsrc%3D2%26word%3D%25E6%259D%258E%25E6%25AF%2585%26lp%3D6025&amp;ssid=&amp;from=&amp;uid=C3F1786E09CF261FC1E78643F7431237%3AFG%3D1&amp;pu=&amp;auth=&amp;originid=2&amp;mo_device=1&amp;bd_page_type=1&amp;tn=bdIndex&amp;regtype=1&amp;tpl=tb">阅读设置</a><br/>            <a href="/mo/q---C3F1786E09CF261FC1E78643F7431237%3AFG%3D1--1-3-0--2--wapp_1547294334085_433/m?tn=bdIndex&amp;lp=5014">贴吧</a>&#160;&lt;&#160;<a href="//wap.baidu.com/?lp=5014&amp;ssid=&amp;from=&amp;uid=C3F1786E09CF261FC1E78643F7431237%3AFG%3D1&amp;pu=&amp;auth=&amp;originid=2&amp;mo_device=1&amp;bd_page_type=1">百度</a><br/>        <div style="text-align:center;"><a href="#top"><img src="//wap.baidu.com/r/wise/wapsearchindex/top.gif" alt="TOP"/></a></div>    2019-1-12&#160;19:58</div></body></html>'''
# html = etree.HTML(testStr)
# divList = html.xpath("//div[contains(@class,'i')]")
#
# for div in divList:
#     item = {}
#     print("title:" + div.xpath("./a/text()")[0] if len(div.xpath("./a/text()")[0]) > 0 else None)
#     print("href:" + div.xpath("./a/@href")[0] if len(div.xpath("./a/@href")[0]) > 0 else None)
#
# print(html)

# line = "http://c.hiphotos.baidu.com/forum/w%3D96%3Bq%3D45%3Bg%3D0/sign=e967ec4036c79f3d8fe1e83681d0f025/cd11728b4710b912e8a65f41cefdfc039245222d.jpg?&src=http%3A%2F%2Fimgsrc.baidu.com%2Fforum%2Fpic%2Fitem%2Fcd11728b4710b912e8a65f41cefdfc039245222d.jpg"
# url = re.search("&src=.*", line).group(0)[5:]
# url = unquote(url, 'utf-8')[39:]
# print(url)

# line = r"8IqW0jdnxx1xbK/tb/edi?tor/@!images/client/image_emoticon25.png"
# print(line)
# # url = line.replace('/', '')
# # url = line.translate(None, "@?/|\! ")
# url = re.sub('[!@#$/]', '', line)
# print(url)

msg = u"【【西大荒和田骏枣1000克】新疆特产大红枣子零食干果红枣新货好吃】https://m.tb.cn/h.3Hhzrqn?sm=99d12d 点击链接，再选择浏览器咑閞；或復·制这段描述￥KqdCbrSVRqC￥后打开手机淘宝"
msg = re.search(ur'https://.* ', msg).group().replace(u' ，', '')
print msg

#urlTemp = "https://www.qiushibaike.com/hot/page/{}/"
#print(urlTemp.format(2))
