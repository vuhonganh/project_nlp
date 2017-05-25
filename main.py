from utils import reader
from utils import robot_simu

rd = reader.Reader("data/small_synonyms.txt", debug=False)
robot = robot_simu.Robot()
while True:
    print("Enter command: ", end='')
    cmd = input()
    if cmd == "exit":
        break
    intent, specs = rd.get_response(cmd)
    if intent == "UNK":
        print("Do not understand. Make sure you use predefined syntax correctly!")
    else:
        robot.do_cmd(intent, specs)
