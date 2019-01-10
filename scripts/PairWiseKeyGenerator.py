#! /usr/bin/env python3
from pbkdf2 import PBKDF2

ssid = 'home' 
phrase = 'qwerty123'
print ("SSID: "+ ssid)
print ("Pass phrase: "+phrase)
print ("Pairwise Master Key: ")
print (PBKDF2(phrase, ssid, 4096).read(32).hex())