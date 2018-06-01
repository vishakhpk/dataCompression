# Data Compression Algorithms

## Lempel-Ziv 77
The basic idea behind a dictionary-based compressor is to replace an occurrence of a particular phrase or group of bytes in a piece of data with a reference to a previous occurrence of that phrase. Lempel-Ziv 77 (LZ77) algorithm is the first Lempel-Ziv compression algorithm for sequential data compression. The dictionary is a portion of the previously encoded sequence. The encoder examines the input sequence through a sliding window. Implementation of the algorithm done in python. 

###Usage: 
* python lempelZiv77.py <-c/-d> <file> 

## Huffman Coding
Huffman coding is a lossless statistical data compression algorithm. The idea is to assign variable-length codes to input characters, lengths of the assigned codes are based on the frequencies of corresponding characters. The most frequent character gets the smallest code and the least frequent character gets the largest code.

###Usage: 
* python huffmanCoding.py <file to be compressed>

