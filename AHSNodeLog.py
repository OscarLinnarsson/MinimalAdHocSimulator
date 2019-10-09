
class nodeTickLog:

    def __init__(self, jsonStr = None):
        if jsonStr == None:
            self.numOwnReq = 0
            self.numSentPackages = 0
            self.numSentGET = 0
            self.numSentPOST = 0
            self.numSentRESPONCE = 0
            self.numSentFILE = 0
            self.numResponces = 0
            self.numRespFromServer = 0
            self.numRespFromCache = 0
            self.currentCacheSize = 0
            self.currentCache = ""
            self.numStopWaiting = 0
            self.numTicksBeforeResponce = 0
        else:
            self.numOwnReq = jsonStr["numOwnReq"]
            self.numSentPackages = jsonStr["numSentPackages"]
            self.numSentGET = jsonStr["numSentGET"]
            self.numSentPOST = jsonStr["numSentPOST"]
            self.numSentRESPONCE = jsonStr["numSentRESPONCE"]
            self.numSentFILE = jsonStr["numSentFILE"]
            self.numResponces = jsonStr["numResponces"]
            self.numRespFromServer = jsonStr["numRespFromServer"]
            self.numRespFromCache = jsonStr["numRespFromCache"]
            self.currentCacheSize = jsonStr["currentCacheSize"]
            self.currentCache = jsonStr["currentCache"]
            self.numStopWaiting = jsonStr["numStopWaiting"]
            self.numTicksBeforeResponce = jsonStr["numTicksBeforeResponce"]

    def getJsonStr(self):
        jsonStr = "{"
        jsonStr += '"numOwnReq" : {},'.format(self.numOwnReq)
        jsonStr += '"numSentPackages" : {},'.format(self.numSentPackages)
        jsonStr += '"numSentGET" : {},'.format(self.numSentGET)
        jsonStr += '"numSentPOST" : {},'.format(self.numSentPOST)
        jsonStr += '"numSentRESPONCE" : {},'.format(self.numSentRESPONCE)
        jsonStr += '"numSentFILE" : {},'.format(self.numSentFILE)
        jsonStr += '"numResponces" : {},'.format(self.numResponces)
        jsonStr += '"numRespFromServer" : {},'.format(self.numRespFromServer)
        jsonStr += '"numRespFromCache" : {},'.format(self.numRespFromCache)
        jsonStr += '"currentCacheSize" : {},'.format(self.currentCacheSize)
        jsonStr += '"currentCache" : "{}",'.format(self.currentCache)
        jsonStr += '"numStopWaiting" : {},'.format(self.numStopWaiting)
        jsonStr += '"numTicksBeforeResponce" : {},'.format(self.numTicksBeforeResponce)
        
        jsonStr = jsonStr[:-1]
        jsonStr += "}"
        return jsonStr

        