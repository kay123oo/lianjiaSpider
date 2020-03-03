import random
from lianjiaSpider.ipprocy.db.DataStore import sqlhelper

class ProxyMiddleware():
    global count
    count = 1
    global ips
    ips = []

    def process_request(self, request, spider):
        # Set the location of the proxy
        global count
        global ips
        if count == 1:
            ips = sqlhelper.selectIps()
        elif count%100 == 0:
            ips = []
            ips = sqlhelper.selectIps()
        else:
            pass
        try:
            num = random.randint(0, len(ips))
            if ips[num][2] == 1:
                ress = 'https://' + ips[num][0] +":"+ ips[num][1]
            else:
                ress = 'http://' + ips[num][0] +":"+ ips[num][1]
        except BaseException as e:
            print(e)
            pass
        else:
            request.meta['proxy'] = str(ress)
            count += 1
