
# SUMULATED TREND ASKS FROM FILE WITH INDEX 0

# POLICY 1 
# Cache own requests, don't share a cached file with other peers

# POLICY 2
# Cache own requests, share cached files 
# with other peers

# POLICY 3
# Only cache files based on there trend value, share with other peers

# POLICY 4
# POLICY 2 + POLICY 3

# POLICY 5
# POLICY 4 + Considere a GET request fullfilled if the asked for file is in a relayed packet, remember to forward the packet


import AHSPacket
import AHSNodeLog
import AHSData
import AHSCacheFile
import AHSPendingReq
import toolbox as tb
import AHSSettings as settings

from random import randint
import math
import copy

policy = settings.policy
dataTTL = settings.dataTTL
packetTTL = settings.packetTTL
getReqContent = settings.avalibleFiles

ticksSinceStart = 0
weightNewTrendVal = 0.6
baseTime = 1000

def sortTrendValue(cacheItem):
    return cacheItem.data.trendVal

class node:

    def __init__(self, isServer, x, y, browsFreq, probFileX, cacheSize, cache):
        self.x = x
        self.y = y
        self.isServer = isServer

        self.browsFreq =  browsFreq
        self.probFileX = probFileX
        self.pendingRequests = []

        self.cacheSize = cacheSize
        self.cache = cache

        self.toForward = []
        self.freshPackets = []

        self.tickLog = AHSNodeLog.nodeTickLog()
        self.ticksLogArr = []

        self.simulateTrend = False

        self.requestFileForReal = []

    def startTrend(self, aFlag):
        self.simulateTrend = aFlag

    def sendTrendDataToServer(self, cacheItem):
        if cacheItem.hasUpdated:
            d = AHSData.data(0, 9999, cacheItem.data.content, cacheItem.data.trendVal, 0)
            newD = copy.deepcopy(d)
            p = AHSPacket.packet(1, 9999, cacheItem.serverX, cacheItem.serverY, self.x, self.y, cacheItem.serverX, cacheItem.serverY, 0, 0, newD, False)
            newP = copy.deepcopy(p)
            self.toForward.append(newP)
    
    def removeCacheItem(self, cacheItem):
        if cacheItem.data.ttl <= 0:
            if settings.policy >= 3:
                self.sendTrendDataToServer(cacheItem)
            return True
        else:
            return False

    def removePendingReq(self, pendingItem):
        if pendingItem.ttl < 0:
            self.tickLog.numStopWaiting += 1
            return True
        else:
            return False

    def setFileCacheIntensity(self):
        self.cache.sort(key = sortTrendValue)
        cInterval = 1
        for ci in self.cache:
            cInterval += 1
            ci.data.cacheInterval = cInterval

    def newTick(self):
        self.tickLog = AHSNodeLog.nodeTickLog()
        self.tickLog.currentCacheSize = len(self.cache)
        for ci in self.cache:
            #self.tickLog.currentCache.append(ci.data.content)
            self.tickLog.currentCache += ci.data.content
        self.requestFileForReal = []

        self.toForward = self.freshPackets
        self.freshPackets = []
        for p in self.toForward:
            p.ttl -= 1
        
        if self.isServer:
            self.setFileCacheIntensity()
            return 
        
        for c in self.cache:
            c.data.ttl -= 1
        if len(self.cache) > 0:
            self.cache = [c for c in self.cache if not self.removeCacheItem(c)]

        for p in self.pendingRequests:
            p.ttl -= 1
        if len(self.pendingRequests) > 0:
            self.pendingRequests = [p for p in self.pendingRequests if not self.removePendingReq(p)]            

        #
        #   WHILE TREND IS SIMULATED
        #
        if self.simulateTrend == True and randint(0, 99) < 25:
            self.getFile(0)
            
        #
        #   NORMAL OPPERATION
        #
        else:
            if randint(0, 99) < self.browsFreq:
                rand = randint(0, 99)
                for i in range(len(self.probFileX)):
                    if rand < self.probFileX[i]:
                        self.getFile(i)
                        break
        
    def getFile(self, reqFileI):
        # ADD REQUEST TO toForward
        self.tickLog.numOwnReq = 1
        if self.fileInCache(getReqContent[reqFileI]):
            self.tickLog.numRespFromCache += 1
            self.tickLog.numResponces += 1
            self.tickLog.numTicksBeforeResponce += 0
        else:
            newD = AHSData.data(1, 9999, getReqContent[reqFileI], 0, 0)
            self.pendingRequests.append(AHSPendingReq.pendingReq(newD.content, 2 * packetTTL + 2))
            pack = AHSPacket.packet(0, packetTTL, -1, -1, self.x, self.y, -1, -1, 0, 0, newD, self.isServer)
            self.toForward.append(pack)
    
    def endTick(self):
        # SAVE LOG DATA
        self.tickLog.numSentPackages += self.tickLog.numSentGET
        self.tickLog.numSentPackages += self.tickLog.numSentPOST
        self.tickLog.numSentPackages += self.tickLog.numSentRESPONCE
        self.ticksLogArr.append(self.tickLog)
        


    def fileInCache(self, content):
        for c in self.cache:
            if c.data.content == content:
                return True
        return False

    def incommingPacket(self, packet):
        p = copy.deepcopy(packet)
        if p.ttl <= 0 or p.data.ttl <= 0: # Drop packet
            return
        if p.pType == 0: # GET
            self.handleGet(p)
        elif p.pType == 1: # POST
            self.handlePost(p)
        elif p.pType == 2: # RESPONCE
            self.handleResponce(p)
        elif p.pType == 3: # RESPONCE WITH FILE
            self.handleResponceWithFile(p)
        
    def handleGet(self, packet): # A REQUEST FOR A FILE BY A CLIENT
        if self.isServer == True:
            for c in self.cache:
                if c.data.content == packet.data.content:
                   self.updateTrendData(packet)
                   self.serverProvideFile(packet, c)
                   return
        elif policy != 1:
            for c in self.cache:
                if c.data.content == packet.data.content:
                    self.provideFromCache(packet, c)
                    return
        self.forwardPacket(packet)
        
    def handlePost(self, packet): # CLIENT SENDS DATA TO SERVER (TREND DATA)
        if self.isServer == True:    
            if packet.toX == self.x and packet.toY == self.y:
                self.updateTrendData(packet)
            else:
                self.forwardPacket(packet)
        else:
            self.forwardPacket(packet)

    def sendFileForReal(self, packet):
        newP = copy.deepcopy(packet)
        newP.pType = 3
        self.freshPackets.append(newP)

    def handleResponceWithFile(self, packet):
        if packet.toX == self.x and packet.toY == self.y:
            self.fileReceivedWithFile(packet)
        else:
            self.forwardPacket(packet)
        if policy > 2:
            self.shouldICacheFile(packet)


    def handleResponce(self, packet): # RETURNED FILES FROM GET REQUESTS
        if packet.toX == self.x and packet.toY == self.y:
            isStillRequested = False
            tmpPending = 1
            for pending in self.pendingRequests:
                if packet.data.content == pending.content:
                    isStillRequested = True
                    tmpPending = pending
                    break
            if isStillRequested:
                self.pendingRequests.remove(tmpPending)
                self.fileReceived(packet, tmpPending)
                self.requestFileForReal.append(packet)
            
        else:
            self.forwardPacket(packet)

    def forwardPacket(self, packet):
        self.freshPackets.append(packet)




