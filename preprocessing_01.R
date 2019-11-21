this is a R script for processing frequencies for latin texts
#following the instructions from Eder et al. (2016): Stylometry with R
#it is needed to use the imposters() function

library(stylo)

#load the prepared corpus where all the files are gathered
#you need to rename the corpus.dir
raw.corpus <- load.corpus(files = "all", corpus.dir = "ENTER DIR HERE", encoding = "UTF-8")

#tokenizing the corpus of the latin text
tokenized.corpus <- txt.to.words.ext(raw.corpus, corpus.lang = "Latin.all", preserve.case = FALSE)

#creating 3char-grams
corpus.char.3.grams <- txt.to.features(tokenized.corpus, ngram.size = 3,features = "c")

#for gathering the frequency list, I built a frequency table from the xxx MFF
#here it's wise to use 1000 MFF, because some texts are really short.
frequent.features <- make.frequency.list(corpus.char.3.grams, head = 1000)
freqs <- make.table.of.frequencies(corpus.char.3.grams, features = frequent.features)

imposters(freqs, distance ="cosine")
#for a more precise analysis, define text-to-be-tested 
#imposters(reference.set = freqs[-c(<rownumber where doc is>),] , test = freqs[<rownumber where doc is>, ])

#optional
imposters.optimize(freqs)

#write the freqs into a csv-file named freqs
write.csv2(freqs,"freqs.csv") 
