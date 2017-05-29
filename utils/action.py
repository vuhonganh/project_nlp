

class ActionGo:
    """
    super Class that extracts information from intent and deal with it 
    """
    def __init__(self, input_dict):
        self.input_dict = input_dict

    def __str__(self):
        return self.input_dict["intent"] + ", " + str(self.input_dict["list_text"])


class ActionTurn:
    def __init__(self, input_dict):
        self.input_dict = input_dict

    def __str__(self):
        return "HELLO" + self.input_dict["intent"] + ", " + str(self.input_dict["list_text"])


if __name__ == "__main__":
    ad = {"go": ActionGo, "turn": ActionTurn}

    ind_go = {"intent": "go", "list_text": [1, 2, 3]}
    ind_turn = {"intent": "turn", "list_text": [1, 2, 3, 4]}

    act_go = ad["go"](ind_go)
    act_turn = ad["turn"](ind_turn)

    print(act_go)
    print(act_turn)

