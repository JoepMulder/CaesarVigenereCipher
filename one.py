from collections import Counter
import math
import re
from nltk import ngrams
import numpy as np

class Crypto:
    lan_freqs = [8.2, 1.5, 2.8, 4.2, 12.7, 2.2, 2.0, 6.1, 7.0, 0.1, 0.8, 
                 4.0, 2.4, 6.7, 7.5, 1.9, 0.1, 6.0, 6.3, 9.0, 2.8, 1.0, 
                 2.4, 0.1, 2.0, 0.1]
    
    def decryptShift(self, cipher):
        cipher_freqs = []
        
        # Find character frequencies in cipher
        for i in range(26):
            cipher_freqs.append(cipher.count(chr(97 + i)) / len(cipher) * 100)

        # Calculate distances
        distance = []
        for i in range(26):
            distance_i = 0
            for j in range(26):
                distance_i += abs(self.lan_freqs[j]  - cipher_freqs[(j + i) % 26])
            distance.append(distance_i * 0.5)

        # Find key with lowest distance
        min_distance = distance.index(min(distance))
        key = (min_distance) % 26

        # Decrypt
        plain = []
        for i in range(len(cipher)):
            if (ord(cipher[i]) <  97 or ord(cipher[i]) > 122): #Non-alphabetic
                plain.append(cipher[i])
            else:
                asci = ord(cipher[i]) - key
                if (asci < 97):
                    asci = asci + 26
                plain.append(chr(asci))
                
        
        return ''.join(plain), key
    
    def encryptShift(self, plain, key):
        cipher = []
        for i in range(len(plain)):
            if (ord(plain[i]) <  97 or ord(plain[i]) > 122):
                cipher.append(plain[i])
            else:
                asci = ord(plain[i]) + key
                if (asci > 122):
                        asci = asci-26
                cipher.append(chr(asci))

        return ''.join(cipher)
    
    def decryptVigenere(self, cipher):       
        keyLength = self.mostLikelyKeyLength(cipher)
        key = self.findVigenereKeyByLength(cipher, keyLength)
        plain = self.decryptVigenereWithKey(cipher, key)
        return keyLength, key, plain
    
    def mostLikelyKeyLength(self, cipher):
        cipherTextOnly = ''.join(x for x in cipher if x.isalpha()) 
        bigrams = ngrams(cipherTextOnly, 2) # Get all bigrams in cipher
        gcd_dict = {}
        for grams in bigrams:
            bigram = ''.join(grams)
            bigram_count = cipherTextOnly.count(bigram)

            if (bigram_count > 1):
                bigram_indices = [m.start() for m in re.finditer(bigram, cipherTextOnly)]
                gaps = [bigram_indices[i+1] - bigram_indices[i] for i in range(len(bigram_indices)-1)]
                gcd = math.gcd(*gaps)
                
                # If valid gcd for gaps of bigram add to dictionary
                if (len(gaps) > 1 and gcd > 3): 
                    exists = gcd_dict.get(str(gcd))
                    if (exists):
                        gcd_dict[str(gcd)] = gcd_dict.get(str(gcd)) + 1 
                    else:
                        gcd_dict[str(gcd)] = 1
                    
        # The key length is most likely the most found GCD over all the bigrams          
        most_found_gcd = int(max(gcd_dict, key=gcd_dict.get)) 
        return most_found_gcd
        

    def decryptVigenereWithKey(self, cipher, key):
        plain = []
        idx = 0
        
        for i in range(len(cipher)):          
            if (ord(cipher[i]) <  97 or ord(cipher[i]) > 122):
                plain.append(cipher[i])
            else:
                idx = idx % len(key)
                k = ord(key[idx]) - 97
                ciph = ord(cipher[i])
                pl = ciph - k
                if (pl < 97):
                    pl += 26
                
                idx += 1

                plain.append(chr(pl))

        return ''.join(plain)
    
    def encryptVigenereWithKey(self, plain, key):
        cipher = []
        idx = 0
        
        for i in range(len(plain)):          
            if (ord(plain[i]) <  97 or ord(plain[i]) > 122):
                cipher.append(plain[i])
            else:
                idx = idx % len(key)
                k = ord(key[idx]) - 97
                ciph = ord(plain[i])
                pl = ciph + k
                if (pl > 122):
                    pl -= 26
                
                idx += 1

                cipher.append(chr(pl))

        return ''.join(cipher)
    
    def findVigenereKeyByLength(self, cipher, keyLength):
        cipherTextOnly = ''.join(x for x in cipher if x.isalpha())

        keys = []
        for i in range(keyLength): 
            cipher_freqs = np.zeros(26)
            for j in range (len(cipherTextOnly)):
                if j % keyLength == i:
                    idx = ord(cipherTextOnly[j])
                    idx -= 97
                    cipher_freqs[idx] += 1 

            distance = []
            for i in range(26):
                distance_i = 0
                for j in range(26):
                    distance_i += abs(self.lan_freqs[j]  - cipher_freqs[(j + i) % 26])
                distance.append(distance_i * 0.5)

            
            min_distance = distance.index(min(distance))
            keys.append(chr(min_distance+97))
        
        return ''.join(keys)

if __name__ == '__main__':
    c = Crypto()
    
    # Shift Cipher
    print("Shift Cipher example\n")
    shiftKey = 9
    plainText = 'This is a secret message encrypted with a shift cipher with key: ' + str(shiftKey) + '. It can be decrypted by using character frequencies of the English language'
    cipher = c.encryptShift(plainText, shiftKey)
    print("Ciphertext of original message: ", cipher)
    
    plain, key = c.decryptShift(cipher)
    print("Original plaintekst: ", plain)
    print("Key used: ", key)

    # Vigenere Cipher
    print("\n\nVigenere Cipher example")
    vigenereKey = "eminem"
    vigenerePlain = '''
        His palms are sweaty, knees weak, arms are heavy
        There's vomit on his sweater already, mom's spaghetti
        He's nervous, but on the surface, he looks calm and ready
        To drop bombs, but he keeps on forgetting
        What he wrote down, the whole crowd goes so loud
        He opens his mouth, but the words won't come out
        He's chokin', how? Everybody's jokin' now
        The clock's run out, time's up, over, blaow
        Snap back to reality, ope, there goes gravity
        Ope, there goes Rabbit, he choked, he's so mad
        But he won't give up that easy, no, he won't have it
        He knows his whole back's to these ropes, it don't matter
        He's dope, he knows that, but he's broke, he's so stagnant
        He knows when he goes back to this mobile home, that's when it's
        Back to the lab again, yo, this old rhapsody
        Better go capture this moment and hope it don't pass him
    '''

    cipherB = c.encryptVigenereWithKey(vigenerePlain.lower(), vigenereKey)
    print("Ciphertext of original message: ", cipherB)

    keyLength, key, plain = c.decryptVigenere(cipherB)
    print("\nplaintext:", plain, "\nkey: ", key, "\nkeyLength:", keyLength)






