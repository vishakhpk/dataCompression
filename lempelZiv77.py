import sys
from bitarray import bitarray

searchBufferSize = 255
lookAheadBufferSize = 300

def compress(filename):
	with open(filename) as f:
        	text = f.read()
        	text = text.strip()
	i = 0
	result = []
	while i<range(len(text)):
		if i < searchBufferSize:
			searchBuffer = text[:i]			
		else:
			searchBuffer = text[i-searchBufferSize:i]
		
		if i+lookAheadBufferSize < len(text):
			lookAheadBuffer = text[i:i+lookAheadBufferSize]
		else:
			lookAheadBuffer = text[i:]
		#print searchBuffer
		#print lookAheadBuffer
		if len(lookAheadBuffer) == 0:
			break
		substring = lookAheadBuffer[0]
		offset = searchBuffer.find(substring)
		if offset == -1:
			offset = 0
			length = 0
			#pattern = substring
		else:
			offset = len(searchBuffer) - offset
			length = 1
			tempSubstring = substring
			for j in range(1, len(lookAheadBuffer)):
				if j == len(lookAheadBuffer):
					break
				tempSubstring = tempSubstring + lookAheadBuffer[j]
				#print tempSubstring, length
				#print searchBuffer.find(tempSubstring)
				if searchBuffer.find(tempSubstring) != -1:
					length+=1
					substring = tempSubstring
					offset = searchBuffer.find(substring)
					offset = len(searchBuffer) - offset
				else:
					break
		if length == len(lookAheadBuffer):
			pattern = '\0'
		else:		
			pattern = lookAheadBuffer[length]
		i+=1
		i+=length
		result.append((offset, length, pattern))
	out = bytearray()
    	for i in result:
        	out.append(i[0])
        	out.append(i[1])
        	out.append(i[2])
	with open(filename+ ".paddy", "w") as f:
        	f.write(bytes(out))
	return result
		
def decompress(filename):
	ba = open(filename, "rb").read()
	res = [[ord(l) for l in ba[m:m+3]] for m in xrange(0, len(ba), 3)]
	for i in res:
		i[2] = chr(i[2])
	text = ""
	for tup in res:
		if tup[1] == 0:
			text += tup[2]
			continue
		if -1*tup[0]+tup[1] !=0:
			text += text[-1*tup[0]:-1*tup[0]+tup[1]]
		else:
			text += text[-1*tup[0]:]			
		text += tup[2]
	print text
	with open(filename[:-6], 'w') as f:
		f.write(text)

if __name__=='__main__':
	if sys.argv[1] == "-c":
		compress(sys.argv[2])
	elif sys.argv[1] == "-d":
		decompress(sys.argv[2])
	else:
		print "Usage: python lz77.py [-c/-d] [filename] "
