# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from collections import defaultdict
from scrapy import signals
from scrapy.exporters import JsonItemExporter, CsvItemExporter, JsonLinesItemExporter
from datetime import datetime
import pandas as pd
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import os


class VestiairePipeline(object):
	def __init__(self):
		self.files = defaultdict(list)

	@classmethod
	def from_crawler(cls, crawler):
		 pipeline = cls()
		 crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
		 crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
		 return pipeline

	def spider_opened(self, spider):
		self.date = datetime.utcnow().strftime("%Y-%m-%d")

		self.csv_file = open(self.date + '_vestiaire.csv', 'a+b')
		# self.json_file = open(self.date + '_vestiaire.json', 'w+b')
		self.jsonline_file = open(self.date + '_vestiaire.jl', 'a+b')

		self.files[spider].append(self.csv_file)
		self.files[spider].append(self.jsonline_file)

		# self.exporters = [
		# 	JsonItemExporter(json_file),
		# 	CsvItemExporter(csv_file)
		# ]

		# for exporter in self.exporters:
		# 	exporter.start_exporting()
		# self.json_exporter = JsonItemExporter(self.json_file, indent=1, ensure_ascii=False, encoding='utf-8')
		# self.json_exporter.start_exporting()
		
		self.jsonline_exporter = JsonLinesItemExporter(self.jsonline_file, indent=1, ensure_ascii=False, encoding='utf-8')
		self.jsonline_exporter.start_exporting()

		self.csv_exporter = CsvItemExporter(self.csv_file, encoding='utf-8')
		self.csv_exporter.fields_to_export = ['category', 'gender', 'itemId', 'name', 'brand', 'subCategory', 'price',
											  'finalPrice', 'estimatedRetailPrice', 'currency', 'qualityCost', 'fetchDate',
											  'model', 'color', 'material', 'style', 'condition', 'onlineSince', 'inclusions',
											  'height', 'width', 'depth', 'url', 'description', 'images']
		# CsvItemExporter(self.csv_file).start_exporting()
		self.csv_exporter.start_exporting()

	def spider_closed(self, spider):
		# for exporter in self.exporters:
		# 	exporter.finish_exporting()
		# JsonItemExporter(self.json_file).finish_exporting()
		self.jsonline_exporter.finish_exporting()
		# JsonLinesItemExporter(self.json_file, ensure_ascii=False, encoding='utf-8').finish_exporting()
		# CsvItemExporter(self.csv_file).finish_exporting()
		self.csv_exporter.finish_exporting()

		files = self.files.pop(spider)
		for file in files:
			file.close()

		date_time = datetime.utcnow().strftime("%Y-%m-%d_%H%M%S")
		# new_file_name_csv = date_time + '_vestiaire.csv'
		# new_file_name_jsonline = date_time + '_vestiaire.jl'

		# old_file_csv = '/home/divya/Documents/vestiaire/' + self.date + '_vestiaire.csv'
		# old_file_jl = '/home/divya/Documents/vestiaire/' + self.date + '_vestiaire.jl'

		# new_file_csv = '/home/divya/Documents/vestiaire/' + date_time + '_vestiaire.csv'
		# new_file_jl = '/home/divya/Documents/vestiaire/' + date_time + '_vestiaire.jl'

		# os.rename(old_file_csv, new_file_csv)
		# os.rename(old_file_jl, new_file_jl)

	def process_item(self, item, spider):
		# item_list = []
		# for exporter in self.exporters:
		currency = item.get('currency')
		category = item.get('category')
		if currency and currency == 'EUR' and category != None:
			item['currency'] = '€'
			# exporter.export_item(item)
			# JsonItemExporter(self.json_file).export_item(item)
			self.jsonline_exporter.export_item(item)
			# JsonLinesItemExporter(self.json_file, ensure_ascii=False, encoding='utf-8').export_item(item)
			# item_list.append(item.get('output'))
			# CsvItemExporter(self.csv_file).export_item(item['output'])
			self.csv_exporter.export_item(item)
		return item
