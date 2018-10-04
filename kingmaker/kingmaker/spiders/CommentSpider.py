# -*- coding: utf-8 -*-
import scrapy


class CommentSpider(scrapy.Spider):
    name = "CommentSpider"
    allowed_domains = ["kickstarter.com"]

    def __init__(self, project_url=None, *args, **kwargs):
        super(CommentSpider, self).__init__(*args, **kwargs)
        self.start_urls = [project_url]

    def parse(self, response):
        pass
