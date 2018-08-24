class IndianNameStemmer(StemmerI):
    def stem(self, token):
        newtup=list()
        for i in token:
            i = re.sub(r'(^\w{2,3}\. ?)', r'', i)
            i = re.sub(r'[^a-zA-Z]', '', i)
            i = re.sub(r'(\w)\1+',r'\1', i)
            i = i[:-2] if i.endswith(('bi', 'ji', 'so')) else i            
            i = i[:-3] if i.endswith(('bai', 'ben', 'beg', 'tai', 'sab', 'rao', 'rav', 'kha', 'lal', 'dev', 'deo')) else i
            i = i[:-4] if i.endswith(('bhai', 'bhau', 'sing', 'devi')) else i
            i = i[:-5] if i.endswith(('saheb', 'singh' , 'shing', 'kumar')) else i
            for r in (("tha", "ta"), ("gi", "ji"), ("bh", "b"), ("v", "w"), ("yu", "u"), ("gh", "g"),  
                      ("bh","b"), ("ph","f"),  ("gaw", "gaon"), ("ksh", "x"), ("z","j"), ("y", "i"), 
                      ("dh", "d"), ("sh", "s"), ("g","j"), ("i", "e"), ("a","") ):
                i = i.replace(*r)

            newtup.append(''.join(i for i, _ in itertools.groupby(i)))
        return tuple(newtup)
