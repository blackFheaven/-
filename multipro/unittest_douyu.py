import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from lxml import etree
chrom_options = Options()
chrom_options.add_argument('--headless')
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from queue import Queue
import threading
class douyu(unittest.TestCase):

    #初始化方法
    def setUp(self):
        self.driver = webdriver.Chrome(executable_path=r'E:\Python 3.6.5\Scripts\chromedriver.exe',
                                       chrome_options=chrom_options)
        self.file = open('../photo/douyu.json','a',encoding='utf-8',)
        self.over_flag =False
        self.queue = Queue()
        for i in range(1,11):
            t = threading.Thread(target=self.save_file,args=('threading_'+str(i),1))
            t.start()


    def save_file(self,*args):
        print('%s线程开启'%args[0])
        while True:
            if self.over_flag and self.queue.empty():
                self.file.close()
                break
            try:
                self.file.write(self.queue.get(timeout=3)+'\n')
                self.queue.task_done()
            except Exception as e:
                print('取消阻塞或者存入失败！',e)
        print('%s线程结束' % args[0])



    def test_douyu(self):
        self.driver.get("https://www.douyu.com/directory/all")
        self.num=0
        self.stop_num = 0



        while True:
            WebDriverWait(self.driver, 20).until(
                ec.presence_of_element_located(
                    (By.CLASS_NAME, 'ListFooter')
                )
            )
            html = etree.HTML(self.driver.page_source)
            ul = html.xpath(".//ul[@class='layout-Cover-list']//li")

            #在线直播
            for item in ul:
                type = item.xpath(".//div[@class='DyListCover-content']/div[1]/span")[0].text
                title = item.xpath(".//div[@class='DyListCover-content']/div[1]/h3")[0].text
                #人气
                popularity = item.xpath(".//div[@class='DyListCover-content']/div[2]/span/text()")[0]
                name = item.xpath(".//div[@class='DyListCover-content']/div[2]/h2/text()")[0]
                print('类型：%s  标题%s  人气%s  主播名字%s'%(type,title,popularity,name))
                dict1=json.dumps({
                    'type':type,'title':title,'popularity':popularity,'name':name
                },ensure_ascii=False)
                self.queue.put(dict1)
                self.num+=1

            # print(html.xpath(".//div[@class='ListFooter']"))
            print(html.xpath(".//div[@class='ListFooter']/ul/li[last()]/@aria-disabled")[0] =='true')
            # if self.stop_num==40 or html.xpath(".//div[@class='ListFooter']/ul/li[last()]/@aria-disabled")[0] =='ture':
            if  html.xpath(".//div[@class='ListFooter']/ul/li[last()]/@aria-disabled")[0] =='True':
                self.over_flag =True
                break
            self.driver.find_element_by_xpath(".//div[@class='ListFooter']/ul/li[last()]").click()
            self.stop_num+=1
            print('第%s页'%str(self.stop_num))

    def tearDown(self):
        print('人数：',self.num)
        self.driver.close()

        print('爬取结束')

