'''
Script for computing similarities between entity sets, using vectors from Sense2Vec.

Adam Trizna
'''

from sense2vec import Sense2Vec
import ErParser

# s2v = Sense2VecComponent(nlp.vocab).from_disk("exported")
# s2v2 = Sense2VecComponent(nlp.vocab).from_disk("../pretrainedVectors/redditComments2019\s2v_reddit_2019_lg")
# s2v3 = Sense2VecComponent(nlp.vocab).from_disk("../pretrainedVectors/s2v_old")

s2v = None
total_passed = 0
total_paired = 0

def getVectorsDistance(word1, word2):
    '''
    If both given words are in the vocabulary, returns normalized euclidian distance of their corresponding vectors.
    '''
    global s2v
    if s2v == None:
        # Vector files are not present in the repository
        s2v = Sense2Vec().from_disk("C:\SKOLA\machine_learning\Project\pretrainedVectors\s2v_reddit_2019_lg")
        # s2v = Sense2Vec().from_disk("C:\SKOLA\machine_learning\Project\wiki corpus/backup/exported")

    if word1 in s2v and word2 in s2v:
        return s2v.similarity(word1, word2)
    return 0

def compute(processed_file_name, treshold):
    '''
    Given textfile contains info about two to-be-compared ER models.
    Computes similarity for each of the entity_set pairs. Checks wether their similarity pass the threshold.
    '''
    entity_set_names1, entity_set_attributes1, entity_set_names2, entity_set_attributes2, paired_entity_sets = parse(processed_file_name)
    passed_threshold = 0
    for es1_key in entity_set_names1.keys():
        for es2_key in entity_set_names2.keys():
            es1_name = entity_set_names1[es1_key]
            es1_attributes = entity_set_attributes1[es1_key]
            es2_name = entity_set_names2[es2_key]
            es2_attributes = entity_set_attributes2[es2_key]
            rate = compute_similarity_rate(es1_name,es1_attributes,es2_name,es2_attributes)
            if ([es1_key,es2_key] in paired_entity_sets):
                if (rate > treshold):
                    passed_threshold += 1
    global total_passed
    global total_paired
    total_paired += len(paired_entity_sets)
    total_passed += passed_threshold

def compute_similarity_rate(es1_name,es1_attrs,es2_name,es2_attrs):
    similarity_measure = getSimilarity(es1_name,es2_name)
    for attr1 in es1_attrs:
        for attr2 in es2_attrs:
            similarity_measure += getSimilarity(attr1,attr2)
    similarity_measure /= (1 + len(es1_attrs)*len(es2_attrs))
    return similarity_measure

def getSimilarity(word1,word2):
    tags = ["|NOUN","|VERB","|ADJ"]
    similarities = []
    for t1 in tags:
        for t2 in tags:
            similarities.append(getVectorsDistance(word1+t1, word2+t2))

    return max(similarities)

def parse(processed_file_name):
    '''
    Parses files, created in ErParser.
    Creates dict objects for later similarity computation.
    '''
    entity_set_names1 = dict()
    entity_set_attributes1 = dict()
    entity_set_names2 = dict()
    entity_set_attributes2 = dict()
    paired_entity_sets = list()
    file = open(processed_file_name, 'r')
    delimiters_count = 0
    for row in file:
        if "=" in row:
            delimiters_count += 1
            continue
        if delimiters_count == 0:
            row = row.split(":")
            entity_set_names1[int(row[0].strip())] = row[1].strip()
            entity_set_attributes1[int(row[0].strip())] = row[2].strip().split(",")
        elif delimiters_count == 1:
            row = row.split(":")
            entity_set_names2[int(row[0].strip())] = row[1].strip()
            entity_set_attributes2[int(row[0].strip())] = row[2].strip().split(",")
        else:
            row = row.split("-")
            paired_entity_sets.append([int(row[0].strip()), int(row[1].strip())])
    file.close()

    return entity_set_names1,entity_set_attributes1,entity_set_names2,entity_set_attributes2,paired_entity_sets

for model in ErParser.get_model_names():
    for i in [1,2]:
        compute("testing_data_processed_paired/" + model + "_student" + str(i) + "_processed.txt", 0.3)

print(str(total_passed) + " out of " + str(total_paired) + " passed the threshold")
