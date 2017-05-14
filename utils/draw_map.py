import turtle

def draw_rectangle(W, H):
    turtle.speed(10)
    turtle.pu()
    # turtle.goto(xC - W/2.0, yC - H/2.0)
    x, y = turtle.position()
    turtle.goto(x - W/2, y - H/2)
    # turtle.bd(-W/2)
    turtle.pd()
    turtle.lt(90)
    for i in range(4):
        if i % 2 == 0:
            turtle.fd(H)
        else:
            turtle.fd(W)
        turtle.rt(90)

turtle.setup(1000, 1000)
draw_rectangle(600, 800)

turtle.pu()
turtle.home()
turtle.pd()
turtle.speed(1)
turtle.pensize(2)

# arbitrary trajectory
turtle.fd(40)
turtle.rt(50)
turtle.fd(40)
turtle.rt(-90)
turtle.fd(40)

turtle.done()

# while True:
#     turtle.speed(2)
#     cmd = input()
#     if cmd == 'exit':
#         break
#     elif cmd == 'f':
#         turtle.fd(50)
#     elif cmd == 'r':
#         turtle.rt(90)
#     elif cmd == 'u':
#         turtle.pu()
#     elif cmd == 'd':
#         turtle.pd()
#     else:
#         print('unknown command')
#
