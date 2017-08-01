import os
import pickle
import copy
import numpy as np
from itertools import islice
import linecache


CODES = {'<PAD>': 0, '<EOS>': 1, '<UNK>': 2, '<GO>': 3 }


def load_data(source_path, target_path, indexes, preprocess):
    """
    Load Dataset from File
    """
    source = []
    target = []
    for i in indexes:
        source_line = linecache.getline(source_path, i)
        if 0 < len(source_line.split(' ')) < 15:
            source.append(preprocess(source_line))
            target_line = linecache.getline(target_path, i)
            target.append(preprocess(target_line))
    return source, target


def preprocess(text):
    text = text.lower()
    text = text.replace('\n', '')
    tokens = """()?!.,:'";'*%$&´`<>-#/|\\"""

    for token in tokens:
        text = text.replace(token, '')
    return text

def process(source_text, target_text, text_to_ids):
    """
    Process Text Data.  Save to to file.
    """
    #source_text, target_text = preprocess(source_text, target_text)

    source_vocab_to_int, source_int_to_vocab = create_lookup_tables(source_text)
    target_vocab_to_int, target_int_to_vocab = create_lookup_tables(target_text)

    source_text, target_text = text_to_ids(source_text, target_text, source_vocab_to_int, target_vocab_to_int)
    
    return source_text, target_text, source_vocab_to_int, target_vocab_to_int, source_int_to_vocab, target_int_to_vocab


def save_data(source_text, target_text, source_vocab_to_int, target_vocab_to_int, source_int_to_vocab, target_int_to_vocab):
    # Save Data
    with open('preprocess.p', 'wb') as out_file:
        pickle.dump((
            (source_text, target_text),
            (source_vocab_to_int, target_vocab_to_int),
            (source_int_to_vocab, target_int_to_vocab)), out_file)


def load_preprocess():
    """
    Load the Preprocessed Training data and return them in batches of <batch_size> or less
    """
    with open('preprocess.p', mode='rb') as in_file:
        return pickle.load(in_file)


def create_lookup_tables(text):
    """
    Create lookup tables for vocabulary
    """
    vocab = set([w for l in text for w in l.split()])
    vocab_to_int = copy.copy(CODES)

    for v_i, v in enumerate(vocab, len(CODES)):
        vocab_to_int[v] = v_i

    int_to_vocab = {v_i: v for v, v_i in vocab_to_int.items()}

    return vocab_to_int, int_to_vocab


def save_params(params):
    """
    Save parameters to file
    """
    with open('params.p', 'wb') as out_file:
        pickle.dump(params, out_file)


def load_params():
    """
    Load parameters from file
    """
    with open('params.p', mode='rb') as in_file:
        return pickle.load(in_file)


def batch_data(source, target, batch_size):
    """
    Batch source and target together
    """
    for batch_i in range(0, len(source)//batch_size):
        start_i = batch_i * batch_size
        source_batch = source[start_i:start_i + batch_size]
        target_batch = target[start_i:start_i + batch_size]
        yield np.array(pad_sentence_batch(source_batch)), np.array(pad_sentence_batch(target_batch))


def pad_sentence_batch(sentence_batch):
    """
    Pad sentence with <PAD> id
    """
    max_sentence = max([len(sentence) for sentence in sentence_batch])
    return [sentence + [CODES['<PAD>']] * (max_sentence - len(sentence))
            for sentence in sentence_batch]
