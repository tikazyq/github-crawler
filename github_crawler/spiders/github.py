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
        self.keyword = keyword
        self.langs = ['python', 'javascript']
        self.sorts = ['updated', 'best-match']

    def start_requests(self):
        for sort in self.sorts:
            url = f'https://api.github.com/search/repositories?q={self.keyword}&sort={sort}'
            for lang in self.langs:
                url = f'https://api.github.com/search/repositories?q={self.keyword}+language:{lang}&sort={sort}'
                yield scrapy.Request(url=url, callback=self.parse)

    def get_next_link_url(self, response):
        link = response.headers.get('Link').decode('utf-8')
        m = re.search(fr'<(https://api\.github\.com/search/repositories\?.+)>; rel="next"',
                      link)
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
                stars=d.get('stargazers_count'),
                forks=d.get('forks'),
                watchers=d.get('watchers_count'),
                language=d.get('language'),
                created_at=d.get('created_at'),
                updated_at=d.get('updated_at'),
                pushed_at=d.get('pushed_at'),
            )

        next_url = self.get_next_link_url(response)
        if next_url is not None:
            yield scrapy.Request(url=next_url, callback=self.parse)
