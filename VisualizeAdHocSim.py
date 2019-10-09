import matplotlib as mpl
import matplotlib.pyplot as plt
import png # library - PyPNG

import json
import copy
import math

import AHSNodeLog


#############################################################
#####                                                   #####
#####       LOAD ALL SIMULATION LOG FILES NEEDED        #####
#####                                                   #####
#############################################################

scenario = input("What scenario do you want to visualize? ")

logFileSim1 = open("AdHocSimulatorLog - S{}P1.txt".format(scenario), "r") # r - read
logFileSim1Str = logFileSim1.readline()
jsonLogSim1 = json.loads(logFileSim1Str)

logFileSim2 = open("AdHocSimulatorLog - S{}P2.txt".format(scenario), "r") # r - read
logFileSim2Str = logFileSim2.readline()
jsonLogSim2 = json.loads(logFileSim2Str)

logFileSim3 = open("AdHocSimulatorLog - S{}P3.txt".format(scenario), "r") # r - read
logFileSim3Str = logFileSim3.readline()
jsonLogSim3 = json.loads(logFileSim3Str)



#####################################################
#####                                           #####
#####       INITIALIZE NECESSARY VARIABLES      #####
#####                                           #####
#####################################################

cacheSize = jsonLogSim1["cacheSize"]
sideL = jsonLogSim1["sideL"]
numOfNodes = sideL * sideL
numTicks = jsonLogSim1["numTicks"]
avalibleFiles = jsonLogSim1["avalibleFiles"]
policy = jsonLogSim1["policy"]
dataTTL = jsonLogSim1["dataTTL"]
packetTTL = jsonLogSim1["packetTTL"]



#########################################################################
#####                                                               #####
#####       CREATE NECESSARY FUNCTIONS FOR DATA VISUALIZATION       #####
#####                                                               #####
#########################################################################

'''
def perResponce(val, respCount):
    if respCount == 0:
        return 0
    return val/respCount
'''
'''
def printMap(map):
    for r in map:
        tmpStr = "["
        for val in r:
            if val < 10:
                tmpStr += "  {},".format(val)
            elif val < 100:
                tmpStr += " {},".format(val)
            else:
                tmpStr += "{},".format(val)
        tmpStr += "]"
        print(tmpStr)
'''

def createPNG(name, map):
    f = open(name, 'wb')
    w = png.Writer(sideL, sideL)
    w.write(f, map) ; f.close()

def getMaxSentPackets(map):
    tmpMax = 0
    for row in map:
        for n in row:
            if tmpMax < sum([log.numSentPackages for log in n]):
                tmpMax = sum([log.numSentPackages for log in n])
    return tmpMax

def getMaxSentResponces(map):
    tmpMax = 0
    for row in map:
        for n in row:
            if tmpMax < sum([log.numSentRESPONCE for log in n]):
                tmpMax = sum([log.numSentRESPONCE for log in n])
    return tmpMax

