# easystemmer
#Stemmer for Indian Names

from easystemmer import IndianNameStemmer
import pandas as pd

s = IndianNameStemmer()
#s.stem(['savithabai'])

df=pd.read_excel('my_file.xlsx')
df.columns=['wrong', 'correct']

df['updated']=df['wrong'].astype(str).apply(lambda x: x.split()).apply(s.stem)
df['updated1']=df['correct'].astype(str).apply(lambda x: x.split()).apply(s.stem)

ndf=df[df['updated'] != df['updated1']]
ndf[['wrong', 'correct']].to_excel('to_study.xlsx')
