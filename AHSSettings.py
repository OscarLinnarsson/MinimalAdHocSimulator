
cacheSize = 5
sideL = 30
numTicks = 501
avalibleFiles = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"] # HAS TO USE " " QUOTES TO WORK AS JSON
policy = 1
dataTTL = 20
packetTTL = 10

'''
simulatedTrendStart = [] 
simulatedTrendEnd = []
simulatedTrendIntervalX = [(20,30), (10,20), (20,30)] # (startX, endX)
simulatedTrendIntervalY = [(20,30), (10,20), (20,30)] # (startY, endY)
'''
'''
simulatedTrendStart = [100, 300] 
simulatedTrendEnd = [200, 450]
simulatedTrendIntervalX = [(0,10), (20,30)] # (startX, endX)
simulatedTrendIntervalY = [(0,10), (20,30)] # (startY, endY)
'''

simulatedTrendStart = [100, 250, 350] 
simulatedTrendEnd = [350, 400]
simulatedTrendIntervalX = [(20,30), (10,20), (20,30)] # (startX, endX)
simulatedTrendIntervalY = [(20,30), (10,20), (20,30)] # (startY, endY)


def getJsonStr():
    jsonStr = ''
    jsonStr += '"cacheSize" : {},'.format(cacheSize)
    jsonStr += '"sideL" : {},'.format(sideL)
    jsonStr += '"numTicks" : {},'.format(numTicks)
    avalibleFilesJsonStr = "{}".format(avalibleFiles)
    avalibleFilesJsonStr = avalibleFilesJsonStr.replace("'", '"')
    jsonStr += '"avalibleFiles" : {},'.format(avalibleFilesJsonStr)
    jsonStr += '"policy" : {},'.format(policy)
    jsonStr += '"dataTTL" : {},'.format(dataTTL)
    jsonStr += '"packetTTL" : {},'.format(packetTTL)
    #jsonStr += '"simulatedTrendStart" : {},'.format(simulatedTrendStart)
    #jsonStr += '"simulatedTrendEnd" : {},'.format(simulatedTrendEnd)
    #jsonStr += '"simulatedTrendIntervalX" : {},'.format(simulatedTrendIntervalX)
    #jsonStr += '"simulatedTrendIntervalY" : {},'.format(simulatedTrendIntervalY)
    return jsonStr