supermaxSentPackets = 0
supermaxSentGet = 0
supermaxSentResp = 0
supermaxTimedOut = 0
supermaxCache = 0
def createSuperMax(mapSim1, mapSim2, mapSim3):
    global supermaxSentPackets
    global supermaxSentGet
    global supermaxSentResp
    global supermaxTimedOut
    global supermaxCache
    for row in mapSim1:
        for n in row:
            if supermaxSentPackets < sum([log.numSentPackages for log in n]):
                supermaxSentPackets = sum([log.numSentPackages for log in n])
            if supermaxSentGet < sum([log.numSentGET for log in n]):
                supermaxSentGet = sum([log.numSentGET for log in n])
            if supermaxSentResp < sum([log.numSentRESPONCE for log in n]):
                supermaxSentResp = sum([log.numSentRESPONCE for log in n])
            if supermaxTimedOut < sum([log.numStopWaiting for log in n]):
                supermaxTimedOut = sum([log.numStopWaiting for log in n])
            if supermaxCache < sum([log.currentCacheSize for log in n]):
                supermaxCache = sum([log.currentCacheSize for log in n])
    for row in mapSim2:
        for n in row:
            if supermaxSentPackets < sum([log.numSentPackages for log in n]):
                supermaxSentPackets = sum([log.numSentPackages for log in n])
            if supermaxSentGet < sum([log.numSentGET for log in n]):
                supermaxSentGet = sum([log.numSentGET for log in n])
            if supermaxSentResp < sum([log.numSentRESPONCE for log in n]):
                supermaxSentResp = sum([log.numSentRESPONCE for log in n])
            if supermaxTimedOut < sum([log.numStopWaiting for log in n]):
                supermaxTimedOut = sum([log.numStopWaiting for log in n])
            if supermaxCache < sum([log.currentCacheSize for log in n]):
                supermaxCache = sum([log.currentCacheSize for log in n])
    for row in mapSim3:
        for n in row:
            if supermaxSentPackets < sum([log.numSentPackages for log in n]):
                supermaxSentPackets = sum([log.numSentPackages for log in n])
            if supermaxSentGet < sum([log.numSentGET for log in n]):
                supermaxSentGet = sum([log.numSentGET for log in n])
            if supermaxSentResp < sum([log.numSentRESPONCE for log in n]):
                supermaxSentResp = sum([log.numSentRESPONCE for log in n])
            if supermaxTimedOut < sum([log.numStopWaiting for log in n]):
                supermaxTimedOut = sum([log.numStopWaiting for log in n])
            if supermaxCache < sum([log.currentCacheSize for log in n]):
                supermaxCache = sum([log.currentCacheSize for log in n])

def createImages(allSimNodes, pol):
    nodeCacheMap = []
    nodeTimedOutMap = []
    nodeSentPMap = []
    mapSentGET = []
    mapSentPOST = []
    mapSentRESPONCE = []
    mapSentFILE = []

    for row in allSimNodes:
        cacheRow = []
        timedOutRow = []
        sentPRow = []
        rowSentGET = []
        rowSentPOST = []
        rowSentRESPONCE = []
        rowSentFILE = []
        for n in row:
            tmpCacheSum = sum([log.currentCacheSize for log in n])
            cacheRow.append(int(tmpCacheSum*255.0/supermaxCache))
            
            tmpTimedOutSum = sum([log.numStopWaiting for log in n])
            timedOutRow.append(int(tmpTimedOutSum*255.0/supermaxTimedOut))
            
            tmpSentP = sum([log.numSentPackages for log in n])
            sentPRow.append(int(tmpSentP*255.0/supermaxSentPackets))

            tmpSentGET = sum([log.numSentGET for log in n])
            rowSentGET.append( int(tmpSentGET*255.0/supermaxSentGet) )
            
            tmpSentPOST = sum([log.numSentPOST for log in n])
            rowSentPOST.append(int(255 - math.floor(255*1.0 / (1 + tmpSentPOST*1.0/numTicks))))
            
            tmpSentRESP = sum([log.numSentRESPONCE for log in n])
            rowSentRESPONCE.append(int(tmpSentRESP*255.0/supermaxSentResp))

            tmpSentFILE = sum([log.numSentFILE for log in n])
            rowSentFILE.append(int(255 - math.floor(255*1.0 / (1 + tmpSentFILE*1.0/numTicks))))

        nodeCacheMap.append(cacheRow)
        nodeTimedOutMap.append(timedOutRow)
        nodeSentPMap.append(sentPRow)
        mapSentGET.append(rowSentGET)
        mapSentPOST.append(rowSentPOST)
        mapSentRESPONCE.append(rowSentRESPONCE)
        mapSentFILE.append(rowSentFILE)

    createPNG('cacheIntesityMap - S{}P{}.png'.format(scenario, pol), nodeCacheMap)
    createPNG('timedOutIntesityMap - S{}P{}.png'.format(scenario, pol), nodeTimedOutMap)
    createPNG('sentPackagesIntensityMap - S{}P{}.png'.format(scenario, pol), nodeSentPMap)
    createPNG('sentGET - S{}P{}.png'.format(scenario, pol), mapSentGET)
    createPNG('sentRESPONCES - S{}P{}.png'.format(scenario, pol), mapSentRESPONCE)
    createPNG('sentPOST - S{}P{}.png'.format(scenario, pol), mapSentPOST)
    createPNG('sentFILE - S{}P{}.png'.format(scenario, pol), mapSentFILE)


