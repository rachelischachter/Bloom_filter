from BitHash import BitHash
from BitVector import BitVector

class BloomFilter(object):
    # Return the estimated number of bits needed (N) in a Bloom 
    # Filter that will store numKeys (n) keys, using numHashes 
    # (d) hash functions, and that will have a
    # false positive rate of maxFalsePositive (P).
    # See the slides for the math needed to do this.  
    # You use Equation B to get the desired phi from P and d
    # You then use Equation D to get the needed N from d, phi, and n
    # N is the value to return from bitsNeeded
    
    # N- bits needed (return)
    # n- numkeys to be stored 
    # d- numHashes number of hash functions 
    # P- maxFalsePositive
    
    def __bitsNeeded(self, numKeys, numHashes, maxFalsePositive):
        # phi- expected proportion of bits that are zero after inserting n keys 
        phi = 1 - (maxFalsePositive ** (1/numHashes)) 
        
        # number of bits needed to store numKeys keys with accuracy of maxFalsePositive
        N = numHashes / (1 - (phi ** (1 / numKeys))) 
        
        return int(N)
    
    # Create a Bloom Filter that will store numKeys keys, using 
    # numHashes hash functions, and that will have a false positive 
    # rate of maxFalsePositive.
    
    def __init__(self, numKeys, numHashes, maxFalsePositive):
        # how big does the big vector have to be? 
        size2 = self.__bitsNeeded(numKeys, numHashes, maxFalsePositive) 
        # the bloom filter bit vector 
        self.__bf = BitVector(size = size2)
        #self.__bf = [0] * size2
        
        # other attributes
        self.__setBits = 0
        self.__numHashes = numHashes 
       
        
    
    # insert the specified key into the Bloom Filter.
    # Doesn't return anything, since an insert into 
    # a Bloom Filter always succeeds!
    def insert(self, key):
        
        # for i in 1 ... d, set the bit at position Hash(key) % N 
        for i in range(1, self.__numHashes + 1): 
            # position in the bloom filter is the hashVal based on ith hash function mod the len of the filter
            pos = BitHash(key, i) % len(self.__bf)
            
            # see if bit is already set. If not, set it and increment counter
            if self.__bf[pos] != 1:
                self.__setBits += 1
                self.__bf[pos] = 1
        
            
    # Returns True if key MAY have been inserted into the Bloom filter. 
    # Returns False if key definitely hasn't been inserted into the BF.

    def find(self, key):
        # for i = 1 ... d, check the buit position at H(key) % N
        # if any of those bits are 0, return false. If all three are 1, return true
        for i in range(1, self.__numHashes + 1):
            pos = BitHash(key, i) % len(self.__bf)
            if self.__bf[pos] == 0:
                return False 
        return True  
       
    # Returns the PROJECTED current false positive rate based on the
    # ACTUAL current number of bits actually set in this Bloom Filter. 
    # This is NOT the same thing as trying to use the Bloom Filter and
    # measuring the proportion of false positives that are actually encountered.
    
    # P- false positive rate. SOLVING FOR THIS
    # phi- zero bits
    # d = number of hash functions
 
    def falsePositiveRate(self):
        zeroBits = len(self.__bf) - self.__setBits
        phi = zeroBits / len(self.__bf)

        answer = (self.__setBits / len(self.__bf)) ** self.__numHashes
        answer2 = (1 - phi) ** self.__numHashes
        return answer2
    
       
    # Returns the current number of bits ACTUALLY set in this Bloom Filter
    def numBitsSet(self):
        return self.__setBits     

def __main():

    # create the Bloom Filter - (numKeys, numHashes, maxFalsePositive)
    numKeys = 100000
    numHashes = 4
    maxFalsePositive = .05
    
    bf = BloomFilter(numKeys, numHashes, maxFalsePositive)
    
    
    # read the first numKeys words from the file and insert them into the Bloom Filter. Close the input file.
    with open("wordlist.txt", "r") as file:
        for i in range(numKeys):
            word = file.readline().rstrip()
            if not word: break
            bf.insert(word)
    file.close()
    # Print out what the PROJECTED false positive rate should 
    print("Projected false positive rate: ", maxFalsePositive)
    
    # THEORETICALLY be based on the number of bits that ACTUALLY ended up being set
    # in the Bloom Filter. Using the falsePositiveRate method.

    print("Theoretical false positive rate: ", bf.falsePositiveRate())
    
    # Re-open the file, and re-read the same bunch of the first numKeys 
    # words from the file and count how many are missing from the Bloom Filter, 
    # printing out how many are missing. This should report that 0 words are 
    # missing from the Bloom Filter.  
    missing = 0
    falsePos = 0
    with open("wordlist.txt", "r") as file:
        for i in range(numKeys):    
            word = file.readline().rstrip()
            if not word: break
            # if you can't find the word in the list, increment missing counter
            if not bf.find(word): 
                missing += 1  
        print("Number of words missing from the Bloom Filter: ", missing)

    # Read the next numKeys words from the file, none of which 
    # have been inserted into the Bloom Filter, and count how many of the 
    # words can be (falsely) found in the Bloom Filter.
    
        for i in range(numKeys):
            word = file.readline().rstrip()
            if not word: break
            # if you find the word, increment falsePos counter
            if bf.find(word): 
                falsePos += 1 
        file.close()
    
    # Print out the percentage rate of false positives.
    print("Calculated false positive percentage: ", falsePos/numKeys, "  |    Compared to expected false positive rate", maxFalsePositive) 


 

    
if __name__ == '__main__':
    __main()       

