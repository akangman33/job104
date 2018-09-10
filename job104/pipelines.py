# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
# import pymongo
#
# class Job104Pipeline(object):
#
#     def open_spider(self, spider):
#         self.client = pymongo.MongoClient('localhost', 27017)
#         scrapy_db = self.client['scrapy_db']
#         self.coll = scrapy_db['job_scrapy']
#
#
#     def process_item(self, item, spider):
#         self.coll.insert_one(item)
#         return item
#
#     def close_spider(self, spider):
#         self.client.close()

import pymysql

class Job104Pipeline(object):

    def open_spider(self, spider):
        self.db = pymysql.connect("localhost","root","123456789","job104")
        self.cur = self.db.cursor()
        create_table = "create table job_scrapy(id int(10) not null, job_name varchar(300), company varchar(300), salary varchar(300)," \
                       "address varchar(300),job_url varchar(300))"
        self.cur.execute(create_table)
        self.db.commit()

    def process_item(self, item, spider):
        insert_sql = "insert into job_scrapy(id, job_name, company, salary, address, job_url) \
                     values('{}', '{}', '{}', '{}', '{}', '{}')".format(item['id'], item['job_name'], item['company'], item['salary'], item['address'], item['job_url'])
        self.cur.execute(insert_sql)
        self.db.commit()
        # return item

    def close_spider(self, spider):
        self.db.close()