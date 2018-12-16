import os
from gensim import corpora, models, similarities
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
TEMP_FOLDER = os.getcwd()+"\\temp"
print('Folder "{}" will be used to save temporary dictionary and corpus.'.format(TEMP_FOLDER))


dictionary = corpora.Dictionary.load(os.path.join(TEMP_FOLDER, 'deerwester.dict'))
corpus = corpora.MmCorpus(os.path.join(TEMP_FOLDER, 'deerwester.mm')) # comes from the first tutorial, "Corpora and Vector Space"
print(corpus)
lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=2)

doc = "Human computer interaction"
vec_bow = dictionary.doc2bow(doc.lower().split())
vec_lsi = lsi[vec_bow] # convert the query to LSI space
print(vec_lsi)

index = similarities.MatrixSimilarity(lsi[corpus]) # transform corpus to LSI space and index it
# index2 = similarities.Similarity(corpus=lsi[corpus],num_features=12,output_prefix="Test") # transform corpus to LSI space and index it,memory friendly

index.save(os.path.join(TEMP_FOLDER, 'deerwester.index'))
# index2.save(os.path.join(TEMP_FOLDER, 'deerwester2.index'))
index = similarities.MatrixSimilarity.load(os.path.join(TEMP_FOLDER, 'deerwester.index'))
#index2 = similarities.Similarity.load(os.path.join(TEMP_FOLDER, 'index'))

sims = index[vec_lsi] # perform a similarity query against the corpus
print(list(enumerate(sims))) # print (document_number, document_similarity) 2-tuples

sims = sorted(enumerate(sims), key=lambda item: -item[1])
print(sims) # print sorted (document number, similarity score) 2-tuples