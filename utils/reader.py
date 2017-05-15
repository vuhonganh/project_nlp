"""
reader.py: process input sentence and extract important information
"""


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


if __name__ == '__main__':
    test_read_parentheses()

