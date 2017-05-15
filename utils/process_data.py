import numpy as np

DATA_PATH = '../data/'
DEFAULT_DIM = 50
DEFAULT_FILE = DATA_PATH + 'glove.6B.' + str(DEFAULT_DIM) + 'd.txt'


def load_selected(tokens_to_idx, file=DEFAULT_FILE, dim=DEFAULT_DIM):
    """
    build dict tokens -> word vectors
    :param tokens_to_idx: dict word -> its index 
    :param file: glove file that store word-vectors
    :param dim: dimension of word-vectors
    :return: 2d np array: tokens_idx -> word vectors    
    """
    words_vecs = np.zeros((len(tokens_to_idx), dim))
    with open(file) as f:
        for line in f:
            line = line.strip()  # remove white space at beginning and at the end of line
            if not line:
                continue
            row = line.split()
            token = row[0]  # token is the first element of row
            if token in tokens_to_idx:
                vec = [float(e) for e in row[1:]]
                if len(vec) != dim:
                    raise RuntimeError('dimensions do not match')
                words_vecs[tokens_to_idx[token]] = np.asarray(vec)

    return words_vecs


def build_dict(file=DEFAULT_FILE, dim=DEFAULT_DIM):
    """
    load all glove to memory, for dim=50 it's only 165 mb
    :param file: glove file that store word-vectors
    :param dim: dimension of word-vectors
    :return: dict all vocab in glove -> word vectors
    """
    dict_all = {}
    with open(file) as f:
        for line in f:
            line = line.strip()  # remove white space at beginning and at the end of line
            if not line:
                continue
            row = line.split()
            token = row[0]  # token is the first element of row
            vec = [float(e) for e in row[1:]]
            if len(vec) != dim:
                raise RuntimeError('dimensions do not match')
            dict_all[token] = np.asarray(vec)

    return dict_all


def test_load():
    small_vocab = ['go', 'turn', 'move', 'run', 'right', 'left', 'the', '!', '.', 'meter']
    small_dict = {x: i for (i, x) in enumerate(small_vocab)}
    word_vecs = load_selected(small_dict)
    print(word_vecs)


if __name__ == '__main__':
    test_load()