def get2DArrayNodeTickLogs(jsonSimData):
    nodeMap = []
    for x in range(sideL):
        row = []
        for y in range(sideL):
            row.append([])
        nodeMap.append(row)
    for tick in jsonSimData["allLogs"]:    
        for index in range(sideL*sideL):
            tmpI = copy.deepcopy(index)
            y = tmpI % sideL
            tmpI -= y
            x = tmpI / sideL
            newLog = AHSNodeLog.nodeTickLog(tick["allLogsOneTick"][index])
            nodeMap[x][y].append(newLog)
    return nodeMap

def getNetworkLogSumTickTimeline(allSimNodes):
    logSumTimeline = []
    for i in range(numTicks):
        log = AHSNodeLog.nodeTickLog()
        for row in allSimNodes:
            for n in row:
                log.numOwnReq += n[i].numOwnReq
                log.numSentPackages += n[i].numSentPackages
                log.numRespFromServer += n[i].numRespFromServer
                log.numRespFromCache += n[i].numRespFromCache
                log.currentCacheSize += n[i].currentCacheSize
                log.currentCache += n[i].currentCache
                log.numStopWaiting += n[i].numStopWaiting
                log.numTicksBeforeResponce += n[i].numTicksBeforeResponce
                log.numResponces += n[i].numResponces
                log.numSentGET += n[i].numSentGET
                log.numSentPOST += n[i].numSentPOST
                log.numSentRESPONCE += n[i].numSentRESPONCE
                log.numSentFILE += n[i].numSentFILE
        logSumTimeline.append(log)
    return logSumTimeline

def printSimulationSummary(networkSumLogArr):
    numOwnRequests = sum([log.numOwnReq for log in networkSumLogArr])
    numRequestsWhichTimedOut = sum([log.numStopWaiting for log in networkSumLogArr])
    numResponces = sum([log.numResponces for log in networkSumLogArr])
    numResponcesFromCache = sum([log.numRespFromCache for log in networkSumLogArr])
    numResponcesFromServer = sum([log.numRespFromServer for log in networkSumLogArr])
    pendingReq = numOwnRequests - numRequestsWhichTimedOut - numResponces 

    print("Num packages sent: {}".format(sum([log.numSentPackages for log in networkSumLogArr])))
    print("Num packages sent GET: {}".format(sum([log.numSentGET for log in networkSumLogArr])))
    print("Num packages sent POST: {}".format(sum([log.numSentPOST for log in networkSumLogArr])))
    print("Num packages sent RESPONCE: {}".format(sum([log.numSentRESPONCE for log in networkSumLogArr])))
    print("Num packages sent FILE: {}".format(sum([log.numSentFILE for log in networkSumLogArr])))
    print("")
    print("Num own requests: {}".format(numOwnRequests))
    print("Num requests timed out: {}".format(numRequestsWhichTimedOut))
    print("Num pending requests at end: {}".format(pendingReq))
    print("")
    print("Num responces: {}".format(numResponces))
    print("Num responces from cache: {}".format(numResponcesFromCache))
    print("Num responces from server: {}".format(numResponcesFromServer))
    print("")
    print("Ticks file A has been cached [times/node-tick]: {}".format(sum([log.currentCache.count("A") for log in networkSumLogArr]) * 1.0 / (numTicks * sideL * sideL) ))
    print("Ticks file B has been cached [times/node-tick]: {}".format(sum([log.currentCache.count("B") for log in networkSumLogArr]) * 1.0 / (numTicks * sideL * sideL) ))
    print("Ticks file C has been cached [times/node-tick]: {}".format(sum([log.currentCache.count("C") for log in networkSumLogArr]) * 1.0 / (numTicks * sideL * sideL) ))
    print("Ticks file D has been cached [times/node-tick]: {}".format(sum([log.currentCache.count("D") for log in networkSumLogArr]) * 1.0 / (numTicks * sideL * sideL) ))
    print("Ticks file E has been cached [times/node-tick]: {}".format(sum([log.currentCache.count("E") for log in networkSumLogArr]) * 1.0 / (numTicks * sideL * sideL) ))
    print("Ticks file F has been cached [times/node-tick]: {}".format(sum([log.currentCache.count("F") for log in networkSumLogArr]) * 1.0 / (numTicks * sideL * sideL) ))
    print("Ticks file G has been cached [times/node-tick]: {}".format(sum([log.currentCache.count("G") for log in networkSumLogArr]) * 1.0 / (numTicks * sideL * sideL) ))
    print("Ticks file H has been cached [times/node-tick]: {}".format(sum([log.currentCache.count("H") for log in networkSumLogArr]) * 1.0 / (numTicks * sideL * sideL) ))
    print("Ticks file I has been cached [times/node-tick]: {}".format(sum([log.currentCache.count("I") for log in networkSumLogArr]) * 1.0 / (numTicks * sideL * sideL) ))
    print("Ticks file J has been cached [times/node-tick]: {}".format(sum([log.currentCache.count("J") for log in networkSumLogArr]) * 1.0 / (numTicks * sideL * sideL) ))
    print("")