#################################
#       REGULAR NODE STUFF      #
#################################
    def provideFromCache(self, packet, cacheItem):
        cacheItem.hasUpdated = True
        self.updateFilesTrendData(cacheItem.data) # Only log update in trend value when a file is sent for real? NOT IMPLEMENTED!!!!
        p = AHSPacket.packet(2, 99999, cacheItem.serverX, cacheItem.serverY, self.x, self.y, packet.fromNodeX, packet.fromNodeY, 0, 0, cacheItem.data, False)
        newP = copy.deepcopy(p)
        self.freshPackets.append(newP)


    def updateCacheItemIfPrecent(self, packet):
        for i in range(len(self.cache)):
            if self.cache[i].data.content == packet.data.content:
                self.cache[i].data = copy.deepcopy(packet.data)
                return True
        return False

    def removeLeastTrendyToAddNew(self, packet):
        index = -1
        compTrendVal = (1/packet.data.cacheInterval) * math.sqrt(packet.data.ttl)
        for i in range(len(self.cache)):
            tmpCompTrendVal = (1/self.cache[i].data.cacheInterval) * math.sqrt(self.cache[i].data.ttl)
            if tmpCompTrendVal < compTrendVal:
                index = i
                compTrendVal = tmpCompTrendVal
        if index < 0:
            return False
        else:
            cacheItem = self.cache[index]
            self.cache.remove(cacheItem)
            return True


    # NODE HAS RECIEVED A REQUESTED FILE    
    # SELFISH CACHING TRUMPS TRENDBASED CACHING
    def fileReceivedWithFile(self, packet):
        newCacheItem = AHSCacheFile.cacheFile(packet.data, packet.fromServerX, packet.fromServerY)
        if policy < 3:
            if self.updateCacheItemIfPrecent(packet) == False:
                if len(self.cache) >= self.cacheSize:
                    tb.pr("REMOVE FROM CACHE")
                    self.cache.remove(self.cache[0])    
                self.cache.append(newCacheItem)
        elif policy > 3:
            if self.updateCacheItemIfPrecent(packet) == False:
                if len(self.cache) >= self.cacheSize:
                    if self.removeLeastTrendyToAddNew(packet):
                        self.cache.append(newCacheItem)
                else: 
                    self.cache.append(newCacheItem)

    def fileReceived(self, packet, pendingItem): 
        if packet.fromServer == True:
            self.tickLog.numRespFromServer += 1
        else:
            self.tickLog.numRespFromCache += 1
        self.tickLog.numResponces += 1
        self.tickLog.numTicksBeforeResponce += pendingItem.ttlStart - pendingItem.ttl

    def trendBasedCacheRemoveCanAdd(self, packet):
        index = -1
        compValue = (1.0/packet.data.cacheInterval) * math.sqrt(packet.data.ttl)
        for i in range(len(self.cache)):
            tmpCompVal = (1.0/self.cache[i].data.cacheInterval) * math.sqrt(self.cache[i].data.ttl)
            if tmpCompVal > compValue:
                index = i
                compValue = tmpCompVal
        if index < 0:
            return False
        itemToRemove = self.cache[i]
        self.cache.remove(itemToRemove)
        return True

    def shouldICacheFile(self, packet):
        if self.isServer == True:
            return
        if packet.data.cacheInterval > 0:
            if packet.nodeHops % packet.data.cacheInterval == 0:
                if len(self.cache) >= self.cacheSize:
                    if self.trendBasedCacheRemoveCanAdd(packet):
                        cf = AHSCacheFile.cacheFile(packet.data, packet.fromServerX, packet.fromServerY)
                        newCF = copy.deepcopy(cf)
                        self.cache.append(newCF)
                else:
                    cf = AHSCacheFile.cacheFile(packet.data, packet.fromServerX, packet.fromServerY)
                    newCF = copy.deepcopy(cf)
                    self.cache.append(newCF)
                


