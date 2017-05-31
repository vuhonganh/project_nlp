
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
        self.res_dict["intent"] = "UNK"
        if len(self.input_dict["list_text"]) >= 3 and is_float(self.input_dict["list_text"][2]):
            direct = 1
            if "backward" == self.input_dict["list_text"][1]:
                direct = -1
            elif "forward" != self.input_dict["list_text"][1]:
                return
            self.res_dict["dist"] = direct * int(float(self.input_dict["list_text"][2]))
            self.res_dict["intent"] = self.input_dict["intent"]

    def do_act(self, robot):
        self._extract_info_strict()
        response = ""
        if self.res_dict["intent"] == "UNK":
            response += "Unknown command! Please check the rule"
        else:
            if abs(self.res_dict["dist"]) < 1001:
                robot.fwd(self.res_dict["dist"])
                response += self.res_dict["intent"] + " complete."
            else:
                response += self.res_dict["intent"] + " distance out of range (max = 1000)"
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
        self.res_dict["intent"] = "UNK"
        length_list = len(self.input_dict["list_text"])
        if length_list == 2 or is_float(self.input_dict["list_text"][2]):
            left = 1
            if "right" == self.input_dict["list_text"][1]:
                left = -1
            elif "left" != self.input_dict["list_text"][1]:
                return
            angle = 90
            if length_list > 2:
                angle = int(float(self.input_dict["list_text"][2])) % 360
            self.res_dict["angle"] = left * angle
            self.res_dict["intent"] = self.input_dict["intent"]

    def do_act(self, robot):
        self._extract_info_strict()
        response = ""
        if self.res_dict["intent"] == "UNK":
            response += "Unknown command! Please check the rule"
        else:
            robot.turn_left(self.res_dict["angle"])
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

