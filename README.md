# General Qi Jiguang's "Fanqie Cipher"

An implementation of the famous Chinese General Qi Jiguang's (戚继光) so-called "Fanqie Cipher (反切码)" technique. The [Fanqie Cipher](https://baike.baidu.com/item/反切码/3837017) is one of the few, if not only, known examples of a cryptographic cipher having been developed in ancient China. 

## Background

There's scant evidence of cryptographic developments in ancient China; the language perhaps not lending itself well to cryptography. Some famous examples of secret codes used in ancient Chinese, such as Yinfu (阴符), were not based around the written language at all.  

### General Qi Jiguang (戚继光)

[Qi Jiguang](https://baike.baidu.com/item/戚继光/22374) was a Chinese military general during the Ming Dynasty, credited for leadership in the fight against the Japanese Wokou pirates. He was also a military strategist, authoring two books and an accomplished poet. 

<p align="center">
  <img src="/doc/qijiguang.jpg">
</p>

### The Fanqie Cipher (反切码)

General Qi's [Fanqie Cipher](https://baike.baidu.com/item/反切码/3837017) technique drew on a phonetic system existing at the time called Fanqie (反切). Similar to other Chinese phonetic systems, the syllable of each Chinese character was split into two sounds, the Initial (声母) and the Final (韵母) sounds.

In Fanqie, two different (often common) characters are combined and used to communicate the syllable of a third. The Initial of the first character is combined with the Final of the second character to form the syllable of a third character. 

Worth noting that there's no dictionary-like mapping of one symbol to one sound, meaning Fanqie, much like other Chinese phonetic systems, is still ambiguous. 

How did General Qi use this as a cipher? He would craft two poems!  

The first poem would contain characters used to encode Initials, while the second poem the Finals. General Qi communicated his ciphertext numerically like 5-52-1, 7-12-4, where each three block of three numbers corresponds to one enciphered character. The first number represents the location of characters in the first poem (representing the Initials), the second number representing characters in the second poem (representing the Finals), and the final number denoting the enciphered character's tone.  

As an art form, poetry doesn't strictly follow grammatical rules. It can be more fluid. This means while common cryptanalysis techniques such as statistical frequency analysis would identify the final number as never being above 8 (tones used in ancient Chinese), and the likely repeated use of many military phrases and thus their corresponding numbers, that's all without the General's poems. The enemy might work out that 52 appears to correlate with "attack", but that's all. Attack where and when? 

The poems essentially act as the cipher key.

If the poems can be memorable enough, the General's technique can also be a paperless key system.

More about the phonetic system called Fanqie here in [English](https://en.wikipedia.org/wiki/Fanqie) and [Chinese](https://baike.baidu.com/item/反切/2339773).

### Implementing General Qi's Cipher Technique with Pinyin

As mastery of the ancient Fanqie system is far beyond my grasp, I've chosen to implement General Qi's technique using the modern Pinyin system. The technique is otherwise the same. A single plaintext character is enciphered using its Pinyin Initial and Final, which are then matched to the same Initial and Final sounds of different characters contained in the poetry files *poem_one.txt* and *poem_two.txt*. 

The poems used in the two poetry files are collections of famous classical Chinese poetry. In order to get a good range of sounds, I've combined multiple poems from different poets in one file. 

Any classical poems or other texts could be placed into the ./data directory for use. The script will try to index the sounds available in each of the two poetry files. 

If plaintext message can't be enciphered using the selected poems (i.e. the sounds in the plaintext cannot be expressed via the sounds available in the collected poems), the script will return an associated error.  

## Getting Started

### Prerequisites

The cipher script is written in Python 2.7.

The following Python module is required:

```
import pypinyin
```

You can read more about [PyPinyin](https://github.com/mozillazg/python-pinyin). This module will do the hard work of translating the Chinese language characters to their equivalent Pinyin forms. 

Required Python modules can be installed via PyPI:

```
pip install pypinyin
```

### Usage

Script can be run from the command line using passing two options 1. "encipher" 2. "decipher"

e.g. 
```
Python fanqieCipher.py encipher
Enter Secret Message:
```

The script will then prompt the user to input their plaintext message for enciphering.

### An Example

Using the two poetry files in this repo's /data directory, the message below can be enciphered as follows:

Plaintext: "吃饭了吗"

The syllable of each character can be matched to their Initial-Final pairs in Pinyin:

| Character | Initial   | Final     | Tone      |
|:---------:|:---------:|:---------:|:---------:|
| 吃        | Ch        | I         | 1st       |
| 饭        | F         | An        | 4th       |
| 了        | L         | E         | Neutral   |
| 吗        | M         | A         | Neutral   |

These Initial-Final pairs are then matched to the following Characters from texts of Poem One and Poem Two:

| Initial | Character (Poem One) | Character Number (Poem One)|
|:-------:|:--------------------:|:--------------------------:|
| Ch      | 处                   | 54                         |
| F       | 釜                   | 78                         |
| L       | 落                   | 64                         |
| M       | 眠                   | 49                         |

| Final | Character (Poem Two) | Character Number (Poem Two)|
|:-------:|:--------------------:|:--------------------------:|
| I       | 一                   | 86                         |
| An      | 山                   | 61                         |
| E       | 野                   | 89                         |
| A       | 踏                   | 37                         |

The above can be put into General Qi's numerical ciphertext format as shown below.

Format: Character from Poem One - Character from Poem Two - Tone of Plaintext Character.

Ciphertext: 54-86-1, 78-61-4, 64-89-0, 49-37-0

## Built With

* [Python](http://www.python.org)
* [PyPinyin](https://github.com/mozillazg/python-pinyin)

## Authors

* **Andrew Houlbrook** - *Initial work* - [AndrewHoulbrook](https://github.com/andrewhoulbrook)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details