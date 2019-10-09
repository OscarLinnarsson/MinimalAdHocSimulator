
# dType = 0     - TREND UPDATE TO SERVER
# dType = 1     - GET REQUEST

class data:

    def __init__(self, dType, ttl, content, trendVal, cacheInterval):
        self.dType = dType
        self.ttl = ttl
        self.content = content
        self.trendVal = trendVal
        self.cacheInterval = cacheInterval
        if self.cacheInterval <= 0:
            self.cacheInterval = 13
