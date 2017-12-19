from nltk import pos_tag, word_tokenize
import os, database, StanfordNLPServer

import config
from nltk.internals import find_jars_within_path
from nltk.tag.stanford import StanfordPOSTagger

# POS tagging
def pos_tagging(tokenized_sentence_list):
    """
    :param tokenized_sentence_list: word tokenize consumer review
    :return: List of word with POS tagging
    """
    ids_pos_value = []
    for review_id, sent_id, sentences in tokenized_sentence_list:
        review_id = review_id
        sent_id = sent_id
        pos_tagged = pos_tag(sentences)
        combine_value = (review_id, sent_id,pos_tagged)
        ids_pos_value.append(combine_value)
    return ids_pos_value


# Standford POS Tagging
def stanford_pos_tagging(sentence_list):
    ids_pos_value = []
    for sent_id, review_id, sentences in sentence_list:
        nlpServer = StanfordNLPServer.SNLPServer()
        pos_tagged = getattr(nlpServer, 'pos')
        combine_value = (sent_id, review_id, pos_tagged(sentences))
        ids_pos_value.append(combine_value)
    database.insert_postagged_sent_into_db(ids_pos_value)
