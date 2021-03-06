import re
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer


def review_cleanup_labeled_data(review):
    """
    Pre-processing: Cleaning manually mention aspects and their sentiment score
    :param review: Each review for pre-processing
    :return: cleaned manually labeled data
    """
    rg_exp_main = r"\w+.*\[?[+/-]\d\]?\#\#|\w+.*\[?[+/-]\d\]\[\w+\]?\#\#"
    filter_review = re.sub(rg_exp_main, '', review)
    return filter_review


def review_cleanup_symbols(review_sentences):
    """
    Pre-processing: Cleaning symbols
    :param review_sentences:
    :return: filtered review after removing [#,{, }] symbols
    """
    reg_exp_main = re.compile('[^A-Za-z0-9^\n^\.^\"^\'^\- ]+', re.IGNORECASE | re.DOTALL)
    # review_filtered_main = re.findall(reg_exp_main, sentences)
    review_filtered_main = re.sub(reg_exp_main, '', review_sentences)
    return review_filtered_main


def sentence_tokenize_of_review(reviews):
    """
    Sentence Tokenization
    :param reviews: List of reviews
    :return: List of sentence after sentence tokenization
    """
    return sent_tokenize(reviews)


def word_tokenize_review(sentence_list):
    """
    Word Tokenization
    :param sentence_list: List of sentences
    :return: list of sentences tokenized into word
    """
    ids_tokenize_value = []
    for sent_id, review_id, sentences in sentence_list:
        sent_id = sent_id
        review_id = review_id
        word_tokenize_sent = word_tokenize(sentences)
        combine_value = (review_id, sent_id, word_tokenize_sent)
        ids_tokenize_value.append(combine_value)
    return ids_tokenize_value


def lemmatization_sentence(sentence):
    """
    Lemmatization: Normalizing words as many variations of words carry same meaning
    :param sentence: List of sentences
    :return: List of sentence after lemmatization
    """
    sentence_after_lemmatization = []
    lemmatizer = WordNetLemmatizer()
    for words in sentence.split():
        lemma_word = lemmatizer.lemmatize(words)
        sentence_after_lemmatization.append(lemma_word)
    return ' '.join(sentence_after_lemmatization)


def filter_stopwords(candidate_aspect_list):
    """
    Filter Stopwords - (English)
    :param candidate_aspect_list: List of candidate aspect list
    :return: candidate aspect list after filtering stopwords
    """
    stop_words = set(stopwords.words('english'))
    new_list = ('(', ')', '.', '-', '--', '``', "'", '"', "ha", "wa", "lot")
    stop_words.update(new_list)
    aspect_list_without_stopwords = []
    for sent_id, review_id, words in candidate_aspect_list:
        product_aspect = []
        for w in words:
            if w not in stop_words and w != '' and len(w) > 1:
                product_aspect.append(w)
        if product_aspect:
            aspect_per_sent_after_stopwords = (sent_id, review_id, product_aspect)
            aspect_list_without_stopwords.append(aspect_per_sent_after_stopwords)
    return aspect_list_without_stopwords


def lemmatization(aspect_list):
    """
    Lemmatization: Normalizing words as many variations of words carry same meaning
    :param aspect_list: aspect list to lemmatization
    :return: combination of product aspect that has the same meaning
    """
    product_aspect_list_after_lemmatization = []
    lemmatizer = WordNetLemmatizer()
    for words in aspect_list:
        lemma_word = lemmatizer.lemmatize(words)
        if lemma_word not in product_aspect_list_after_lemmatization:
            product_aspect_list_after_lemmatization.append(lemma_word)
    return product_aspect_list_after_lemmatization


def get_synonyms_set(aspect_list):
    """
    Synonyms Matching
    :param aspect_list: Aspect list for synonyms resolution
    :return: aspect list after synonyms resolution
    """
    product_aspects_dictionary = {}
    noun_list_replacing_space = []
    for noun, count in aspect_list:
        rg_exp_replace_space = re.compile('(\\s+)', re.IGNORECASE | re.DOTALL)
        noun_list_replacing_space_with_underscore = re.sub(rg_exp_replace_space, '_', noun)
        new_noun_count_pair = (noun_list_replacing_space_with_underscore, count)
        noun_list_replacing_space.append(new_noun_count_pair)

    for noun, count in aspect_list:
        synonyms = []
        for syn in wordnet.synsets(noun):
            for lemma in syn.lemmas():
                synonyms.append(lemma.name())

        if synonyms:
            for nn, cc in noun_list_replacing_space:
                if nn in synonyms:
                    noun_count_pair = (nn, cc)
                    replace_value = (noun, cc)
                    noun_list_replacing_space[noun_list_replacing_space.index(noun_count_pair)] = replace_value

    # print(len(noun_list), noun_list)
    for noun, count in noun_list_replacing_space:
        if noun in product_aspects_dictionary:
            product_aspects_dictionary[noun] = (product_aspects_dictionary[noun]) + count
        else:
            product_aspects_dictionary[noun] = count

    product_aspect = sorted(product_aspects_dictionary.items(), key=lambda x: x[1], reverse=True)
    return product_aspect