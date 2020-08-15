#!/usr/bin/python
# -*- encoding: utf-8 -*-
# A modern implementation of General Qi Jiguang's "Fanqie Cipher" technique
# Follows General's Qi technique but uses modern Pinyin as opposed to the ancient Fanqie system
import sys
import codecs
from pypinyin import Style, pinyin
from pinyinTable import initials, finals   # Reference dict structures for standard Pinyin initials and finals

# Function to replace multiple chars in a string
def multiReplace(inputStr, replacements):
    # Iterate over the strings to be replaced
    newStr = inputStr
    for replaceStr in replacements:
        newStr = newStr.replace(replaceStr.decode('utf8'), "") 
    return  newStr

# Function to clean input strings (strip whitespace and common punctuation)
def cleanInput(inputStr):
    cleanStr = ''.join(inputStr.split()).strip()
    cleanStr = multiReplace(cleanStr, [',', '.', '-', "'", ':', ';', '"', "(", ")", "!", "&"])
    cleanStr = multiReplace(cleanStr, ['，', '。', '——', "’", '：', '；', "（", "）", '”', "！", "& "])
    return cleanStr.strip().lower()
       
# Get the pinyin initial and final halves of a character's sylablle
# Analogous to General Qi's use of the ancient Fanqie system
def getInitialFinal(char):
    pinyin_text = pinyin(char, style=Style.NORMAL)[0][0]   # Suppress diacritics and tone marks from the output
    initial = pinyin(char, style=Style.INITIALS, strict=False)[0][0]
    final = pinyin_text.replace(initial, "")
    return initial, final

def getTone(char):
    pinyin_text = pinyin(char, style=Style.TONE3)[0][0]
    tone = pinyin_text[-1:]
    if tone.isnumeric(): return tone 
    else: return "0"

# Read in (and clean) the text of a poem from a given filepath
def readPoem(filepath):
    poem = ""
    with codecs.open(filepath, "r", "utf-8") as fin:
        for line in fin:
            poem += line.rstrip("\n")
        poem = cleanInput(poem)
    return poem

# Index the available initials and finals from each of the two poem texts
def indexPoem(poem, flag):
    # Get the pinyin intials and finals for each character in the plaintext
    for x in xrange(1, len(poem)):
        i_f = getInitialFinal(poem[x])   # returns initial and finals
        if flag: initials[i_f[0]] = x
        else: finals[i_f[1]] = x

# Perform enciphering of user's plaintext message. Return ciphertext
def encipher(plainText):
    cipherText = ""
    for char in plainText:
        i_f = getInitialFinal(char)
        tone = getTone(char)
        if initials[i_f[0]] != 'X' and finals[i_f[1]] != 'X':
            # Create ciphertext following General Qi's numerical format e.g. 10-22-1
            cipherText += '{}-{}-{} '.format(str(initials[i_f[0]]), str(finals[i_f[1]]), tone)
        else:
            # Error message for missing Pinyin initials or finals
            # Plaintext message cannot be enciphered using selected poem texts
            print "Error: This Message cannot be Expressed using the given two Poems"
            sys.exit(1)
    return cipherText.strip()

# Perform deciphering of user's ciphertext message. Return plaintext
def decipher(cipherText):
    plainText = ""
    # Split ciphertext into blocks
    cipherText_words = cipherText.split(' ')
    for word in cipherText_words:
        # Split each block according to the three components in General Qi's numerical format
        cipherText_digits = word.split('-')
        initial = cipherText_digits[0]    # Index of character in first poem
        final = cipherText_digits[1]      # Index of character in second poem
        tone = cipherText_digits[2]       # Tone number of original character to be deciphered
        for digit in cipherText_digits:
            # Get the characters from each poem that correspond to the ciphertext
            initial_char = poem_one[int(initial)]
            final_char = poem_two[int(final)]

            # Get the pinyin initial and finals for these character in each poem
            pinyin_initial = getInitialFinal(initial_char)[0]
            pinyin_final = getInitialFinal(final_char)[1]

        # Create the plaintext by combining the Pinyin initial from first poem with the Pinyin final from second poem
        plainText += '{}{}{} '.format(pinyin_initial, pinyin_final, tone)
    return plainText

# Output ciphertext or plaintext messages to file
def outputFile(text, filepath):
    with open(filepath, 'w') as foutput:
        foutput.write(text.encode('utf8'))

cipherText_filepath = "test/ciphertext.txt"
decipherText_filepath = "test/deciphertext.txt"

# Filepaths for the two poem texts
poem_one_filepath = "data/poem_one.txt"
poem_two_filepath = "data/poem_two.txt"

# Read in the two selected poem texts
poem_one = readPoem(poem_one_filepath)
poem_two = readPoem(poem_two_filepath)

# Index available initials and finals available in the texts of the first and second poems
indexPoem(poem_one, True)       # index of available initials
indexPoem(poem_two, False)      # index of available finals

# Get user input option
mode = sys.argv[1]

if mode:
    if mode == "encipher":
        # Get the user's secret message
        # e.g. plainText = u"吃饭了吗"
        plainText = raw_input("Enter Secret Message: ").decode('utf8') 
        cipherText = encipher(plainText)
        outputFile(cipherText, cipherText_filepath)
        print cipherText       

    elif mode == "decipher":
        # Get the user's enciphered message
        # e.g. cipherText = "53-85-1 77-60-4 63-88-0 48-36-0"
        cipherText = raw_input("Enter Ciphertext Message: ").decode('utf8') 
        plainText = decipher(cipherText)      
        outputFile(plainText, decipherText_filepath)
        print plainText.encode('utf8')
else:
    print "Error: Please choose Encode or Decode mode"
