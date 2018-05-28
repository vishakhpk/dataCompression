"""
Usage: python huffmanCoding.py <filename> 
"""

import heapq
import sys

class Node(object):
    def __init__(self, data, frequency):
        self.data = data
        self.left = None
        self.right = None
        self.freq = frequency

def displayQueue(queue):
    for i in queue:
        print i[0], repr(i[1].data)

def makeFrequencyDictionary(filename):
    freqDict = {}
    with open(filename) as f:
        text = f.read()
        text = text.strip()
        for char in text:
            if char in freqDict:
                freqDict[char]+=1
            else:
                freqDict[char]=1
    print "Dictionary Made"
    #print freqDict
    return freqDict

def makeMinHeap(freqDict):
    minHeapFreq = []
    nodeList = []
    nodeLocation = {}
    k = 0
    
    for key in freqDict.keys():
        tempNode = Node(key, freqDict[key])
        heapq.heappush(minHeapFreq, (freqDict[key], tempNode) )
        nodeList.append(tempNode)
        nodeLocation[key] = k
        k+=1
    
    print "Min Heap Constructed"

    while len(minHeapFreq)>1:
        tuple1 = heapq.heappop(minHeapFreq)
        tuple2 = heapq.heappop(minHeapFreq)
        #print "Extracted Tuples: ", tuple1, tuple2
    
        tempTupleFreq = freqDict[tuple1[1].data]+freqDict[tuple2[1].data]
        tempTupleKey = tuple1[1].data + tuple2[1].data
        freqDict[tempTupleKey] = tempTupleFreq
    
        tempNode = Node(tempTupleKey, tempTupleFreq)
        tempNode.left = nodeList[nodeLocation[tuple1[1].data]]
        tempNode.right = nodeList[nodeLocation[tuple2[1].data]]
        heapq.heappush(minHeapFreq, (tempTupleFreq, tempNode))
        nodeList.append(tempNode)
        nodeLocation[tempTupleKey] = k
        k+=1
    return minHeapFreq, nodeList, nodeLocation

def makeCodes(root, currentCode, finalCodes, reverseCodes):
    if root==None:
        return
    if root.data!=None and root.left==None and root.right==None:
        finalCodes[root.data]=currentCode
        reverseCodes[currentCode] = root.data
    makeCodes(root.left, currentCode+"0", finalCodes, reverseCodes)
    makeCodes(root.right, currentCode+"1", finalCodes, reverseCodes)

def main(filename):
    freqDict = makeFrequencyDictionary(filename)
    minHeapFreq, nodeList, nodeLocation = makeMinHeap(freqDict)

    finalCodes = {}
    reverseCodes = {}
    root = heapq.heappop(minHeapFreq)[1]
    currentCode = ""
    makeCodes(root, currentCode, finalCodes, reverseCodes)
    print finalCodes
    
    encodedText = ""
    with open(filename) as f:
        text = f.read()
        text = text.strip()
        for character in text:
            encodedText+=finalCodes[character]
    print encodedText
    
    paddingLength = 8 - (len(encodedText)%8)
    for i in range(paddingLength):
        encodedText += "0"
    paddedInfo = "{0:08b}".format(paddingLength)
    encodedText = paddedInfo + encodedText
     
    print encodedText

    outputBytes = bytearray()
    for i in range(0, len(encodedText), 8):
        byte = encodedText[i:i+8]
        outputBytes.append(int(byte,2))

    with open(filename+ ".paddy", "w") as f:
        f.write(bytes(outputBytes))
    
    bitString = ""
    with open(filename+".paddy", "r") as f:
        byte = f.read(1)
        while(byte!=""):
            byte = ord(byte)
            bits = bin(byte)[2:].rjust(8, '0')
            bitString += bits
            byte = f.read(1)
    
    paddedInfo = bitString[:8]
    padding = int(paddedInfo, 2)

    encodedText = bitString[8:] 
    encodedText = encodedText[:-1*padding]
    
    currentCode = ""
    decodedText = ""
    
    for bit in encodedText:
        currentCode+=bit
        if currentCode in reverseCodes:
            decodedText+=reverseCodes[currentCode]
            print currentCode, decodedText
            currentCode = ""
    print decodedText

if __name__=="__main__":
    main(sys.argv[1])
