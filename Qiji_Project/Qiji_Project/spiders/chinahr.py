# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re
import datetime
from datetime import timedelta
# from Qiji_Project.items import DhinahrItem

from scrapy_redis.spiders import RedisCrawlSpider#爬虫集成 RedisCrawlSpider

class ChinahrSpider(RedisCrawlSpider):
    name = 'chinahr'
    allowed_domains = ['chinahr.com']
    # start_urls = ['http://www.chinahr.com/']
    redis_key = 'chinahrspider:start_urls'
    #匹配路径
    rules = (

        Rule(LinkExtractor(allow=r'chinahr.com/sou/'), follow=True),
        Rule(LinkExtractor(allow=r'chinahr.com/.*/jobs/\d+/')),
        Rule(LinkExtractor(allow=r'.chinahr.com/job/\d+.html'), callback='parse_item', follow=False),
        Rule(LinkExtractor(allow=r'/company/\d+.html'), follow=True),
        Rule(LinkExtractor(allow=r'chinahr.com/sou/?orderField=relate&page=\d+'), follow=True)

    )
    num_pattern = re.compile(r'\d+')
    #页面解析函数
    def parse_item(self, response):
        # item = DhinahrItem()
        item = {}
        #链接
        url = response.url
        # print(url)
        # 职位名称
        pname = response.xpath('//div[@class="base_info"]//span[@class="job_name"]/text()').extract()
        if not pname:
            pname = None
        else:
            pname = pname[0]
        #工资
        money = response.xpath('//span[@class="job_price"]/text()').extract()
        if money:
            money = money[0]
            smoney,emoney = self.process_money(money)
        else:
            smoney,emoney = None,None
        #工作城市
        location = response.xpath('//div[@class="job_require"]//span[@class="job_loc"]/text()').extract()
        if not location:
            location = None
        else:
            location = location[0]
        #工作经历
        year = response.xpath('//div[@class="job_require"]//span[@class="job_exp"]/text()').extract()
        if not year:
            syear,eyear = None,None
        else:
            year = year[0]
            syear,eyear = self.process_year(year)
        #学历
        degree = response.xpath('//div[@class="job_require"]//span[4]/text()').extract()
        if not degree:
            degree = None
        else:
            degree = degree[0]
        #工作类型
        ptype = response.xpath('//div[@class="job_require"]//span[3]/text()').extract()
        if not ptype:
            ptype = None
        else:
            ptype = ptype[0]

        tags = None
        #发布时间
        date_pub = response.xpath('//p[@class="updatetime"]/text()').extract()
        if not date_pub:
            date_pub = None
        else:
            date_pub = date_pub[0]
            date_pub = self.process_date(date_pub)
        #福利
        advantage = response.xpath('//ul[@class="clear"]//li/text()').extract()
        if not advantage:
            advantage = None
        else:
            advantage = advantage[0]
        #工作描述
        jobdesc = response.xpath('//div[@class="job_intro_info"]/text()').extract()
        if not jobdesc:
            jobdesc = None
        else:
            jobdesc = self.process_desc(jobdesc)
        #工作地点
        jobaddr = response.xpath('//div[@class="job_require"]//span[@class="job_loc"]/text()').extract()
        if not jobaddr:
            jobaddr = None
        else:
            jobaddr = jobaddr[0]
        # 公司名称
        company = response.xpath('//div[@class="job-detail-r"]//h4/a/text()').extract()
        if not company:
            company = None
        else:
            company = company[0]
        #抓取时间
        crawl_time = datetime.datetime.now().strftime('%Y-%m-%d')

        # print(url,pname,smoney,emoney,eyear,syear,degree,ptype,tags,date_pub,advantage,jobdesc,jobaddr,company,crawl_time)
        item["url"] = url
        item["pname"] = pname
        item["smoney"] = smoney
        item["emoney"] = emoney
        item["location"] = location
        item["syear"] = syear
        item["eyear"] = eyear
        item["degree"] = degree
        item["ptype"] = ptype
        item["tags"] = tags
        item["date_pub"] = date_pub
        item["advantage"] = advantage
        item["jobdesc"] = jobdesc
        item["jobaddr"] = jobaddr
        item["company"] = company
        item["crawl_time"] = crawl_time
        if item['pname'] != None:
            yield item

    #发布时间处理
    def process_date(self,value):
        if '今天' in value:
            date_pub = datetime.datetime.now().strftime('%Y-%m-%d')
        else:
            res = self.num_pattern.search(value).group()
            date_pub = (datetime.datetime.now() - timedelta(days=int(res))).strftime('%Y-%m-%d')
        return date_pub
    #工作经历处理
    def process_year(self,value):
        if '应届' in value:
            syear = 0
            eyear = 0
        else:
            res = self.num_pattern.search(value)
            if res is None:
                syear = None
                eyear = None
            else:
                syear = res.group()
                eyear = res.group()
        return syear,eyear
    #工资处理
    def process_money(self,value):
        if "面" not in value:
            smoney = value.split('-')[0]
            emoney = value.split('-')[1]
        else:
            smoney = 0
            emoney = 0
        return smoney,emoney
    #工作详情处理
    def process_desc(self,value):
        jobdesc = ''.join(value).replace('\r\n','').strip()
        return jobdesc