def graphAvrCacheSize(p1, p2, p3):
    fig, ax = plt.subplots()
    plt.title("CACHE SIZE")
    plt.xlabel("time [ticks]")
    plt.ylabel("Average number of files in cache")

    x = range(numTicks)
    ax.plot(x, [(v1.currentCacheSize * 1.0 / (numOfNodes)) for v1 in p1], '-r', label='Policy 1')
    ax.plot(x, [(v2.currentCacheSize * 1.0 / (numOfNodes)) for v2 in p2], '--g', label='Policy 2')
    ax.plot(x, [(v3.currentCacheSize * 1.0 / (numOfNodes)) for v3 in p3], '-*b', label='Policy 3')

    plt.xlim(0, numTicks-1)         #X:s granser
    plt.ylim(0, 6)                  #Y:s granser
    plt.legend(frameon=True, loc='upper right', ncol=1)
    plt.grid(color='k', linestyle='-', linewidth=0.25)
    plt.savefig('/Users/oscarlinnarsson/Desktop/AdHoc-AvrCacheSize-S{}.png'.format(scenario), bbox_inches='tight') 
    #plt.show()


def graphAvrNumSentPackets(p1, p2, p3):
    fig, ax = plt.subplots()
    plt.title("PACKETS SENT")
    plt.xlabel("time [ticks]")
    plt.ylabel("Average number of packets sent")

    x = range(numTicks)
    ax.plot(x, [(v1.numSentPackages * 1.0 / (numOfNodes)) for v1 in p1], '-r', label='Policy 1')
    ax.plot(x, [(v2.numSentPackages * 1.0 / (numOfNodes)) for v2 in p2], '--g', label='Policy 2')
    ax.plot(x, [(v3.numSentPackages * 1.0 / (numOfNodes)) for v3 in p3], '-*b', label='Policy 3')

    plt.xlim(0, numTicks-1)             #X:s granser
    plt.ylim(0, 80)                     #Y:s granser
    plt.legend(frameon=True, loc='upper right', ncol=1)
    plt.grid(color='k', linestyle='-', linewidth=0.25)
    plt.savefig('/Users/oscarlinnarsson/Desktop/AdHoc-AvrNumSentPackets-S{}.png'.format(scenario), bbox_inches='tight') 
    #plt.show()

