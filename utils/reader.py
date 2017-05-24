"""
reader.py: process input sentence and extract important information
"""
import nltk


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
        cur_pos = read_coordinates(in_text[id_start+1: id_end])
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