# TaoBaoSpider
基于selenium的Chrome淘宝自动化爬虫项目
目的是获取指定商品的视频 主图 详情页 SKU（仅含图片及视频）
仅用作学习研究，禁止商用，非法爬取及违规使用，滥用后果自负
如有侵权，请联系删除

Spider是一个半自动爬虫
需要在self.url中补全淘宝商品详情页url

auto_Spider是一个全自动爬虫
需要在goods.txt文件中一行一个地写入商品名
在main.py中的loop函数中
for goods_name, goods_url in list(zip(self.goods_name, self.goods_url))[:2]:
可修改[:2]中的数字更改每件商品爬取的店铺数量

最新版Chrome可删去以下代码
ssl._create_default_https_context = ssl._create_unverified_context
self.driver = uc.Chrome(version_main=148)

第一次登录需要扫码获取cookies
注意cookies过期时间
或开启self.auto_login()
并在
user_textarea.send_keys("")中补全账号
pass_textarea.send_keys("")中补全密码
值得注意的是使用auto_login()函数有几率触发人机验证
触发账号风控，一般情况不建议使用

注意控制time.sleep()时长避免占用过多服务器资源

满意的话请点个星星吧
感谢