def graphAvrNumSentGET(p1, p2, p3):
    fig, ax = plt.subplots()
    plt.title("GET PACKETS SENT")
    plt.xlabel("time [ticks]")
    plt.ylabel("Average number of GET packets sent")

    x = range(numTicks)
    ax.plot(x, [(v1.numSentGET * 1.0 / (numOfNodes)) for v1 in p1], '-r', label='Policy 1')
    ax.plot(x, [(v2.numSentGET * 1.0 / (numOfNodes)) for v2 in p2], '--g', label='Policy 2')
    ax.plot(x, [(v3.numSentGET * 1.0 / (numOfNodes)) for v3 in p3], '-*b', label='Policy 3')

    plt.xlim(0, numTicks-1)             #X:s granser
    plt.ylim(0, 70)                     #Y:s granser
    plt.legend(frameon=True, loc='upper right', ncol=1)
    plt.grid(color='k', linestyle='-', linewidth=0.25)
    plt.savefig('/Users/oscarlinnarsson/Desktop/AdHoc-AvrNumSentGET-S{}.png'.format(scenario), bbox_inches='tight') 
    #plt.show()

def graphAvrNumSentFilePerOwnReq(p1, p2, p3):
    fig, ax = plt.subplots()
    plt.title("FILE PACKETS SENT PER OWN REQUEST")
    plt.xlabel("time [ticks]")
    plt.ylabel("Average number of FILE packets sent")

    x = range(numTicks)
    ax.plot(x, [( (v1.numSentFILE + v1.numStopWaiting * 20) * 1.0 / v1.numOwnReq) for v1 in p1], '-r', label='Policy 1')
    ax.plot(x, [( (v2.numSentFILE + v2.numStopWaiting * 20) * 1.0 / v2.numOwnReq) for v2 in p2], '--g', label='Policy 2')
    ax.plot(x, [( (v3.numSentFILE + v3.numStopWaiting * 20) * 1.0 / v3.numOwnReq) for v3 in p3], '-*b', label='Policy 3')

    plt.xlim(0, numTicks-1)             #X:s granser
    plt.ylim(0, 15)                     #Y:s granser
    plt.legend(frameon=True, loc='upper right', ncol=1)
    plt.grid(color='k', linestyle='-', linewidth=0.25)
    plt.savefig('/Users/oscarlinnarsson/Desktop/AdHoc-AvrNumSentFILE-S{}.png'.format(scenario), bbox_inches='tight') 
    #plt.show()

def graphAvrTrafficLoad(p1, p2, p3):
    fig, ax = plt.subplots()
    plt.title("AVERAGE TRAFFIC LOAD")
    plt.xlabel("time [ticks]")
    plt.ylabel("Average traffic load per node\nFILE packets are weighted x20")

    x = range(numTicks)
    ax.plot(x, [(  (v1.numSentPackages + v1.numSentFILE * 19) * 1.0 / (numOfNodes)) for v1 in p1], '-r', label='Policy 1')
    ax.plot(x, [(  (v2.numSentPackages + v2.numSentFILE * 19) * 1.0 / (numOfNodes)) for v2 in p2], '--g', label='Policy 2')
    ax.plot(x, [(  (v3.numSentPackages + v3.numSentFILE * 19) * 1.0 / (numOfNodes)) for v3 in p3], '-*b', label='Policy 3')

    plt.xlim(0, numTicks-1)             #X:s granser
    plt.ylim(0, 90)                     #Y:s granser
    plt.legend(frameon=True, loc='upper right', ncol=1)
    plt.grid(color='k', linestyle='-', linewidth=0.25)
    plt.savefig('/Users/oscarlinnarsson/Desktop/AdHoc-AvrTrafficLoad-S{}.png'.format(scenario), bbox_inches='tight') 
    #plt.show()

def perResponce(val, respCount):
    if respCount == 0:
        return 0
    return val * 1.0 / respCount

