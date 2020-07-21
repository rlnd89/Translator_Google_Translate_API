##################################################################################################################
## Text to Text & Speech Translator Program
##################################################################################################################
##
## Readme:
## 
## Install libraries:
##     - pip install googletrans
##     - pip install pyttsx3
##     - pip install pyperclip
##     - pip install keyboard
##     - pip install pandas
##     - pip install plyer
## or with one liner:
##     - pip install googletrans pyttsx3 pyperclip keyboard pandas plyer
## 
## How to use the program::
##     1) Select text you want to translate
##     2) Copy text to clipboard (ctrl+c or right click --> copy)
##     3) Press "+" for translation
##     4) Press "*" for speech output
##     5) Press "Esc" to stop program and save translated text to file
##                         
##################################################################################################################

### 0) Import libraries
from googletrans import Translator         # to translate text
import pyttsx3                             # to convert text to speech
import pyperclip                           # to read text from clipboard
import keyboard                            # to listen to key presses
from plyer import notification             # to generate text in notification area
import pandas as pd                        # to create dataframe for translated text
import os.path                             # to use OS dependent functionality

### 1) Set parameters
translator = Translator()                  # create object instance of the Translator class
from_lang = 'en'                           # source language
to_lang = 'hu'                             # destination language
words = []                                 # create empty list for translations
engine = pyttsx3.init()                    # init function to get an engine instance for the speech synthesis
engine.setProperty('rate',160)             # speech rate: words per minute
engine.setProperty('volume',1)             # volume: float from 0.0 to 1.0 
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # voice based on what languages are installed on OS 
outfile = 'dictionary.csv'                 # create csv file to write the output 

### 2) Define functions
# 2.1) Function to convert text to speech 
def say_it():                 
    word = pyperclip.paste()               # paste text from clipboard
    engine.say(word)                       # say pasted text
    engine.runAndWait()                    # blocks while processing all currently queued commands

# 2.2) Function to append translations to list of lists
def append(title, message):
    words.append([title, message])

# 2.3) Function to translate text
def translate_it():  
    word = pyperclip.paste()
    # translate word from source to destination language
    translation = translator.translate(word, src=from_lang, dest=to_lang)
    # generate notification
    notification.notify(title=word, message=translation.text)
    # call append function
    append(word, translation.text)                                       

### 3) Run translator and save translation history
# initiate infinite loop
while True: 
    if keyboard.is_pressed('*'):
        say_it()
    if keyboard.is_pressed('+'):
        translate_it()
    if keyboard.is_pressed('esc'):
        # create dataframe from list with 2 columns
        df = pd.DataFrame(words, columns = [from_lang, to_lang])
        
        # remove duplications before writing to file
        df.drop_duplicates(keep='first',inplace=True)           

        # if file exists append translations without headers to file
        if os.path.isfile(outfile) == True: 
            df.to_csv(outfile, mode='a', header=False, index=False)
            break
        # if file doesn't exist write translations with headers to file
        else:
            df.to_csv(outfile, mode='w', header=True, index=False)
            break