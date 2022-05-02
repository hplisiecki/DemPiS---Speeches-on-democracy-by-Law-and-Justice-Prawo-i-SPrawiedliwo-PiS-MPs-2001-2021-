from bs4 import BeautifulSoup
from pyMorfologik import Morfologik
from pyMorfologik.parsing import ListParser
import os
from tqdm import tqdm
import pandas as pd
import re

parser = ListParser()
stemmer = Morfologik()



clean_dir = '' # directory where the raw files are stored

with open('lemmatizer_dictionary.pickle', 'rb') as handle:
    lema_dict = pickle.load(handle)



def stem(sentence):

    morf = stemmer.stem([sentence.lower()], parser)
    string = ''
    for i in morf:
        if i[0] in lema_dict.keys():
            string += lema_dict[i[0]] + ' '
        else:
            try:
                string += list(i[1].keys())[0] + ' '
            except:
                print(morf)
                string += i[0] + ' '
    string = string[:-1]

    return string

stop = False
collate = []
for file_one in tqdm(os.listdir(clean_dir)):
    for file_two in os.listdir(os.path.join(clean_dir, file_one)):
        for file_three in os.listdir(os.path.join(clean_dir, file_one, file_two)):
            for file_four in os.listdir(os.path.join(clean_dir, file_one, file_two, file_three)):
                filename = file_one + '/' + file_two + '/' + file_three + '/' + file_four

                if filename in list(corpus.file):
                    with open(os.path.join(clean_dir, filename), encoding='utf8') as f: # open in readonly mode
                        html = BeautifulSoup(f, "html.parser")
                        text = html.getText()                               # read the clean texts

                        stemmed = stem(text)                                # stem the text
                        stemmed = stemmed.replace('\t', ' ')                # remove tabs
                        stemmed = stemmed.replace('  ', ' ')                # remove double spaces
                        collate.append(stemmed)                             # append to collate

# save to csv
df = pd.DataFrame(collate)

directory = ''  # directory to save the csv file
df.to_csv(directory, index=False)



# count demok occurences

import pandas as pd

corpus = pd.read_csv(directory)

demok_counts = []
for speech in corpus.text:
    demok_counts.append(speech.count('demok'))
    speech = speech.replace('\n\n', ' ')


corpus['demok_counts'] = demok_counts

demok = corpus[corpus.demok_counts > 2]
pisdemok = demok[demok.klub == 'PiS']

pisdemok.to_csv(directory)
