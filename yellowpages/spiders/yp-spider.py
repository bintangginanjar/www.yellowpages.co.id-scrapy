import scrapy

from scrapy.loader import ItemLoader
from yellowpages.items import YellowpagesItem

class YpSpider(scrapy.Spider):
    name = 'yp'
    baseUrl = 'https://yellowpages.co.id/'
    
    custom_settings = {
        'FEED_EXPORT_FIELDS': [
            'bidang',
            'kategori',
            'pageUrl',
            'namaClient',
            'alamat',
            'kota',
            'noTelp',
            'email',
            'site'
        ]
    }    

    def start_requests(self):
        self.logger.info('Start requests')
                
        yield scrapy.Request(self.baseUrl, callback=self.getBidang)

    
    def getBidang(self, response):
        self.logger.info('Get bidang')
        
        for row in response.css('div.paragraf-intro > ul > li'):
            #self.logger.info(row.css('li > a::attr(href)').extract())
            bidangBisnis = row.css('a::text').get()
            nextUrl = row.css('a::attr(href)').get()

            yield response.follow(nextUrl, self.getPageNum, meta = {'bidangBisnis': bidangBisnis, 'parentUrl': nextUrl})

    
    def getPageNum(self, response):
        self.logger.info('Get page number')

        pagination = response.css('ul.pagination > li > a::text').extract()

        for i in range(1, int(pagination[-2])+1):
            targetUrl = response.meta['parentUrl'] + '/page/' + str(i)
            #self.logger.info(targetUrl)
            yield scrapy.Request(targetUrl, callback=self.parseClient, meta = {'bidangBisnis': response.meta['bidangBisnis'], 'pageUrl': targetUrl})

    
    def parseClient(self, response):
        self.logger.info('Parse client')

        for res in response.css('div.home-list-pop'):
            loader = ItemLoader(item = YellowpagesItem(), selector = res)
            loader.add_value('bidang', response.meta['bidangBisnis'])
            #self.logger.info(res)

            loader.add_value('pageUrl', response.meta['pageUrl'])

            # get business name
            loader.add_css('namaClient', 'div.col-md-5 > h4::text')
            #self.logger.info(res.css('div.col-md-5 > h4::text').get())

            # get address
            addrCat = res.css('div.col-md-5 > p::text').getall()
            loader.add_value('kategori', addrCat[0])
            loader.add_value('alamat', addrCat[1])
            loader.add_value('kota', addrCat[2])
            #self.logger.info(res.css('div.col-md-5 > p::text').extract())
            
            # get phone number
            phoneNum = res.css('div.row > ul > li::text').getall()
            loader.add_value('noTelp', phoneNum[1])
            #self.logger.info(res.css('div.row > ul > li::text').extract())
            
            # get email address            
            #emailSite = res.css('div.col-md-4 > div.row > ul').getall() 
            #self.logger.info(res.xpath('//*div[@class="col-md-4"]/div[@class="row"]/ul[1]//li//text()'))
            emailSite = res.css('div.col-md-4 > div.row > ul > li > a::attr(href)').extract()

            for row in emailSite:
                if 'mailto' in row:
                    loader.add_value('email', row)
                else:
                    loader.add_value('site', row)

            #self.logger.info(emailSite)
            
            yield loader.load_item()