import scrapy
from duanmoi.items import DuanmoiItem

class MysraperSpider(scrapy.Spider):
    name = "mysraper"
    allowed_domains = ["motchillwin.net"]
    start_urls = ["https://motchillwin.net"]
    def start_requests(self):
        for i in range(1, 36):  # Duyệt qua 35 trang
            url = f'https://motchillwin.net/danh-sach/phim-moi.html?page={i}'
            yield scrapy.Request(url=url, callback=self.parse)
            yield scrapy.Request(url='https://motchillwin.net/danh-sach/phim-moi.html?page=1', callback=self.parse)
      
    def parse(self, response):
        courseList = response.xpath('//html/body/main/descendant::div/div/section/div/div/article/a/@href').getall()
        for courseItem in courseList:
            item = DuanmoiItem()
            item['courseUrl'] = response.urljoin(courseItem)
            request = scrapy.Request(url = response.urljoin(courseItem), callback=self.parseCourseDetailPage)
            request.meta['datacourse'] = item
            yield request
            
    def parseCourseDetailPage(self, response):
        item = response.meta['datacourse']
        item['coursename'] = response.xpath('normalize-space(string(//html/body/main/div[3]/div/div/section[1]/div[1]/div/div[1]/div[2]/h1))').get()
        item['trangthai'] = response.xpath('normalize-space(string(//html/body/main/div[3]/div/div/section[1]/div[1]/div/div[1]/div[2]/div/div/dl/div[1]/dd/span))').get()
        item['daodien'] = response.xpath('normalize-space(string(//html/body/main/div[3]/div/div/section[1]/div[1]/div/div[1]/div[2]/div/div/dl/div[2]/dd))').get()
        item['thoiluong'] = response.xpath('normalize-space(string(//html/body/main/div[3]/div/div/section[1]/div[1]/div/div[1]/div[2]/div/div/dl/div[3]/dd))').get()

        item['sotap'] = response.xpath('normalize-space(string(//html/body/main/div[3]/div/div/section[1]/div[1]/div/div[1]/div[2]/div/div/dl/div[4]/dd))').get()
        item['ngonngu'] = response.xpath('normalize-space(string(//html/body/main/div[3]/div/div/section[1]/div[1]/div/div[1]/div[2]/div/div/dl/div[5]/dd))').get()
        item['namsx'] = response.xpath('normalize-space(string(//html/body/main/div[3]/div/div/section[1]/div[1]/div/div[1]/div[2]/div/div/dl/div[6]/dd))').get()

        item['quocgia'] = response.xpath('normalize-space(string(//html/body/main/div[3]/div/div/section[1]/div[1]/div/div[1]/div[2]/div/div/dl/div[7]/dd))').get()
        item['theloai'] = response.xpath('normalize-space(string(//html/body/main/div[3]/div/div/section[1]/div[1]/div/div[1]/div[2]/div/div/dl/div[8]/dd/span))').get()
        item['mota'] = response.xpath('normalize-space(string(//html/body/main/div[3]/div/div/section[1]/div[1]/div/div[5]/div[1]/p))').get()
        
        
       
        yield item