def graphAvrRTT(p1, p2, p3):
    fig, ax = plt.subplots()
    plt.title("AVERAGE RTT PER RESPONCE")
    plt.xlabel("time [ticks]")
    plt.ylabel("Average RTT for first responce on GET request")

    x = range(numTicks)
    ax.plot(x, [perResponce(v1.numTicksBeforeResponce, v1.numResponces) for v1 in p1], '-r', label='Policy 1')
    ax.plot(x, [perResponce(v2.numTicksBeforeResponce, v2.numResponces) for v2 in p2], '--g', label='Policy 2')
    ax.plot(x, [perResponce(v3.numTicksBeforeResponce, v3.numResponces) for v3 in p3], '-*b', label='Policy 3')

    plt.xlim(0, numTicks-1)             #X:s granser
    plt.ylim(0, 10)                     #Y:s granser
    plt.legend(frameon=True, loc='upper right', ncol=1)
    plt.grid(color='k', linestyle='-', linewidth=0.25)
    plt.savefig('/Users/oscarlinnarsson/Desktop/AdHoc-AvrRTT-S{}.png'.format(scenario), bbox_inches='tight') 
    #plt.show()


def graphAvrNumTimedOut(p1, p2, p3):
    fig, ax = plt.subplots()
    plt.title("TIMED OUT GET REQUESTS")
    plt.xlabel("time [ticks]")
    plt.ylabel("Average number of GET requests never receiving a responce")

    x = range(numTicks)
    ax.plot(x, [(v1.numStopWaiting * 1.0 / (numOfNodes)) for v1 in p1], '-r', label='Policy 1')
    ax.plot(x, [(v2.numStopWaiting * 1.0 / (numOfNodes)) for v2 in p2], '--g', label='Policy 2')
    ax.plot(x, [(v3.numStopWaiting * 1.0 / (numOfNodes)) for v3 in p3], '-*b', label='Policy 3')

    plt.xlim(0, numTicks-1)             #X:s granser
    plt.ylim(0, 0.2)                    #Y:s granser
    plt.legend(frameon=True, loc='upper right', ncol=1)
    plt.grid(color='k', linestyle='-', linewidth=0.25)
    plt.savefig('/Users/oscarlinnarsson/Desktop/AdHoc-AvrNumTimedOut-S{}.png'.format(scenario), bbox_inches='tight') 
    #plt.show()

#####################################################################################
#####                                                                           #####
#####       CODE FOR EXTRACTING WANTED DATA FROM THE SIMULATION LOG FILE        #####
#####                                                                           #####
#####################################################################################

print("----------------------- SIMULATION 1")
allNodesSim1 = get2DArrayNodeTickLogs(jsonLogSim1)
logArrSim1 = getNetworkLogSumTickTimeline(allNodesSim1)

print("----------------------- SIMULATION 2")
allNodesSim2 = get2DArrayNodeTickLogs(jsonLogSim2)
logArrSim2 = getNetworkLogSumTickTimeline(allNodesSim2)

print("----------------------- SIMULATION 3")
allNodesSim3 = get2DArrayNodeTickLogs(jsonLogSim3)
logArrSim3 = getNetworkLogSumTickTimeline(allNodesSim3)

createSuperMax(allNodesSim1, allNodesSim2, allNodesSim3)


#printSimulationSummary(logArrSim1)
createImages(allNodesSim1, 1)

#printSimulationSummary(logArrSim2)
createImages(allNodesSim2, 2)

#printSimulationSummary(logArrSim3)
createImages(allNodesSim3, 3)

graphAvrCacheSize(logArrSim1, logArrSim2, logArrSim3)
graphAvrNumSentPackets(logArrSim1, logArrSim2, logArrSim3)
graphAvrRTT(logArrSim1, logArrSim2, logArrSim3)
graphAvrNumTimedOut(logArrSim1, logArrSim2, logArrSim3)
graphAvrNumSentGET(logArrSim1, logArrSim2, logArrSim3)
graphAvrNumSentFilePerOwnReq(logArrSim1, logArrSim2, logArrSim3)
graphAvrTrafficLoad(logArrSim1, logArrSim2, logArrSim3)