#############################
#       SERVER STUFF        #
#############################
    def serverProvideFile(self, packet, cFile):
        d = AHSData.data(cFile.data.dType, dataTTL, cFile.data.content, cFile.data.trendVal, cFile.data.cacheInterval)
        newD = copy.deepcopy(d)
        p = AHSPacket.packet(2, 99999, self.x, self.y, self.x, self.y, packet.fromNodeX, packet.fromNodeY, 0, 0, newD, True)
        newP = copy.deepcopy(p)
        self.freshPackets.append(newP)

    def updateFilesTrendData(self, data):
        data.trendVal = (weightNewTrendVal * (baseTime + ticksSinceStart)) + ((1 - weightNewTrendVal) * data.trendVal)

    def updateTrendData(self, packet):
        index = -1
        for i in range(len(self.cache)):
            if self.cache[i].data.content == packet.data.content:
                index = i
                break
        if index < 0:
            tb.pr("THIS SHOULD NEVER HAPPEN. THE SIMULATOR IS BROKEN IN SOME WAY!!")
            tb.pr("SERVER HASN'T GOT THE FILE!!!")
            tb.pr("THIS IS MY CACHE: {}".format([c.data.content for c in self.cache]))
            return
        if packet.pType == 0:   # UPDATE FROM GET REQUEST TO SERVER
            d = self.cache[index].data
            self.updateFilesTrendData(d)
        else:                   # UPDATE FROM NODE
            d = self.cache[index].data
            d.trendVal = (d.trendVal + packet.data.trendVal) / 2

