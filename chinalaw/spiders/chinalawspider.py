# -*- coding: utf-8 -*-
import scrapy
import pymongo
from scrapy.conf import settings
import re
import datetime

from chinalaw.items import ChinalawItem
from chinalaw.items import ChinalawBrefItem

class ChinalawspiderSpider(scrapy.Spider):
    name = "chinalawspider"
    allowed_domains = ["chinalaw.gov.cn"]
    regurl = 'http://www.chinalaw.gov.cn/col/#ColCode#/index.html?uid=1648&pageNum=1'

    start_urls = ['http://www.chinalaw.gov.cn/']

    def __init__(self,page_max=settings['PAGE_MAX_DEFAULT'],update=settings['UPDATE_DEFAULT'],*args, **kwargs):
        self.page_max = int(page_max)
        ColCodes = ['col11','col12','col13','col14','col15']
        for colcode in ColCodes:
            url = self.regurl.replace('#ColCode#',colcode)
            self.start_urls.append(url)

    def parse(self, response):
        #print "res:",response.body
        #print "tp:",response.xpath('//*[@id="barrierfree_container"]/div[3]/div[2]/div[2]/script[4]/text()')
        total_pages = 50
        #print "total_pages:",total_pages
        #print "responseurl:",response.url
        if self.page_max == 1:
            end_page = int(total_pages)
        else:
            end_page = self.page_max
        for n in range(1,end_page + 1):
            strinfo = re.compile('pageNum=\d+')
            url = strinfo.sub('pageNum='+str(n),response.url)
            yield scrapy.Request(url, self.parse_list)

    def parse_list(self,response):
        
        links = response.xpath('//div[@id="1648"]')
        #print "response:",response.body
        #print "res_url:",response.url,
        #print "links:",links.extract()
        #print "chinalaws:",re.findall(r'\<li\>(.*?)\</li\>',links.extract()[0],re.M)
        chinalaws = re.findall(r'\<li\>(.*?)\</li\>',links.extract()[0],re.M)
        print "chinalaws:",chinalaws
        itembref = ChinalawBrefItem()
        for url in chinalaws:
            try:
         	#print "url:",url
                url0 = re.findall(r'href=\"(.*?)\"\>',url)[0]
                #print "url0:",url0
                gid=re.findall(r'art_(.*?).html',url0)[0]
                itembref['title'] = re.findall(r'html\"\>(.*?)\</a\>',url)[0]
                #print "title:",re.findall(r'html\"\>(.*?)\</a\>',url)[0]
                itembref['gid'] = gid
                itembref['urls'] = url0
                itembref['date'] = re.findall(r'\<span\>(.*?)\</span\>',url)[0]
                itembref['rksj'] = str(datetime.datetime.now())
                yield itembref
            except Exception,e:
                print "exception in parselist:",e
            finally:
                ex_href='http://www.chinalaw.gov.cn'
                href=ex_href+url0
                yield scrapy.Request(href, self.parse_detail)

    def parse_detail(self,response):
        item = ChinalawItem()
        url0 = response.url
        print "url in detail:",url0
        #print "res in detail:",response.body
        item['gid'] = re.findall(r'art_(.*?).html',url0)[0]
        item['urls'] = url0
        item['title2'] = response.xpath('//h3[@class="art_tit"]/text()').extract()[0]
        #item['text'] = response.xpath('//div[@id="zoom"]/*/text()').extract()
        item['html'] = response.body
        dr = re.compile(r'<[^>]+>',re.S)
        item['text'] = dr.sub('',response.body)
        item['maketime'] = response.xpath('//meta[@name="Maketime"]/@content').extract()[0]
        item['subsite'] = response.xpath('//meta[@name="subsite"]/@content').extract()[0]
        item['channel'] =response.xpath('//meta[@name="channel"]/@content').extract()[0]
        item['category'] =response.xpath('//meta[@name="category"]/@content').extract()[0]
        item['author'] = response.xpath('//meta[@name="author"]/@content').extract()[0]
        item['pubDate'] = response.xpath('//meta[@name="pubDate"]/@content').extract()[0]
        item['source'] = response.xpath('//meta[@name="source"]/@content').extract()[0]
        item['location'] = response.xpath('//meta[@name="location"]/@content').extract()[0]
        item['department'] = response.xpath('//meta[@name="department"]/@content').extract()[0]
        item['title'] = response.xpath('//meta[@name="title"]/@content').extract()[0]
        item['description'] = response.xpath('//meta[@name="description"]/@content').extract()[0]
        item['guid'] =response.xpath('//meta[@name="guid"]/@content').extract()[0]
        item['effectiveTime'] = response.xpath('//meta[@name="effectiveTime"]/@content').extract()[0]
        item['keyword'] =response.xpath('//meta[@name="keyword"]/@content').extract()[0]
        item['rksj'] = str(datetime.datetime.now())
        return item
