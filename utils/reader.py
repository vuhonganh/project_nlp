"""
reader.py: process input sentence and extract important information
"""
import nltk
GO = "GO"
TURN = "TURN"
UNK = "UNK"

class Reader:
    """
    Each time reads in one sentence text and return 3 intents GO, TURN, UNK
    """

    def __init__(self, synonym_file="../data/small_synonyms.txt",debug=False):
        self.syn_dict = read_small_synonyms(synonym_file)
        self.debug = debug
        self.cur_intent = None
        self.specs = {}
    def _preprocess(self, text):
        """
        remove "can you", "please" and punctuation from text string and replace synonym
        :param text: input as whole text string
        :return: text preprocessed as list
        """
        # nltk helps separate punctuation from word (e.g. please? -> please ?)
        text_list = nltk.word_tokenize(text.lower())
        to_removes = ('please', 'can', 'could', 'you', '.', '!', '?')
        res = [t for t in text_list if t not in to_removes]
        res = replace_syn(res, self.syn_dict)
        return res

    def _read_tags(self, words_tags):
        """
        
        :param words_tags: 
        :return: 
        """
        # turn: VB - CD - NN - TO - PRP$ - NN
        # turn: VB - CD - NN - TO - DT - NN
        turn_possible = ["CD NN TO PRP$ NN",
                         "CD NN TO DT NN"]  # omit the first verb
        if self.cur_intent == TURN:
            cur_tags = " ".join(wt[1] for wt in words_tags[1:])
            if cur_tags not in turn_possible:
                self.cur_intent = UNK
                return
            else:
                # if not left or right at the end -> UNK
                turn_right = 1
                if words_tags[-1][0] == "left":
                    turn_right = -1
                elif words_tags[-1][0] != "right":
                    self.cur_intent = UNK
                    return
                self.specs["degree"] = int(words_tags[1][0]) * turn_right
        elif self.cur_intent == GO:
            #TODO
            pass




    def read(self, text):
        text_list = self._preprocess(text)
        """
        this text_list will have to get the intents: GO TURN OR UNK
        if GO: check if go to point, otherwise go fwd or bwd 
        if TURN: check if 
        """
        if text_list[0] == "go":
            self.cur_intent = GO
        elif text_list[0] == "turn":
            self.cur_intent = TURN
        else:
            self.cur_intent = UNK
            return

        specs = {}
        if self.cur_intent == GO:
            # check if go to point
            if "to" in text_list:
                dests_list = read_all_parentheses(text)
                if len(dests_list) == 0:
                    self.cur_intent = UNK
                else:
                    specs["dests_list"] = dests_list
            else:
                # POS tag goes here:
                words_tags = nltk.pos_tag(text_list)  # get a list of tuple (w, t)
                for w, t in words_tags[1:]:  # skip the first word which is "go" or "turn"
                    #TODO
                    pass



def read_small_synonyms(syn_file="../data/small_synonyms.txt"):
    """
    build a dict from synonym -> its represent word (first word in file)
    :param syn_file: file contains synonym by line
    :return: dict maps synonym -> its represent word
    """
    res = {}
    with open(syn_file) as f:
        for line in f:
            line.strip()  # remove white spaces at the start and the end of line
            if not line:
                continue
            ws = line.split()  # split by white spaces
            val = ws[0]
            res.update({key: val for key in ws})
    return res


def read_all_parentheses(in_text):
    """
    read all parentheses in the in_text
    :param in_text: the input text that can have more than one (x, y)
    :return: list of [(x, y)] if any, otherwise return empty list
    """
    res = []
    while True:
        id_end = in_text.find(')')
        id_start = in_text.find('(')
        if id_start == -1 or id_end == -1 or id_start > id_end:
            break
        cur_pos = read_coordinates(in_text[id_start + 1: id_end])
        if cur_pos is not None:
            res.append(cur_pos)
        in_text = in_text[id_end + 1:]

    return res


def read_coordinates(in_parenthese):
    """
    read coordinate x, y in in_paranthese
    :param in_parenthese: the text inside "(...)"
    :return: x, y in float form
    """
    if ',' not in in_parenthese:
        print('wrong syntax: must use comma to separate coordinates')
        return None
    else:
        elems = in_parenthese.strip().split(',')
        if len(elems) != 2:
            print('wrong syntax: only support 2D coordinates')
            return None
        else:
            try:
                return int(float(elems[0])), int(float(elems[1]))
            except ValueError as er:
                print('invalid coordinates format: ', er)
                return None


def replace_syn(line_list, syn_dict):
    """
    Replace synonyms in text_line by its values
    :param line_list: list of input tokens
    :param syn_dict: the synonym dict
    :return: syn_text_list: the line with representative synonym 
    """
    res = []
    for t in line_list:
        if t in syn_dict.keys():
            res.append(syn_dict[t])
        else:
            res.append(t)
    return res





def test_read_parentheses():
    text_inputs = ['go to point (23, 45)',
                   'go to point (2, 34, 5)',
                   'go to point ()',
                   'go to point (0,',
                   'go to point (0. 12, 2.54)',
                   'go to point ((0, 1)',
                   'go to point (0, 1) then go to point (2, 3)'
                   ]
    for i in text_inputs:
        print(read_all_parentheses(i))


def test_read_synonyms():
    syn_dict = read_small_synonyms()
    line_list = 'go 50 degrees to your left-side'.split()
    out_list = replace_syn(line_list, syn_dict)
    print(nltk.pos_tag(out_list))


if __name__ == '__main__':
    # test_read_parentheses()
    test_read_synonyms()
