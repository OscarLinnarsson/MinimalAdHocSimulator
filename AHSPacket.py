
# pType = 0     - GET REQUEST
# pType = 1     - POST data to server
# pType = 2     - RESPONCE, from server or node with requested data

class packet:

    def __init__(self, pType, ttl, serverX, serverY, fromX, fromY, toX, toY, dirX, dirY, data, fromServer):
        self.pType = pType
        self.ttl = ttl
        self.fromServerX = serverX
        self.fromServerY = serverY
        self.fromNodeX = fromX
        self.fromNodeY = fromY
        self.toX = toX
        self.toY = toY
        self.dirX = dirX
        self.dirY = dirY
        self.data = data
        self.fromServer = fromServer
        self.nodeHops = 0

