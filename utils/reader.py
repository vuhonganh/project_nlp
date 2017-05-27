#TODO: create GOTO intent

"""
reader.py: process input sentence and extract important information
"""
import nltk
GO = "GO"
TURN = "TURN"
UNK = "UNK"
"""
turn: VB - CD - NNS - TO - PRP$ - NN (e.g. turn 50 degrees to your left)
turn: VB - CD - NNS - TO - DT - NN   (e.g. turn 50 degrees to the left-side)
"""
TURN_POSSIBLE = ["CD NNS TO PRP$ NN",
                 "CD NNS TO DT NN"]  # omit the first verb, singular -> plural

""" 
go: VB - RB - IN - CD - NNS       (e.g. go forward/backward for 50 metres)
go: VB - CD - NNS - RB            (e.g. go 50 metres backward/forward)
"""
GO_POSSIBLE = ["RB IN CD NNS",
               "CD NNS RB"]  # omit the first verb, singular -> plural (nltk reads meter as RB)


class Reader:
    """
    Each time reads in one sentence text and return 3 intents GO, TURN, UNK
    """
    def __init__(self, synonym_file="../data/small_synonyms.txt", debug=False):
        self.syn_dict = read_small_synonyms(synonym_file)
        self.debug = debug
        self.cur_intent = None
        self.specs = {}

    def _preprocess(self, text):
        """
        remove some redundant words and punctuation from text string and replace synonym
        :param text: input as whole text string
        :return: text preprocessed as list
        """
        # nltk helps separate punctuation from word (e.g. please? -> please ?)
        text_list = nltk.word_tokenize(text.lower())
        to_removes = ('please', 'can', 'could', 'you', '.', '!', '?', 'straight')
        res = [t for t in text_list if t not in to_removes]
        res = replace_syn(res, self.syn_dict)
        return res

    def _read_tags(self, words_tags):
        """
        extract information (degree / meter) from words and its tags
        :param words_tags: list of tuple (word, tag) given from nltk.pos_tag()
        :return: None (this is a procedure that modify directly self.cur_intent) 
        """
        if self.cur_intent == TURN:
            self._read_TURN_long(words_tags)
        elif self.cur_intent == GO:
            self._read_GO_long(words_tags)
        return

    def _read_TURN_long(self, words_tags):
        cur_tags = " ".join(wt[1] for wt in words_tags[1:])
        if self.debug:
            print(cur_tags)
        if cur_tags not in TURN_POSSIBLE:
            self.cur_intent = UNK
            return
        else:
            # if not degree -> UNK:
            if words_tags[2][0] != "degrees":
                print("Only support angle in degree")
                self.cur_intent = UNK
                return
            # if not left or right at the end -> UNK
            turn_right = 1
            if words_tags[-1][0] == "left":
                turn_right = -1
            elif words_tags[-1][0] != "right":
                self.cur_intent = UNK
                return
            self.specs["degrees"] = int(words_tags[1][0]) * turn_right

    def _read_GO_long(self, words_tags):
        cur_tags = " ".join(wt[1] for wt in words_tags[1:])
        if self.debug:
            print(cur_tags)
        if cur_tags not in GO_POSSIBLE:
            print("not in go possible")
            self.cur_intent = UNK
        else:
            # if not meter -> UNK:
            if "meters" not in words_tags[2] and "meters" not in words_tags[4]:
                print("Only support distance in meter")
                self.cur_intent = UNK
                return
            # find the adverb (RB) in words_tags for GO: (there should be only 1 elem)
            direction = [wt[0] for wt in words_tags if wt[1] == "RB"]
            forward = 1
            if direction[0] == "backward":
                forward = -1
            elif direction[0] != "forward":
                print("Only support forward and backward direction")
                self.cur_intent = UNK
                return
            distance = [wt[0] for wt in words_tags if wt[1] == "CD"]
            self.specs["meters"] = int(distance[0]) * forward
            self.specs["goto"] = False

    def read(self, text):
        text_list = self._preprocess(text)
        """
        this text_list will have to get the intents: GO, TURN, UNK
        if GO: check if go to point, otherwise go fwd or bwd 
        if TURN: check do it straight forward
        """
        if len(text_list) == 0:
            self.cur_intent = UNK
            return
        if text_list[0] == "go":
            self.cur_intent = GO
            if "to" in text_list:  # check if go to point
                dests_list = read_all_parentheses(text)
                if len(dests_list) == 0:
                    self.cur_intent = UNK
                    return
                else:
                    self.specs["dests_list"] = dests_list
                    self.specs["goto"] = True
                    return
            else:
                self.specs["goto"] = False
        elif text_list[0] == "turn":
            self.cur_intent = TURN
        else:
            self.cur_intent = UNK
            return

        words_tags = nltk.pos_tag(text_list)  # get a list of tuple (w, t)
        words_tags, detect_negative_value = correct_nltk_tags(words_tags)
        if detect_negative_value:
            print("Negative value is used?! Not supported negative values")
            self.cur_intent = UNK
            return
        if self.debug:
            print("words_tags = ", words_tags)
        if self.cur_intent == TURN:
            if self.debug:
                print("read tags TURN")
            self._read_tags(words_tags)

        if self.cur_intent == GO:
            if self.debug:
                print("read tags GO")
            self._read_tags(words_tags)
        return

    def get_response(self, text):
        self.read(text)
        return self.cur_intent, self.specs


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


def special_notice_nltk():
    """
    found some case where nltk is defective when there are negative values
    """
    print(nltk.pos_tag(nltk.word_tokenize("go -100 metres forward")))
    print(nltk.pos_tag(nltk.word_tokenize("turn -20 degrees to the left")))
    return

def correct_nltk_tags(pos_tags):
    """
    correct negative number tags, backward is tagged NN in some case 
    :param pos_tags: result of nltk.pos_tags() 
    :return: corrected_pos_tags, detect_neg_val
    """
    res = pos_tags
    detect_neg_val = False
    for i in range(len(pos_tags)):
        # backward -> RB
        if res[i][0] == "backward":
            res[i] = (res[i][0], "RB")
        try:
            float(res[i][0])
            if res[i][1] != "CD":
                res[i] = (res[i][0], "CD")
                detect_neg_val = True
        except ValueError:
            continue
    return res, detect_neg_val


if __name__ == '__main__':
    # test_read_parentheses()
    test_read_synonyms()
