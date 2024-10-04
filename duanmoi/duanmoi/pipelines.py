# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
import pymongo
import json
# from bson.objectid import ObjectId
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import csv
import os
# useful for handling different item types with a single interface

class MongoDBDuanmoiPipeline:
    def __init__(self):
        # Sử dụng giá trị mặc định nếu 'Mongo_HOST' không được thiết lập
        self.connect_uri = os.environ.get('Mongo_HOST', 'mongodb://localhost:27017')  # Sử dụng biến môi trường nếu có
        # Tạo kết nối tới MongoDB
        self.client = pymongo.MongoClient(self.connect_uri)
        self.db = self.client['dbduanmoi']  # Tạo Database
        pass
    
    def process_item(self, item, spider):
        collection = self.db['tbmotchill']  # Tạo Collection hoặc Table
        try:
            collection.insert_one(dict(item))
            return item
        except Exception as e:
            raise DropItem(f"Error inserting item: {e}")       
        pass

class DuanmoiPipeline:
    def process_item(self, item, spider):
        with open('duanmoi.json', 'a', encoding='utf-8') as file:
            line = json.dumps(dict(item), ensure_ascii=False) + '\n'
            file.write(line)
        return item
class CSVDBDuanmoiPipeline:
    '''
    mỗi thông tin cách nhau với dấu $
    Ví dụ: coursename$lecturer$intro$describe$courseUrl
    Sau đó, cài đặt cấu hình để ưu tiên Pipline này đầu tiên
    '''
    def process_item(self, item, spider):
        with open('csvduanmoi.csv', 'a', encoding='utf-8', newline='') as file:
            writer = csv.writer(file, delimiter='$')
            writer.writerow([
                item['coursename'],
                item['trangthai'],
                item['daodien'],
                item['thoiluong'],
                item['sotap'],
                item['ngonngu'],
                item['namsx'],
                item['quocgia'],
                item['theloai'],
                item['mota'],
                item['courseUrl']
            ])
        return item
    pass