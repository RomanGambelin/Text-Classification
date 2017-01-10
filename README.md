#Text-Classification
Text treatment and machine learning in Python :

The aim is to classify sementicaly a set of texts in k groups.

Files :
- TextClass.py : python code
- 20_newsgroups : folder divided in 20 sub-folders (each one correspond to a group) containing a total of approximatively 20,000 texts (netnews)

You can obtain the folder "20_newsgroups" by downloading the original data "20news-19997.tar.gz" on http://qwone.com/~jason/20Newsgroups/ and decompressing it.

Method :
- Import of the whole texts using glob module
- Normalization of the texts (transforming them into a list a relevant words)
- Computation of the TF-IDF of each word in each text (= (frequency of a word in a text) * log( number of texts / number of texts where the word appears) )
- Selection of the most relevant words of the corpus and transformation of the texts into relevant words frequencies vectors
- Definition of k random frequencies vectors (taken among the texts by example) called the "mobile centers" and association of a group (corresponding to the mobile centers) to each text using cosine similarity then computing the mean frequencies vectors of each group as new mobile centers and iterate (method of the k-means)

To use the code, just write the folder containing the texts folder "20_newsgroups" at the indicated location (l. 34) and run the source.
!! It takes about 20mn to classify efficently the texts into 20 groups !!

N.B. : The code is commented in french
