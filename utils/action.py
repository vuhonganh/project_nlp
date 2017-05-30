
def is_float(t):
    try:
        float(t)
        return True
    except ValueError:
        return False

class ActionGo:
    """
    super Class that extracts information from intent and deal with it 
    """
    def __init__(self, input_dict):
        self.input_dict = input_dict
        self.res_dict = {}

    def __str__(self):
        return self.input_dict["intent"] + ", " + str(self.input_dict["list_text"])

    def _extract_info_strict(self):
        """
        strictly follow the rules for GO intent
        procedure extracts info to self.res_dict
        """
        if is_float(self.input_dict["list_text"][2]):
            direct = 1
            if "backward" == self.input_dict["list_text"][1]:
                direct = -1
            elif "forward" != self.input_dict["list_text"][1]:
                self.res_dict["intent"] = "UNK"
                return
            self.res_dict["dist"] = direct * int(float(self.input_dict["list_text"][2]))
            self.res_dict["intent"] = self.input_dict["intent"]

    def do_act(self, robot):
        self._extract_info_strict()
        response = ""
        if self.res_dict["intent"] == "UNK":
            response += "Unknown command! Please check the rule"
        else:
            robot.fwd(self.res_dict["dist"])
            response += self.res_dict["intent"] + " complete."
        return response


class ActionTurn:
    def __init__(self, input_dict):
        self.input_dict = input_dict
        self.res_dict = {}

    def __str__(self):
        return self.input_dict["intent"] + ", " + str(self.input_dict["list_text"])

    def _extract_info_strict(self):
        """
        strictly follow the rules for TURN intent
        procedure extracts info to self.res_dict
        """
        if is_float(self.input_dict["list_text"][2]):
            right = 1
            if "left" == self.input_dict["list_text"][1]:
                right = -1
            elif "right" != self.input_dict["list_text"][1]:
                self.res_dict["intent"] = "UNK"
                return
            self.res_dict["angle"] = right * int(float(self.input_dict["list_text"][2]))
            self.res_dict["intent"] = self.input_dict["intent"]

    def do_act(self, robot):
        self._extract_info_strict()
        response = ""
        if self.res_dict["intent"] == "UNK":
            response += "Unknown command! Please check the rule"
        else:
            robot.turn_right(self.res_dict["angle"])
            response += self.res_dict["intent"] + " complete."
        return response


if __name__ == "__main__":
    ad = {"go": ActionGo, "turn": ActionTurn}

    ind_go = {"intent": "go", "list_text": [1, 2, 3]}
    ind_turn = {"intent": "turn", "list_text": [1, 2, 3, 4]}

    act_go = ad["go"](ind_go)
    act_turn = ad["turn"](ind_turn)

    print(act_go)
    print(act_turn)

