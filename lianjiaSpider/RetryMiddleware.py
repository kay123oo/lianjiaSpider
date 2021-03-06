from datetime import time
import random

from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message

from lianjiaSpider.ipprocy.db.DataStore import sqlhelper


class Process_Proxies(RetryMiddleware):


    def process_response(self, request, response, spider):
        print("返回码：")
        print(response.status)
        if request.meta.get('dont_retry', False):
            return response
        if response.status in self.retry_http_codes:
            reason = response_status_message(response.status)
            # 删除代理
            print("重试中间件：")
            print(reason)
            self.delete_proxy(request.meta.get('proxy', False))
            return self._retry(request, reason, spider) or response
        return response

    def process_exception(self, request, exception, spider):
        if isinstance(exception, self.EXCEPTIONS_TO_RETRY) and not request.meta.get('dont_retry', False):
            # 删除该代理
            print("重试中间件：exception：")
            print(exception)
            self.delete_proxy(request.meta.get('proxy', False))
            return self._retry(request, exception, spider)


    def delete_proxy(self,proxy,res=None):
        proxy = str(proxy).split(':')
        ip = proxy[1].replace('//','')
        port = proxy[2]
        #if proxy :
            #result = sqlhelper.delete({'ip': ip, 'port': port})
            #print("成功删除代理"+result)


