# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from openpyxl import Workbook
import json
from StackOverflow.items import SoCommentItem, StackoverflowItem
class StackoverflowPipeline:
    def __init__(self):
        self.wb = Workbook()
        self.ws = self.wb.active
        self.wbc = Workbook()
        self.wsc = self.wbc.active
        self.ws.append(['questions', 'answers', 'votes', 'views', 'links', 'tags'])
        self.wsc.append(['question_header', 'users', 'comments', 'votes', 'date'])
        # self.f = open("D:/StackOverflow/StackOverflow/Data/"+"soc.json", "w", encoding="utf-8")
    def process_item(self, item, spider):
        if isinstance(item, StackoverflowItem):
            line = [item['questions'][0], item['answers'][0], item['votes'][0], item['views'][0], item['links'], item['tags']]
            self.ws.append(line)
            self.wb.save("./StackOverflow/Data/" + 'so.xlsx')
        # linec = [item['question_header'][0], item['comment_user'][0], item['comments'], item['comment_vote'][0], item['comment_date'][0]]
        # self.wsc.append(linec)
        # self.wbc.save("H:/StackOverflow/StackOverflow/Data/" + 'so_comment.xlsx')
        if isinstance(item, SoCommentItem):
            linec = [item['question_header'][0], item['comment_user'][0], item['comments'], item['comment_vote'][0], item['comment_date'][0]]
            self.wsc.append(linec)
            self.wbc.save("./StackOverflow/Data/" + 'so_comment.xlsx')
        return item

    def close_spider(self, spider):
        self.ws.close()
        self.wsc.close()
        pass