import nltk

class Reader2:
    """
    simple reader that returns the intent, POS tags and raw text
    """
    def __init__(self, syn_file):
        self.syn_dict = self.__class__.build_synonyms_dict(syn_file)
        self.res_dict = {}

    def _preprocess(self, text):
        """
        remove some redundant words and punctuation from text string 
        and replace by its synonym
        :param text: input as whole text string
        :return: text preprocessed as list
        """
        # nltk helps separate punctuation from word (e.g. please? -> please ?)
        text_list = nltk.word_tokenize(text.lower())
        # NOTE: consider can/could be another intent (question abt ability)
        # to_removes = ('please', 'can', 'you', '.', '!', '?', 'straight')
        to_removes = ('please', '.', '!', '?', 'straight', 'so', 'well')
        res = [t for t in text_list if t not in to_removes]
        res = [self.syn_dict[t] if t in self.syn_dict.keys() else t for t in res]
        return res

    def read(self, text):
        self.res_dict["raw_text"] = text

        text_processed_list = self._preprocess(text)
        self.res_dict["list_text"] = text_processed_list

        if text_processed_list[0] == "go":
            self.res_dict["intent"] = text_processed_list[0]
            if len(text_processed_list) > 1 and text_processed_list[1] == "to":
                self.res_dict["intent"] = "goto"

        return self.res_dict

    @staticmethod
    def build_synonyms_dict(syn_file):
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
                res.update({key: val for key in ws[1:]})
        return res


if __name__ == "__main__":
    rd = Reader2("../data/small_synonyms.txt")
    print(rd.read("go forward 100 meters"))