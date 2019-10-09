

class cacheFile:

    def __init__(self, data, serverX, serverY):
        self.data = data
        self.serverX = serverX
        self.serverY = serverY
        self.numReq = 0
        self.numTimeSteps = 0
        self.hasUpdated = False