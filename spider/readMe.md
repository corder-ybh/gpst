###使用代理注意事项
- 1、准备ip池
- 2、如何随机选择IP地址
  - {"ip":ip,"times":0}
  - [{},{}]对这个ip的列表进行排序，按照使用次数进行排序
  - 选择使用次数最少的10个ip
###1、检查IP可用性
    - 1、设置request超时
    - 2、使用代理检测地址

###携带cookie请求
  - cookie组成cookie池

###请求登陆之后网站的思路
  - 实例化session
  - 先使用session发送请求，登陆对网站，把cookie保存在session中
  - 再使用session请求登陆之后才能访问的网站，session能自动的携带登陆成功时保存在其中的cookie

###不发送post请求，使用cookie获取登陆后的页面
  - 1、cookie获取时间很长的网站 政府、学校 除大多数互联网公司之外的
  - 2、在cookie过期之前能拿到所有的数据，比较麻烦
  - 3、配合其他程序一起使用，有程序专门进行登陆获取cookie操作，当前程序专门获取页面

###寻找表单中action来寻找post地址
   - 如果没有，则用抓包，抓包，如果发现跳转，可以勾选process log，或者输入错误密码
   - search on file 可以搜索所有内容，包括js
   - 选择按钮，右边会出现enent_listener
   - source下的值，复制到console下可以直接显示
   - source下js中可以点击左边打断点，左下角可以格式化
   - 查看js操作的动作，然后在python中模拟的操作（但是这种比较麻烦）

####tips:
  1. 尽量使用返回json的url，可以使用chrome切换手机页面和使用手机
  app抓包软件
  2. 在response中搜索中文可能搜不到，因为可能被转义，但是在priview中就没有此问题
  3. network中，可以使用ctrl来多选不同的类型xhr指ajax，如果过滤效果不好，也可以使用右上角search on file
     