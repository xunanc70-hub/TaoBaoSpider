# TaoBaoSpider
基于selenium的Chrome淘宝自动化爬虫项目
目的是获取指定商品的视频 主图 详情页 SKU（仅含图片及视频）
仅用作学习研究，禁止商用，非法爬取及违规使用，滥用后果自负
如有侵权，请联系删除

根据Chrome浏览器版本更改version_main=xxx(第27行代码)
self.driver = uc.Chrome(version_main=148)

根据提示安装软件包

Spider是一个半自动爬虫
需要在self.url中更改淘宝商品详情页url(第20行代码)
更改你的cookies_path路径(第35行代码)

auto_Spider是一个全自动爬虫
需要在goods.txt文件中一行一个地写入商品名(先清空)
在main.py中的loop函数中(第118行代码)
for goods_name, goods_url in list(zip(self.goods_name, self.goods_url))[:2]:
可修改[:2]中的数字更改每件商品爬取的店铺数量
更改你的cookies_path路径(第39行代码)

第一次登录需要扫码获取cookies
注意cookies过期时间
或在(第49行代码)开启self.auto_login()
并在
user_textarea.send_keys("")中补全账号(第58行代码)
pass_textarea.send_keys("")中补全密码(第63行代码)
值得注意的是使用auto_login()函数有几率触发人机验证
容易触发账号风控，一般情况不建议使用

注意在(第179,185,188行代码)
控制time.sleep(random.uniform(a,b))
每条请求等待a-b秒(建议慢一点)
避免占用过多服务器资源

满意的话请点个星星吧
感谢
