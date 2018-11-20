#!/usr/bin/env python
# encoding: utf-8
'''
@author: AnthonyZero
@file: custom_scrapy.py
@time: 2018/11/20 10:46
@desc: 自定义简单scrapy框架
'''

import types
from twisted.internet import defer    #特殊的socket对象（不会发请求 手动移除）
from twisted.web.client import getPage #socket对象
from twisted.internet import reactor  #事件循环
import queue


class Request(object):

    def __init__(self, url, callback):
        self.url = url
        self.callback = callback

class Response(object):

    def __init__(self, body, request):
        self.body = body
        self.request = request
        self.url = request.url

    @property
    def text(self):
        return self.body.decode('utf-8')

# 自己的业务爬虫
class BaiduSpider(object):
     name = "baidu"
     start_url = ["http://www.baidu.com", "http://news.baidu.com/"]
     def start_request(self):
         for url in self.start_url:
            yield Request(url, self.parse)

     def parse(self, response):
         print(response, response.url)
         # yield Request("http://www.baidu.com", self.parse)

# 请求队列
queue = queue.Queue()

class Engine(object):
    def __init__(self):
        self._close = None
        self._max_currentcy = 5
        self._crawling = [] # 正在进行调度的请求

    def get_reponse_callback(self, content, request):
        self._crawling.remove(request)
        response = Response(content, request)
        result = request.callback(response)
        if isinstance(result, types.GeneratorType):
            for req in result:
                queue.put(req) # yield的请求又继续放入队列

    def next_request(self):
        if queue.qsize() == 0 and len(self._crawling) == 0: # 所有调度都完成
            self._close.callback(None)
            return

        if len(self._crawling) >= self._max_currentcy:
            return
        while len(self._crawling) < self._max_currentcy:
            try:
                request = queue.get(block = False)
                self._crawling.append(request)
                d_defer = getPage(request.url.encode('utf-8'))
                # 页面下载完成 get_reponse_callback 调用用户spider中自定义的parse方法 并且将新请求加入到调度器
                d_defer.addCallback(self.get_reponse_callback, request)

                d_defer.addCallback(lambda _:reactor.callLater(0, self.next_request))
            except Exception as e:
                return

    @defer.inlineCallbacks
    def crawl(self, spider): # 开始调度爬虫
        # Download
        start_quest = iter(spider.start_request())
        while True:
            try:
                queue.put(next(start_quest)) # 往队列中放入request对象
            except StopIteration as ex:
                break
        # 去调度器取request 发起请求
        reactor.callLater(0, self.next_request)
        self._close = defer.Deferred()
        yield self._close

_active = set()
engine = Engine()
spider = BaiduSpider()
d = engine.crawl(spider)
_active.add(d)
defer_list = defer.DeferredList(_active)

defer_list.addBoth(lambda a: reactor.stop())
reactor.run()