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
    :return: all_words_vecs: all words in vector form, (a 2D np array) 
             all_words_list: idx -> word
             words_idx_dict: word -> idx
                 
    """
    all_words_vecs = []
    all_words_list = []
    words_idx_dict = {}
    idx = 0
    with open(file) as f:
        for line in f:
            line = line.strip()  # remove white space at beginning and at the end of line
            if not line:
                continue
            row = line.split()
            word = row[0]  # word is the first element of row
            vec = [float(e) for e in row[1:]]
            if len(vec) != dim:
                raise RuntimeError('dimensions do not match')
            all_words_vecs.append(vec)
            all_words_list.append(word)
            words_idx_dict[word] = idx
            idx += 1

    all_words_vecs = np.asarray(all_words_vecs)
    norm = np.sqrt(np.sum(np.square(all_words_vecs), axis=1))
    all_words_vecs = all_words_vecs / norm[:, None]  # normalized glove
    return all_words_vecs, all_words_list, words_idx_dict


def closest_words(input_list, word_vecs, word_list, word_dict, n=10):
    """
    return n closest words to each word in list_words
    :param input_list: words that we want to find closest words
    :param word_vecs: vector form of all words 
    :param word_list: idx -> word
    :param word_dict: word -> idx
    :param n: number of closest words that we want to find
    :return: list of lists containing closest words for each word in list_words 
    """
    input_idx = [word_dict[w] for w in input_list if w in word_dict.keys()]
    closest_ws = []
    closest_dsts = []
    for i in range(len(input_idx)):
        cur_word = word_vecs[input_idx[i]]
        cos_dist = 1.0 - np.dot(word_vecs, cur_word)
        n_closest_idx = np.argsort(cos_dist)[:n+1]
        n_closest_dst = cos_dist[n_closest_idx]
        closest_ws.append([word_list[idx] for idx in n_closest_idx])
        closest_dsts.append(n_closest_dst)
    return closest_ws, closest_dsts


def test_load_selected():
    small_vocab = ['go', 'turn', 'move', 'run', 'right', 'left', 'the', '!', '.', 'meter']
    small_dict = {x: i for (i, x) in enumerate(small_vocab)}
    word_vecs = load_selected(small_dict)
    print(word_vecs)


def test_build():
    word_vecs, word_list, word_dict = build_dict()
    small_list = ['be', 'go', 'turn', 'move', 'run', 'right', 'left', 'at', 'the', '!', '.', 'meter']
    ws, ds = closest_words(small_list, word_vecs, word_list, word_dict)
    for i in range(len(ws)):
        print(ws[i])
        print(ds[i])

if __name__ == '__main__':
    # test_load_selected()
    # build_dict()
    test_build()
