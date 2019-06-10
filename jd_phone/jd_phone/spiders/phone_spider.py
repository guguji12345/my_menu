# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import re
from jd_phone.items import JdPhoneItem
import json
import pymongo

class PhoneSpiderSpider(scrapy.Spider):
    name = 'phone_spider'
    allowed_domains = ['list.jd.com']
    start_urls = ['https://list.jd.com/list.html?cat=9987,653,655&page=1']

    def parse(self,response):
        total = response.xpath("//div[@class='p-wrap']/span[@class='p-num']/a[last()-1]/text()").extract_first()
        for i in range(1,2):#int(title)
            page_url = "https://list.jd.com/list.html?cat=9987,653,655&page={}".format(i)
            yield Request(url=page_url,callback=self.parse_id,dont_filter=True)#翻页


    def parse_id(self,response):#传入商品url至item便于直接打开商品进行浏览
        lis = response.xpath("//ul[@class='gl-warp clearfix']/li").extract()
        # client = pymongo.MongoClient(host="localhost", port=27017)
        # db = client["jd_phone"]
        # collection = db["JdPhoneItem"]#导入db库及collection
        for li in lis:
            item = JdPhoneItem()
            skuid = re.findall(r'.*?<div class="gl-i-wrap j-sku-item".*?data-sku="(.*?)".*?>',li,re.DOTALL)[0]#store_id
            venderid = re.findall(r'.*?<div class="gl-i-wrap j-sku-item".*?venderid="(.*?)".*?>',li,re.DOTALL)[0]#price_id
            item["price_id"]=venderid
            detail_url = "https://item.jd.com/{}.html".format(skuid)
            # result = collection.find_one({"url":detail_url})#查找detail_url是否在数据库中,用于数据去重,可实现暂停爬虫作用
            # if result!=None:#判断该url是否存在数据库中,若存在继续下一个商品url
            #     continue
            # else:#若不存在则继续抓取
            yield Request(url=detail_url,callback=self.parse_detail,meta={"item":item},dont_filter=True)#根据获取到的每个商品id来获取商品详情页url

    def parse_detail(self,response):#获取商品部分信息进行清洗后存入item
        item = response.meta['item']
        url = response.url
        item["url"]=url
        venderid = item["price_id"]
        skuid = re.findall(r'[0-9]+',url,re.DOTALL)[0]
        name = response.xpath("//div[@class='itemInfo-wrap']/div[@class='sku-name']//text()").extract()
        name = "".join(name).replace("\n","").strip()
        store = response.xpath("//div[@class='name']/a/text()")
        if store == []or store==None:
            item["store"] = "未注册店名"
        else:
            store = response.xpath("//div[@class='name']/a/text()").extract_first()
            item["store"]=store
        lis = response.xpath("//ul[@class='parameter1 p-parameter-list']/li/div[@class='detail']/p/text()").extract()
        params = {}
        for li in lis:
            li = li.replace("\xa0","").strip()
            chara = li.split("：")[0]
            param = li.split("：")[1]
            params[chara]=param#商品参数
        item["name"]=name
        item["params"]=params
        ques_url = "https://c0.3.cn/stock?skuId={}&cat=9987,653,655&venderId={}&area=22_1930_4284_0".format(skuid,venderid)
        yield Request(url=ques_url,callback=self.parse_price,meta={"item":item},dont_filter=True)

    def parse_price(self,response):#获取商品价钱存入item
        url = response.url
        item = response.meta['item']
        productid = re.findall(r'.*?skuId=(.*?)&cat=.*?',url,re.DOTALL)[0]
        json_str = json.loads(response.text,encoding="gbk")
        data = json_str["stock"]
        price = data["jdPrice"]["p"]
        item["price"] = price
        question_url = "https://question.jd.com/question/getQuestionAnswerList.action?page=1&productId={}".format(productid)
        yield Request(url=question_url,callback=self.parse_ques,meta={"item":item},dont_filter=True)#分析url规律由商品标价url获取问题及回复所在url


    def parse_ques(self,response):#获取商品问答情况进行清洗后存入item
        item = response.meta['item']
        json_str = json.loads(response.text)
        questions = json_str["questionList"]
        if questions == []:
            item["sale"] = "销量较少"
            item["question"] = "无问题及回复者"
        else:
            data_total = re.findall(r'.*?"totalItem":(.*?),.*?', response.text, re.DOTALL)[0]
            item["sale"] = int(data_total)
            q_as = []#question and answer
            for question in questions:
                q_a = {}#question and answer
                content = question["content"]
                answer = question["answerCount"]
                q_a["问题"]=content
                q_a["回答数量"]=answer
                q_as.append(q_a)
            item["question"]=q_as
        yield item#传入pipeline进行存库操作
