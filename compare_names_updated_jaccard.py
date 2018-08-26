import pandas as pd
import numpy as np
import itertools, re
from nltk.stem import StemmerI
from nltk.metrics import edit_distance
import nltk

from sklearn.feature_extraction import FeatureHasher
from sklearn.metrics import jaccard_similarity_score

hasher=FeatureHasher(input_type="string", n_features=25, dtype=np.int32)

class IndianNameStemmer(StemmerI):
    def stem(self, token):
        newtup=list()
        for i in token:
            i = re.sub(r'\([^)]*\)', '', i).strip()
            i = re.sub(r'\[[^)]*\]', '', i).strip()
            i = re.sub(r'(^\w{1,3}\. ?)', r'', i)
            i = i.split('.')[0]
            i = i.split('-')[0]
            i = re.sub(r'[^a-zA-Z]', '', i)
            i = re.sub(r'(\w)\1+',r'\1', i)
            i = i[:-2] if i.endswith(('bi', 'ji', 'so')) else i            
            i = i[:-3] if i.endswith(('bai', 'ben', 'beg', 'tai', 'sab', 'rao', 'rav', 'kha', 'lal', 'dev', 'deo')) else i
            i = i[:-4] if i.endswith(('bhai', 'bhau', 'sing', 'devi')) else i
            i = i[:-5] if i.endswith(('saheb', 'singh' , 'shing', 'kumar')) else i
            for r in (("tha", "ta"), ("krish", "krush"), ("gi", "ji"), ("bh", "b"),  ("yu", "u"), ("gh", "g"),  
                      ("bh","b"), ("ph","f"),  ("gaw", "gaon"), ("ksh", "x"), 
                      ("dh", "d"), ("sh", "s") ):
                # ("g","j"), ("o", "u"), ("i", "e"), ("m", "n"),  ("y", "i"), ("v", "w"), ("z","j"),, ("a","")
                i = i.replace(*r)

            newtup.append(''.join(i for i, _ in itertools.groupby(i)))
        return tuple(newtup)



s = IndianNameStemmer()
s.stem([ 'm.sattar', 'bhimrav'])

df=pd.read_excel('correct.xlsx')
df.columns=['wrong', 'correct']

def mytrigrams(mys):
    try:
        shingles=["".join(i) for i in nltk.trigrams([c for c in mys])]
        return hasher.transform([shingles]).toarray()
    except:
        return np.array(())

df['wrong_trigram'] = df['wrong'].apply(mytrigrams)
df['correct_trigram'] = df['correct'].apply(mytrigrams)

mylist=list()
for i, rows in df.iterrows():
    try:
        mylist.append(jaccard_similarity_score(rows['wrong_trigram'][0], rows['correct_trigram'][0]))
    except:
        mylist.append(np.inf)
        
df['jaccard'] = mylist

df['updated']=df['wrong'].astype(str).apply(lambda x: x.split('/')).apply(s.stem)
df['updated1']=df['correct'].astype(str).apply(lambda x: x.split('/')).apply(s.stem)

mylist=list()
mylist1=list()
for i, rows in df.iterrows():
    mylist.append(edit_distance(rows['updated'][0], rows['updated1'][0] , substitution_cost=1, transpositions=True))
    mylist1.append(edit_distance(str(rows['wrong']), str(rows['correct']), substitution_cost=1, transpositions=True))

df['edu1'] = mylist
df['wc'] = mylist1

#pd.concat([df.edu1.value_counts(), df.wc.value_counts()], axis=1)

df['tally']=df.wrong.str[:1] == df.correct.str[:1]

df['diff'] = df['wc'] - df['edu1']

ndf=df[~((df['edu1'] > 3) & (df['wc'] > 5) & (df['tally'] == 0) & (df['diff'] < 4) )]
ndf=ndf[~( ((ndf['edu1'] > 2) & (ndf['wc'] > 4) ) &  (df['tally'] == 1)  )]
ndf=ndf[~( ((ndf['edu1'] > 3)  | (ndf['wc'] > 3) ) &  (df['tally'] == 0)  )]

tdf=df.merge(ndf, how='outer', left_index=True, right_index=True, indicator=True)
tdf=tdf[tdf._merge == 'left_only']

tdf.to_excel('tdf.xlsx')

#ndf=ndf[np.logical_and(np.logical_and((ndf['edu1'] > 3) , (ndf['wc'] > 5)),  (ndf['tally'] == 0 ))]

#ndf['ulen'] = ndf['updated'].str[0].apply(len)
#ndf = ndf.sort_values('ulen')

ndf.to_excel('to_study1.xlsx')
_____

from io import StringIO

myst="""shantanu prabhakar oka, 905034 , 19:44   
sammeer annashaaheb goankar, 905094  , 19:33
paravatibai vittal shelke,  905154 ,   21:56
"""
u_cols=['name', 'my_index', 'current_tm']

myf = StringIO(myst)
import pandas as pd
df = pd.read_csv(StringIO(myst), sep=',', names = u_cols)

myst="""shantanu34 prabakar oka, 905034 , 19:44   
sammir anashaheb goankar, 905094  , 19:33
parwati vithal bholke,  905154 ,   21:56
 anashaheb  gavkar, 905094  , 19:33

"""
u_cols=['name', 'my_index', 'current_tm']

myf = StringIO(myst)
import pandas as pd
df1 = pd.read_csv(StringIO(myst), sep=',', names = u_cols)

df['updated']=df['name'].astype(str).apply(lambda x: x.split()).apply(s.stem).apply(sorted).apply(tuple)
df1['updated1']=df1['name'].astype(str).apply(lambda x: x.split()).apply(s.stem).apply(sorted).apply(tuple)

df.merge(df1, how='outer', left_on=['updated'], right_on=['updated1'], indicator=True)

mylist=list()
for i, rows in df.iterrows():
        for i1, rows1 in df1.iterrows():
            #mylist.append(edit_distance(rows['updated'], rows1['updated1'], substitution_cost=2))
            #print (rows['updated'], rows1['updated1'], edit_distance(rows['updated'], rows1['updated1'], substitution_cost=2))
            s1, s2 = " ".join(list(rows['updated'])), " ".join(list(rows1['updated1']))  
            final=list()
            for i in s1.split():
                mylisti=list()
                for k in s2.split():
                    mylisti.append(edit_distance(i, k, transpositions=True))
                    #print (i,k,  edit_distance(i, k, transpositions=True) )
                final.append(min(mylisti))
            mylist.append(sum(final))
            
            
fdf = pd.merge(df.assign(key=0), df1.assign(key=0), on='key').drop('key', axis=1)
fdf['eud'] = mylist

gdf=fdf.groupby(['name_x'])['eud'].min()
gdf=gdf.reset_index()
gdf.merge(fdf, how='left', left_on=['name_x', 'eud'], right_on=['name_x', 'eud'])
