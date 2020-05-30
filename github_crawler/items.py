# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RepoItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    full_name = scrapy.Field()
    html_url = scrapy.Field()
    description = scrapy.Field()
    git_url = scrapy.Field()
    ssh_url = scrapy.Field()
    stars = scrapy.Field()
    forks = scrapy.Field()
    watchers = scrapy.Field()
    language = scrapy.Field()
    created_at = scrapy.Field()
    updated_at = scrapy.Field()
    pushed_at = scrapy.Field()
