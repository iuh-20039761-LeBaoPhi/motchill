import scrapy
from duanmoi.items import DuanmoiItem

class MysraperSpider(scrapy.Spider):
    name = "mysraper"
    allowed_domains = ["motchilliu.net"]
    start_urls = ["https://motchilliu.net/"]
    def start_requests(self):
        for i in range(1, 35):  # Duyệt qua 35 trang
            url = f'https://motchilliu.net/danh-sach/phim-moi.html?page={i}'
            yield scrapy.Request(url=url, callback=self.parse)
            yield scrapy.Request(url='https://motchilliu.net/danh-sach/phim-moi.html?page=', callback=self.parse)
      
    def parse(self, response):
        courseList = response.xpath('//html/body/div/descendant::div/div/div/div/div/a/@href').getall()
        for courseItem in courseList:
            item = DuanmoiItem()
            item['courseUrl'] = response.urljoin(courseItem)
            request = scrapy.Request(url = response.urljoin(courseItem), callback=self.parseCourseDetailPage)
            request.meta['datacourse'] = item
            yield request
            
    def parseCourseDetailPage(self, response):
        item = response.meta['datacourse']
        item['coursename'] = response.xpath('normalize-space(string(//h1/span/a))').get()
        item['trangthai'] = response.xpath('normalize-space(string(//dt[contains(text(), "Trạng thái")]/following-sibling::dd))').get()
        item['daodien'] = response.xpath('normalize-space(string(//dt[contains(text(), "Đạo diễn")]/following-sibling::dd))').get()
        item['thoiluong'] = response.xpath('normalize-space(string(//dt[contains(text(), "Thời lượng")]/following-sibling::dd))').get()

        item['ngonngu'] = response.xpath('normalize-space(string(//dt[contains(text(), "Ngôn ngữ")]/following-sibling::dd))').get()
        item['namsx'] = response.xpath('normalize-space(string(//dt[contains(text(), "Năm")]/following-sibling::dd))').get()
        item['quocgia'] = response.xpath('normalize-space(string(//dt[contains(text(), "Quốc gia")]/following-sibling::dd))').get()
        item['theloai'] = response.xpath('normalize-space(string(//dt[contains(text(), "Thể loại")]/following-sibling::dd))').get()
        item['mota'] = response.xpath('normalize-space(string(//article//div/div/text() | //article//div/div/p/text()))').get()

        # Cào thêm các thuộc tính mới
        item['danhgia'] = response.xpath('normalize-space(string(//p[@class="text-xs text-white align-middle"]))').get()
        item['chatluong'] = response.xpath('normalize-space(string(//dt[contains(text(), "Chất lượng")]/following-sibling::dd))').get()
        item['luotxem'] = response.xpath('normalize-space(string(//dt[contains(text(), "Lượt xem")]/following-sibling::dd))').get()
        yield item
