from turtle import Turtle
import cozmo
from cozmo.util import degrees, distance_mm, speed_mmps
from scipy.misc import imread, imresize, imsave, imshow
import time

class Robot(Turtle):

    def __init__(self, acozmo=None):
        Turtle.__init__(self)
        self.getscreen().setup(1000, 1000)  # window
        self.draw_map()
        self.m_cozmo = acozmo
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

    def fwd(self, dist):
        self.forward(dist)
        if self.m_cozmo:
            self.m_cozmo.drive_straight(distance_mm(dist), speed_mmps(100))
            # self.m_cozmo.drive_straight(distance_mm(dist), speed_mmps(50)).wait_for_completed()

    def turn_left(self, angle):
        self.lt(angle)
        if self.m_cozmo:
            self.m_cozmo.turn_in_place(degrees(angle))
            # self.m_cozmo.turn_in_place(degrees(angle)).wait_for_completed()

    def shut_down(self):
        self.getscreen().bye()

    def take_photo(self):
        if self.m_cozmo:
            # self.m_cozmo.world.wait_for(cozmo.world.EvtNewCameraImage) - not work
            cnt = 0
            latest_img = None
            while latest_img is None and cnt < 10:
                latest_img = self.m_cozmo.world.latest_image
                time.sleep(0.1)
                cnt += 1
            img = latest_img.raw_image
            imsave('cur_orig_img.JPEG', img)
            # imsave('cur_img.png', img)
            img = imresize(img, (224, 224))
            return img
        return None

    def take_photo_detect(self):
        if self.m_cozmo:
            # self.m_cozmo.world.wait_for(cozmo.world.EvtNewCameraImage) - not work
            cnt = 0
            latest_img = None
            while latest_img is None and cnt < 10:
                latest_img = self.m_cozmo.world.latest_image
                time.sleep(0.1)
                cnt += 1
            img = latest_img.raw_image
            imsave('cur_orig_img.JPEG', img)
            # imsave('cur_img.png', img)
            # img = imresize(img, (224, 224))
            return img
        return None


    def say_text(self, text):
        if self.m_cozmo:
            self.m_cozmo.say_text(text)