from turtle import Turtle


class Robot(Turtle):

    def __init__(self):
        Turtle.__init__(self)
        self.getscreen().setup(1000, 1000)  # window
        self.draw_map()
    def draw_map(self, W=600, H=800):
        self.speed(10)
        self.pu()
        # turtle.goto(xC - W/2.0, yC - H/2.0)
        x, y = self.position()
        self.goto(x - W / 2, y - H / 2)
        # turtle.bd(-W/2)
        self.pd()
        self.lt(90)
        for i in range(4):
            if i % 2 == 0:
                self.fd(H)
            else:
                self.fd(W)
            self.rt(90)
        self.pu()
        self.home()
        self.pd()
        self.speed(1)
        self.pensize(2)

    def do_cmd(self, intent, specs):
        if intent == "GO":
            self.fd(specs["meters"])
        elif intent == "GOTO":
            for dest in specs["dests_list"]:
                self.goto(dest[0], dest[1])
        elif intent == "TURN":
            self.rt(specs["degrees"])
        else:
            print("Unknown intent")
