# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import re
from datetime import date
from time import sleep
from datetime import datetime
from vestiaire.items import VestiaireItem
import json


class VestiaireSpider(scrapy.Spider):
	name = 'Vestiaire_collec'
	allowed_domains = ['www.vestiairecollective.com']
	# start_urls = ['https://www.vestiairecollective.com/']

	def __init__(self, category=None, **kwargs):
		self.category = category

	def start_requests(self):
		# meta = {'proxy': 'http://127.0.0.1:1080'}
		category = self.category.lower()
		url = None
		if category == 'men':
			url = 'https://www.vestiairecollective.com/men-bags/'
		elif category == 'women':
			url = 'https://www.vestiairecollective.com/women-bags'
		else:
			print '-----------Category Is Not Defined---------------'
		# # url = 'https://www.vestiairecollective.com/women-bags/handbags/mulberry/brown-leather-bayswater-tote-mulberry-handbag-20338606.shtml'
		# url = 'https://www.vestiairecollective.com/women-bags/handbags/vivienne-westwood/brown-alligator-derby-vivienne-westwood-handbag-20383916.shtml'

		yield Request(url=url, callback=self.parse) 

	def parse(self, response):
		for i in range(1,22):
			page_url = None
			if self.category.lower() == 'men':
				page_url = 'https://www.vestiairecollective.com/men-bags/p-' + str(i)
			else:
				page_url = 'https://www.vestiairecollective.com/women-bags/p-' + str(i)
			yield Request(url=page_url, callback=self.listing_urls, dont_filter=True, priority=(100-i)*100)

	def listing_urls(self, response):
		product_urls = response.xpath('//vc-ref[@class="productSnippet__imageContainer"]/a/@href').extract()
		print '-----------------------',len(product_urls)
		for urls in product_urls:
			urls = 'https://www.vestiairecollective.com' + urls if 'https://www.vestiairecollective.com' not in urls else urls
			yield Request(url=urls, callback=self.product_details, dont_filter=True)

	def product_details(sel, response):
		name = response.xpath('//div[@class="productTitle__name"]/text()').extract_first() or \
			   response.xpath('//div[@class="product-main-heading_productTitle__name__x_rnE"]/text()').extract_first()
		name = name.strip() if name else None

		brand = response.xpath('//div[@class="vc-title-l productTitle__brand"]/vc-ref/a/text()').extract_first() or \
				response.xpath('//a[@class="product-main-heading_productTitle__brand__link__lBDOQ"]/text()').extract_first()
		brand = brand.strip() if brand else None

		title = brand + ' ' + name if name and brand else None

		details_path = response.xpath('//ul[@class="descriptionList__block__list descriptionList__block__list--detail"]') or \
					   response.xpath('//div[@class="product-description-list_descriptionList__column__SjoIE product-description-list_descriptionList__column--left__EwwnT"]/div/ul')

		# product_id = details_path.xpath('.//li[contains(text(),"Reference:")]/text()').extract_first()
		# product_id = re.findall(r'Reference: (.*)',product_id) if product_id else None
		# product_id = product_id[0].strip() if product_id else None
		product_id = details_path.xpath('//li/span[contains(text(),"Reference:")]/following-sibling::span[1]/text()').extract_first()
		product_id = product_id.strip() if product_id else None

		# model = details_path.xpath('.//li[contains(text(),"Model:")]/text()').extract_first()
		# model = re.findall(r'Model: (.*)',model) if model else None
		# model = model[0].strip() if model else None
		model = details_path.xpath('//li/span[contains(text(),"Model:")]/following-sibling::span[1]/text()').extract_first()
		model = model.strip() if model else None

		# conditions = details_path.xpath('.//li/span[contains(text(),"Condition:")]/text()').extract_first()
		# conditions = re.findall(r'Condition: (.*)',conditions) if conditions else None
		# conditions = conditions[0].strip() if conditions else None
		conditions = details_path.xpath('//li/span[contains(text(),"Condition:")]/following-sibling::span[1]/text()').extract_first()
		conditions = conditions.strip() if conditions else None

		# category = details_path.xpath('.//li[contains(text(),"Category:")]/text()').extract_first()
		# category = re.findall(r'Category: (.*)',category) if category else None
		# category = category[0].strip() if category else None
		category = details_path.xpath('//li/span[contains(text(),"Category:")]/following-sibling::span[1]/text()').extract_first()
		category = category.strip() if category else None

		# color = details_path.xpath('.//li[contains(text(),"Colour:")]/text()').extract_first()
		# color = re.findall(r'Colour: (.*)',color) if color else None
		# color = color[0].strip() if color else None
		color = details_path.xpath('//li/span[contains(text(),"Colour:")]/following-sibling::span[1]/text()').extract_first()
		color = color.strip() if color else None

		# material = details_path.xpath('.//li[contains(text(),"Material:")]/text()').extract_first()
		# material = re.findall(r'Material: (.*)',material) if material else None
		# material = material[0].strip() if material else None

		# material = details_path.xpath('.//li/span[contains(text(),"Material:")]/following-sibling::span[1]/text()').extract_first()
		# material = material.strip() if material else None
		json_txt = response.xpath('//script[@id="__NEXT_DATA__"]/text()').extract_first()

		json_data = json.loads(json_txt)

		req_dict = json_data['props']['pageProps']['product']['material']
		material_dict = req_dict.get('parent')
		material = material_dict.get('name') if material_dict else req_dict.get('name')
		material = material.strip() if material else None

		# gender = details_path.xpath('.//li[contains(text(),"Categories")]/text()').extract_first()
		# gender = re.findall(r'Categories :(.*)',gender) if gender else None
		# gender = gender[0].strip() if gender else None
		gender = details_path.xpath('.//li/span[contains(text(),"Categories :")]/following-sibling::span[1]/text()').extract_first()
		gender = gender.strip() if gender else None 

		# online_since = details_path.xpath('.//li[contains(text(),"Online since:")]/text()').extract_first()
		# online_since = re.findall(r'Online since: (.*)',online_since) if online_since else None
		# online_since = online_since[0].strip() if online_since else None
		online_since = details_path.xpath('.//li/span[contains(text(),"Online since:")]/following-sibling::span[1]/text()').extract_first()
		online_since = online_since.strip() if online_since else None

		# sub_category = details_path.xpath('.//li[contains(text(),"Sub-category:")]/text()').extract_first()
		# sub_category = re.findall(r'Sub-category: (.*)',sub_category) if sub_category else None
		# sub_category = sub_category[0].strip() if sub_category else None
		sub_category = details_path.xpath('.//li/span[contains(text(),"Sub-category:")]/following-sibling::span[1]/text()').extract_first()
		sub_category = sub_category.strip() if sub_category else None

		# style = details_path.xpath('.//li[contains(text(),"Style:")]/text()').extract_first()
		# style = re.findall(r'Style:(.*)',style) if style else None
		# style = style[0].strip() if style else None
		style = details_path.xpath('.//li/span[contains(text(),"Style:")]/following-sibling::span[1]/text()').extract_first()
		style = style.strip() if style else None

		# size = 

		width = None
		height = None
		depth = None
		# measuremet = response.xpath('//div[@class="descriptionList__block descriptionList__block--dimensions"]/ul/li/text()').extract()
		# for value in measuremet:
		# 	if 'WIDTH' in value.upper():
		# 		width = value.strip().replace('Width: ','')
		# 	elif 'HEIGHT' in value.upper():
		# 		height = value.strip().replace('Height: ','')
		# 	elif 'DEPTH' in value.upper():
		# 		depth = value.strip().replace('Depth: ','')
		width = response.xpath('//div[@class="product-description-list_descriptionList__column__SjoIE product-description-list_descriptionList__column--right__h5uu_"]/div/ul/li/span[contains(text(),"Width")]/following-sibling::span[1]/text()').extract()
		width = ''.join(width).strip().replace(' ','') if width else None

		height = response.xpath('//div[@class="product-description-list_descriptionList__column__SjoIE product-description-list_descriptionList__column--right__h5uu_"]/div/ul/li/span[contains(text(),"Height")]/following-sibling::span[1]/text()').extract()
		height = ''.join(height).strip().replace(' ','') if height else None

		depth = response.xpath('//div[@class="product-description-list_descriptionList__column__SjoIE product-description-list_descriptionList__column--right__h5uu_"]/div/ul/li/span[contains(text(),"Depth")]/following-sibling::span[1]/text()').extract()
		depth = ''.join(depth).strip().replace(' ','') if depth else None
		# measures = response.xpath('//div[@class="descriptionList__block descriptionList__block--dimensions"]/ul/li/text()').extract()
		# measures = ', '.join(measures) if measures else None

		# currency = response.xpath('//span[@itemprop="priceCurrency"]/@content').extract_first()
		# if not currency:
		# 	currency = re.findall(r'priceCurrency": (.*)',response.body)
		# 	currency = currency[0].replace('"','').replace(',','') if currency else None
		# currency = currency.strip() if currency else None
		currency = response.xpath('//span[@class="product-price_productPrice__price--promo__Cxs_S"]').extract_first() or \
				   response.xpath('//div[@class="product-price_productPrice__Uq0dh"]/p/span/text()').extract_first()
		currency = "EUR" if currency and '€' in currency else None
		# if currency == 'EUR':
		# 	currency = '€'
		# elif currency == 'GBP':
		# 	currency = '£'
		# elif currency == 'USD':
		# 	currency = '$'

		final_price = response.xpath('//span[@class="productPrice__price"]/text()').re_first(r'[\d\s*\.*,*]+') or \
					  response.xpath('//span[@class="productPrice__price productPrice__price--promo"]/text()').re_first(r'[\d\s*\.*,*]+') or \
					  response.xpath('//span[@class="product-price_productPrice__price--promo__Cxs_S"]/text()').re_first(r'[\d\s*\.*,*]+') or \
					  response.xpath('//div[@class="product-price_productPrice__Uq0dh"]/p/span/text()').re_first(r'[\d\s*\.*,*]+')
		final_price = final_price.strip().replace(',','.') if final_price and currency=='EUR' else final_price

		price_before_discount = response.xpath('//span[@class="productPrice__price productPrice__price--strikeOut"]/text()').re_first(r'[\d\s*\.*,*]+') or \
								response.xpath('//span[@class="undefined product-price_productPrice__price--strikeOut__t2OBQ"]/text()').re_first(r'[\d\s*\.*,*]+')
		price_before_discount = price_before_discount.strip().replace(',','.') if price_before_discount and currency=='EUR' else price_before_discount
		price_before_discount = price_before_discount if price_before_discount else final_price

		# currency = response.xpath('//span[@itemprop="priceCurrency"]/@content').extract_first()
		# if not currency:
		# 	currency = re.findall(r'priceCurrency": (.*)',response.body)
		# 	currency = currency[0].replace('"','').replace(',','') if currency else None
		# currency = currency.strip() if currency else None

		# date_time = date.today()
		date_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

		# images = response.xpath('//img[@width="500"]/@src').extract()
		images = response.xpath('//div[@class="swiper-slide slider_image__wrapper__LLX1C"]/img/@data-src').extract()
		# all_images = '; '.join(images) if images else None
		# all_images = list(all_images) if all_images else None

		# product_main_image = images[0] if images else None

		description = response.xpath('//div[@class="sellerDescription"]/p/text()').extract_first() or \
					  response.xpath('//div[@class="product-seller-description_sellerDescription__SnSkU"]/p/text()').extract_first()
		description = description.replace('\n','').replace('  ','').replace('\t','').replace(';','').strip().encode('utf-8') if description else None

		quality_cost = response.xpath('//p[@class="productPrice__buyerFees vc-body3"]/text()').re_first(r'[\d\s*\.*,*]+') or \
					   response.xpath('//p[@class="product-price_productPrice__buyerFees__PdoBB vc-body3"]/text()').re_first(r'[\d\s*\.*,*]+')
		quality_cost = quality_cost.strip().replace(',','.') if quality_cost and currency=='EUR' else quality_cost

		sold_with = response.xpath('//div[@class="descriptionList__block descriptionList__block--packaging"]/ul/li/text()').extract() or \
					response.xpath('//h3[contains(text(),"Sold with")]/following-sibling::ul/li/span/text()').extract()
		sold_with = ', '.join(sold_with) if sold_with else None

		# import pdb;pdb.set_trace()

		sold_products = response.xpath('//span[@class="productPrice__sold"]/text()').extract_first() or \
						response.xpath('//span[@class="product-price_productPrice__sold__OeDQf"]/text()').extract_first()
		# client doesn't want sold products.
		if not sold_products:
			item = VestiaireItem()

			item['itemId'] = product_id
			item['url'] = response.url
			item['name'] = title
			item['brand'] = brand
			item['estimatedRetailPrice'] = None
			item['price'] = price_before_discount
			item['finalPrice'] = final_price
			# item['fetchDate'] = date_time.isoformat()
			item['fetchDate'] = date_time
			item['currency'] = currency
			item['model'] = model
			item['condition'] = conditions
			item['category'] = category
			item['gender'] = gender
			item['color'] = color
			item['material'] = material
			# item['measures'] = measures
			item['height'] = height
			item['width'] = width
			item['depth'] = depth
			# item['imageUrl'] = product_main_image
			item['images'] = images
			item['description'] = description
			item['onlineSince'] = online_since
			item['subCategory'] = sub_category
			item['style'] = style
			item['qualityCost'] = quality_cost
			item['inclusions'] = sold_with

			# item = VestiaireItem()
			# item['output'] = output # populates item by extracted data.

			yield item
		else:
			pass
		





