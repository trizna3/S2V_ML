# S2V_ML
Project sources for Machine Learning Course.

The data sets are not uploaded, due to their size.

Already pretrained vectors (s2v_reddit_2019_lg) can be found here https://github.com/explosion/sense2vec.

Corpus's I've used for my own training (enwiki-latest-abstract.xml.gz) can be found here https://dumps.wikimedia.org/enwiki/latest/.

Files (01_parse.py, 02_preprocess.py, 03_glove_build_counts.py, fastText/04_fasttext_train_vectors.py and 05_export.py) are **NOT** my own work. I've pulled them from https://github.com/explosion/sense2vec/tree/master/scripts and made minor changes to them, so i could run them on windows os.

Testing data can be found in input_model_scripts_eng/, testing_data_processed/ and testing_data_processed_paired/ directories.

The similarity computation is made in the SimilarityDict.py script.
