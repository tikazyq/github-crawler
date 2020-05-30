# -*- coding: utf-8 -*-
import json
import os
import re

import scrapy

from github_crawler.items import RepoItem


class GithubSpider(scrapy.Spider):
    name = 'github'
    allowed_domains = ['github.com']

    def __init__(self, keyword='crawler', *args, **kwargs):
        super(GithubSpider, self).__init__(*args, **kwargs)
        self.start_urls = [f'https://api.github.com/search/repositories?q={keyword}']

    @staticmethod
    def get_next_link_url(response):
        link = response.headers.get('Link').decode('utf-8')
        m = re.search('<(.*)>; rel="next"', link)
        if m is not None:
            return m.group(1)
        return None

    def parse(self, response):
        data = json.loads(response.body)
        for d in data.get('items'):
            yield RepoItem(
                id=d.get('id'),
                name=d.get('name'),
                full_name=d.get('full_name'),
                html_url=d.get('html_url'),
                description=d.get('description'),
                git_url=d.get('git_url'),
                ssh_url=d.get('ssh_url'),
                created_at=d.get('created_at'),
                updated_at=d.get('updated_at'),
                pushed_at=d.get('pushed_at'),
            )

        next_url = self.get_next_link_url(response)
        yield scrapy.Request(url=next_url, callback=self.parse)
