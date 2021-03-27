from flask import jsonify

x_size = 5 - 1  # starts count from 0
y_size = 5 - 1  # starts count from 0

class robot:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
    
    def rotate(self, change):
        new_direction = self.direction + change
        if new_direction == -0:
            new_direction = 4
        elif new_direction == 5:
            new_direction = 1
        self.direction = new_direction
            
    def move(self):
        movement = {
            1 : [0,1],
            2 : [1,0],
            3 : [0,-1],
            4 : [-1,0]
        }
        
        new_x = self.x + movement[self.direction][0]
        new_y = self.y + movement[self.direction][1]
        
        if new_x <= x_size and new_x >= 0:
            self.x = new_x
        if new_y <= y_size and new_y >= 0:
            self.y = new_y

def actions(commands, new_robot):

    report = False

    facing_direction = {
    "NORTH" : 1,
    "EAST" : 2,
    "SOUTH" : 3,
    "WEST" : 4
    }

    if commands[0].upper() == "PLACE" and len(commands) == 2:    # checks if initializing command is correct
        try:
            commands[1][0] = int(commands[1][0])
            commands[1][1] = int(commands[1][1])
            
            if commands[1][0] >= 0 and commands[1][0] <= x_size and commands[1][1] >= 0 and commands[1][1] <= y_size \
            and commands[1][2].upper() in list(facing_direction.keys()):

                new_robot = robot(commands[1][0],commands[1][1],facing_direction[commands[1][2].upper()])   # initializes robot

        except:
            pass

    elif commands[0].upper() == "MOVE" and len(commands) == 1:
        try:
            new_robot.move()
        except:
            pass

    elif commands[0].upper() == "RIGHT" and len(commands) == 1:
        try:
            new_robot.rotate(1)
        except:
            pass
        

    elif commands[0].upper() == "LEFT" and len(commands) == 1:
        try:
            new_robot.rotate(-1)
        except:
            pass

    elif commands[0].upper() == "REPORT" and len(commands) == 1:   #sends report to stdout & a file named with the session user
        try:
            direction = list(facing_direction.keys())[new_robot.direction - 1]
            report = ": " + ",".join((str(new_robot.x), str(new_robot.y), direction.upper()))
        except:
            pass
        
    
    elif commands[0] == "```" and len(commands) == 1:
        new_robot.x, new_robot.y, new_robot.direction = None, None, None

    return new_robot, report

def respond(messsage):
    response = jsonify(messsage)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response