# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
#-*- coding:utf-8 -*-
import scrapy


class StackoverflowItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    links = scrapy.Field()
    views = scrapy.Field()
    votes = scrapy.Field()
    answers = scrapy.Field()
    tags = scrapy.Field()
    questions = scrapy.Field()

class SoCommentItem(scrapy.Item):
    question_header = scrapy.Field()
    comments = scrapy.Field()
    comment_user = scrapy.Field()
    comment_date = scrapy.Field()
    comment_vote = scrapy.Field()