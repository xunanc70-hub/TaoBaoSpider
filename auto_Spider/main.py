from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from selenium import webdriver
from lxml import etree
import requests
import random
import time
import json
import ssl
import re
import os

class MainSpider:
    # 初始化，共用变量
    def __init__(self):
        self.url = "https://www.taobao.com"
        # 内网测试
        # self.url = "http://172.20.10.2/taobao"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
            "Referer": "https://item.taobao.com/"}
        ssl._create_default_https_context = ssl._create_unverified_context
        self.driver = uc.Chrome(version_main=148)
        self.driver.maximize_window()
        self.goods = []  # 商品名称
        self.goods_name = []  # 商铺名称
        self.goods_url = []  # 商品URL
        self.res = []   # 视频
        self.res1 = []  # 主图
        self.res2 = []  # 详情页
        self.res3 = []  # SKU
        self.video = [] # 视频(异常抛出)

    def refresh_cookies(self):
        cookies_path = "/Users/lamlam/PycharmProjects/auto_Spider/cookies.json"
        if os.path.exists(cookies_path):
            # 30天后cookies过期
            create_time = os.path.getctime(cookies_path)
            now = time.time()
            if now - create_time > 30 * 24 * 3600:
                os.remove(cookies_path)
                input("cookies过期，回车重新登录")
        if not os.path.exists(cookies_path):
            self.driver.get(self.url)
            time.sleep(random.uniform(1, 2))
            # 亲，请登录
            login_btn = self.driver.find_element(By.XPATH,
                                                 value='//div[@class = "site-nav-sign"]//a[contains(@href, "login.taobao.com") and contains(text(), "请登录")]')
            login_btn.click()  # selenium模拟真人点击
            # driver.execute_script("arguments[0].click();", login_btn)  # 浏览器底层触发点击
            time.sleep(random.uniform(1, 2))
            # 直接扫码最保险
            input("扫码登录，回车继续")
            # 程序自动登录
            # self.auto_login()
            cookies = self.driver.get_cookies()  # 获取cookies
            with open("cookies.json", "w") as f:
                json.dump(cookies, f)

    def auto_login(self):
        # 账号
        user_textarea = self.driver.find_element(By.XPATH, value='//input[contains(@name, "fm-login-id")]')
        user_textarea.clear()
        user_textarea.send_keys("")
        time.sleep(random.uniform(1, 2))
        # 密码
        pass_textarea = self.driver.find_element(By.XPATH, value='//input[contains(@name, "fm-login-password")]')
        pass_textarea.clear()
        pass_textarea.send_keys("")
        time.sleep(random.uniform(1, 2))
        # 同意协议
        agree_btn = self.driver.find_element(By.XPATH,
                                        value='//div[@class = "fm-agreement resize-window"]//input[contains(@name, "fm-agreement-checkbox")]')
        agree_btn.click()  # selenium模拟真人点击
        # driver.execute_script("arguments[0].click();", agree_btn)  # 浏览器底层触发点击
        time.sleep(random.uniform(1, 2))
        # 登录
        submit_btn = self.driver.find_element(By.XPATH,
                                         value='//div[@class = "fm-btn"]//button[contains(@type, "submit") and contains(text(), "登录")]')
        submit_btn.click()  # selenium模拟真人点击
        # driver.execute_script("arguments[0].click();", submit_btn)  # 浏览器底层触发点击
        time.sleep(random.uniform(1, 2))

    def cookies_login(self):
        # 判断是否为空白页
        current_url = self.driver.current_url
        if "chrome://new-tab-page/" in current_url:
            # 携带cookies访问
            self.driver.get("https://www.taobao.com/robots.txt")
            self.driver.delete_all_cookies()
            with open("cookies.json", "r") as f:
                cookies = json.load(f)
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            self.driver.refresh()
            self.driver.get(self.url)
            time.sleep(random.uniform(1, 2))

    def get_goods(self):
        with open("goods.txt", "r", encoding = "utf-8") as f:
            for line in f:
                # 删除换行符
                name = line.strip()
                if name:
                    self.goods.append(name)

    def loop(self):
        for goods in self.goods:
            # 切换窗口句柄至原始窗口
            handles = self.driver.window_handles
            self.driver.switch_to.window(handles[0])
            print(f"开始搜索商品:{goods}")
            self.get_goods_url(goods)
            for goods_name, goods_url in list(zip(self.goods_name, self.goods_url))[:2]:
                self.res = []
                self.res1 = []
                self.res2 = []
                self.res3 = []
                self.video = []
                self.get_res_url(goods_url)
                self.res_cleaning(res_list=self.res)
                self.res_cleaning(res_list=self.res1)
                self.res_cleaning(res_list=self.res2)
                self.res_cleaning(res_list=self.res3)
                self.download(goods, goods_name, res_list=self.res, folder_name="视频")
                self.download(goods, goods_name, res_list=self.res1, folder_name="主图")
                self.download(goods, goods_name, res_list=self.res2, folder_name="详情页")
                self.download(goods, goods_name, res_list=self.res3, folder_name="SKU")
            print(f"商品下载完毕:{goods}")
            self.driver.close()

    def get_goods_url(self, goods):
        # 输入商品名
        search_textarea = self.driver.find_element(By.XPATH, value = '//input[contains(@id, "q") and contains(@aria-label, "请输入搜索文字")]')
        search_textarea.clear()
        search_textarea.send_keys(goods)
        # search_textarea.send_keys("test", Keys.ENTER) # 直接回车提交
        time.sleep(random.uniform(1, 2))
        # 搜索
        search_btn = self.driver.find_element(By.XPATH, value = '//button[contains(@class, "btn-search tb-bg") and text() = "搜索"]')
        #search_btn.click()  # selenium模拟真人点击
        self.driver.execute_script("arguments[0].click();", search_btn)  # 浏览器底层触发点击
        time.sleep(random.uniform(1, 2))
        # 切换窗口句柄至最新窗口
        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[-1])
        # 获取DOM
        goods_html = self.driver.page_source
        # 获取商品URL(47条)
        self.goods_url = re.findall(pattern=r'data-spm-act-id="(\d{1,})"', string=goods_html)
        self.goods_name = self.goods_url.copy()
        for goods_url in range(len(self.goods_url)):
            self.goods_url[goods_url] = "https://detail.tmall.com/item.htm?id=" + self.goods_url[goods_url] + "&mi_id=0000rFOkF-oICZj8WCG8BzktvEp063pG-WO38LTAWAKaths"
        # https://item.taobao.com/item.htm?id={goods.name} :淘宝
        # https://detail.tmall.com/item.htm?id={goods.name} :天猫
        # &mi_id=0000rFOkF-oICZj8WCG8BzktvEp063pG-WO38LTAWAKaths :随机参数

    def slow_scrolling(self):
        # 缓慢平滑滚动页面
        last_h = self.driver.execute_script("return document.documentElement.scrollHeight")
        repeat = 0  # 滚动8次
        wait = 0  # 两次高度一致判定break
        while True:
            self.driver.execute_script("window.scrollBy({top:5000, behavior:'smooth'})")
            time.sleep(random.uniform(1,2))
            now_h = self.driver.execute_script("return document.documentElement.scrollHeight")
            repeat += 1
            if now_h == last_h:
                wait += 1
                if wait >= 2:
                    break
            if repeat == 8:
                break
            else:
                wait = 0
                last_h = now_h

    def get_res_url(self, goods_url):
        self.driver.get(goods_url)
        time.sleep(random.uniform(1, 2))
        # 自动滚动
        self.slow_scrolling()
        # self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(random.uniform(1, 2))
        # 定位按钮
        try:
            video_btn = self.driver.find_element(By.XPATH,
                                                 value='//div[starts-with(@class, "switchTabsItem--") and text() = "视频"]')
            video_btn.click()  # selenium模拟真人点击
            self.driver.execute_script("arguments[0].click();", video_btn)  # 浏览器底层触发点击
            time.sleep(random.uniform(1, 2))
        except NoSuchElementException:
            pass
        # 获取DOM
        html = self.driver.page_source
        # res视频 res1主图 res2详情页 res3SKU
        '''self.res = re.findall(pattern=r'(?:video-sh.cloudvideocdn.taobao.com|tbm-auth.alicdn.com)/.{,200}?auth_key.{,300}?taobao', string=html)
        if self.res:
            if "https:" not in self.res[0]:
                self.res[0] = "https://" + self.res[0]'''
        # JS
        try:
            self.video = [self.driver.execute_script("return document.querySelector('video').src")]
            if self.video:
                self.res = self.video
            else:
                self.res = []
        except:
            self.res = []
        # XPATH
        tree = etree.HTML(html)
        self.res1 = tree.xpath('//div[starts-with(@class, "thumbnailItem--WQyauvvr")]//img/@src')
        for res_url in range(len(self.res1)):
            if "https:" not in self.res1[res_url]:
                self.res1[res_url] = "https:" + self.res1[res_url]
        self.res2 = tree.xpath('//div[starts-with(@class, "descV8")]//img/@src')
        for res_url in range(len(self.res2)):
            if "https:" not in self.res2[res_url]:
                self.res2[res_url] = "https:" + self.res2[res_url]
        self.res3 = tree.xpath('//div[@class = "valueItemImgWrap--ZvA2Cmim"]//img/@src')
        for res_url in range(len(self.res3)):
            if "https:" not in self.res3[res_url]:
                self.res3[res_url] = "https:" + self.res3[res_url]
        # 打印下载地址测试
        # print(self.res, self.res1, self.res2, self.res3)
        # 保存下载地址测试
        # with open("test.txt", "w", encoding="utf-8") as f:
        #     f.write('\n'.join(self.res))

    def res_cleaning(self, res_list):
        # deduplication 数据去重
        new_res = list(dict.fromkeys(res_list))
        res_list.clear()
        res_list.extend(new_res)

    def download(self, goods, goods_name, res_list=None, folder_name=""):
        # 生成文件夹
        save_dir = os.path.join(goods, goods_name, folder_name)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        # 批量下载
        for idx, res_url in enumerate(res_list):
            try:
                media = requests.get(res_url, headers=self.headers)
                if media.status_code == 200:
                    if folder_name == "视频":
                        save_path = os.path.join(save_dir, f"mov_{idx}.mp4")
                        with open(save_path, "wb") as f:
                            f.write(media.content)
                        print(f"下载成功:{res_url}")
                        time.sleep(random.uniform(1, 2))
                    else:
                        save_path = os.path.join(save_dir, f"img_{idx}.jpg")
                        with open(save_path, "wb") as f:
                            f.write(media.content)
                        print(f"下载成功:{res_url}")
                        time.sleep(random.uniform(1, 2))
                else:
                    print(f"下载失败{media.status_code}:{res_url}")
                    time.sleep(random.uniform(1, 2))
            except Exception as err:
                print(f"error:{err},{res_url}")

# 主程序入口
if __name__ == "__main__":
    try:
        # 实例化对象
        spider = MainSpider()
        # 调用函数
        spider.refresh_cookies()
        spider.cookies_login()
        spider.get_goods()
        spider.loop()
    except Exception as e:
        print(f"error:{e}")
