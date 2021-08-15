#!/usr/bin/python3

### This file contain all the function to generate a BIP39 Mnemonic Seed
import secrets
from itertools import chain, product
import binascii
import sys
import hmac

from hashlib import sha256 , pbkdf2_hmac , sha512



def resize_bin(bin, nbits):
	if nbits - len(bin) > 0:
		for i in range(0, nbits - len(bin)):
			bin = "0" + bin
	return (bin)


def checksum(entropy, nbits):
	entropy_hex = hex(entropy)[2:]
	entropy_bin = bin(entropy)[2:]
	entropy_bin = resize_bin(entropy_bin, nbits)
	fingerprint_hash = sha256(binascii.a2b_hex(resize_bin(entropy_hex, int(nbits/4)))).hexdigest()
	fingerprint = bin(int(fingerprint_hash, 16))[2:]
	fingerprint = resize_bin(fingerprint, 256)
	checksum = str(entropy_bin) + fingerprint[:int(nbits/32)]
	return (checksum)


def get_dic(dict_path):
	wordlist = {}
	with open(dict_path) as dict:
		key = 0
		for line in dict:
			(key, val) = key , line
			wordlist[int(key)] = val
			key += 1
		return (wordlist)


def get_mnemonic(checksum, dict):
	mnemonic = {}
	index = 1
	i = 0
	while i < len(checksum):
		word = int(checksum[i:i+11], 2)
		word = dict.get(word)
		(index, word) = index , word[:-1]
		mnemonic[int(index)] = word
		index += 1
		i += 11
	return (mnemonic)


def mnemonic_to_seed(mnemonic, passphrase):
	mnemonic_phrase = ""
	for key in mnemonic:
		mnemonic_phrase = mnemonic_phrase + mnemonic[key] + " "
	mnemonic_phrase = mnemonic_phrase[:-1] + passphrase
	seed = pbkdf2_hmac("SHA512", bytes(mnemonic_phrase.encode()), bytes(("mnemonic" + passphrase).encode()), 2048).hex()
	return (seed)


def get_wordnumber(word, dict_path):
	index = 0
	with open(dict_path) as dict:
		for line in dict:
			if word == line or word == line[:-1]:
				return bin(index)[2:]
			index += 1
	return ("Error")


def get_uncompleted_mnemonic(phrase, dict_path):
	mnemonic = ""
	phrase = phrase.split(" ")
	for words in phrase:
		mnemonic += get_wordnumber(words, dict_path)
	return(mnemonic)


def bruteforce(charset, maxlength):
	return (''.join(candidate)
		for candidate in chain.from_iterable(product(charset, repeat=i)
		for i in range(1, maxlength + 1)) if len(candidate) == maxlength)


def fill_mnemonic(mnemonic, nbits, dict_path):
	nwords = len(mnemonic) / 11
	mnemonic_test = str(mnemonic)
	bits_to_fill = int(nbits - (nwords * 11))
	list = bruteforce("01", bits_to_fill)
	tries = {}
	index = 0
	for attempt in list:
		mnemonic_test += attempt
		mnemonic_test = checksum(int(mnemonic_test, 2), nbits)
		tries[index] = 	get_mnemonic(mnemonic_test, get_dic(dict_path)).get(nwords + 1)
		mnemonic_test = mnemonic
		index += 1
	return (tries)

		
def printer(phrase, lasts_words):
	print("Phrase :\t", phrase, "\n")
	print("Lasts words finded :\n")
	i = 0
	for key, value in lasts_words.items():
		print("[{}] : {}".format(key, value))
	

def mnemonic_filler(phrase, dict_path):
	nbits = 256
	mnemonic = get_uncompleted_mnemonic(phrase, dict_path)
	ln = len(mnemonic)
	if ln == 121:
		nbits = 128
	elif ln == 154:
		nbits = 160
	elif ln == 187:
		nbits = 192 
	elif ln == 220:
		nbits = 224
	elif ln == 253:
		nbits = 256
	else:
		return("Error : wrong nbits")
	lasts_words = (fill_mnemonic(mnemonic, nbits, dict_path))
	printer(phrase, lasts_words)


def main():
	phrase = ""
	dict_path = "./BIP39_Wordlists/BIP39_EN"
	if len(sys.argv) == 3:
		phrase = sys.argv[1]
		dict_path = sys.argv[2]
	if len(sys.argv) == 2:
		phrase = sys.argv[1]
	mnemonic_filler(phrase, dict_path)

main()