from os import path
import json
from flask import Flask, jsonify, request

my_app = Flask(__name__)

class Key:
    # timestamp = 0
    # press_key = "Q"
    # press_time = "500"
    # box = "redBox"
    # boolStatus = True

    def __init__(self, timestamp, press_key, press_time, box, boolStatus):
        self.timestamp = timestamp
        self.press_key = press_key
        self.press_time = press_time
        self.box = box
        self.boolStatus = boolStatus

    def getKey(self):
        return {
                "timestamp": self.timestamp,
                "press_key": self.press_key,
                "press_time": self.press_time,
                "box": self.box,
                "boolStatus": self.boolStatus
            }
        


class Level:
    # (int) level_no = 1
    # (list) keys = []
    keys = []

    def __init__(self, level_no,):
        self.level_no = level_no

    def getLevel(self):
        level_to_dict = {
            "level": self.level_no,
            "keys": []
        }
        for key in self.keys:
            level_to_dict["keys"].append(key.getKey())
        return level_to_dict
    
    def addKeyToLevel(self, key):
        self.keys.append(key)


class User:
    # (int) user_id = 999
    # (list) levels = [ {level: 1}, {level: 2} ]
    user_id = 0
    levels = []
    def __init__(self, user_id):
        self.user_id = int(user_id)
        if path.exists(self.getFileName()):
            self.loadUserFromFile()

    def getFileName(self):
        return str(self.user_id) + ".json"

    def loadUserFromFile(self):
        with open(self.getFileName(), "r") as f:
            loadedJson = json.load(f)
        for level in loadedJson["levels"]:
            my_level = Level(level["level"])
            for key in level["keys"]:
                my_key = Key(
                    key["timestamp"],
                    key["press_key"],
                    key["press_time"],
                    key["box"],
                    key["boolStatus"]
                )
                my_level.addKeyToLevel(my_key)
            self.levels.append(my_level)

    def writeUserToFile(self):
        with open(self.getFileName(), "w") as f:
            user_to_dict = {
                "user_id": self.user_id,
                "levels": []
            }
            for level in self.levels:
                user_to_dict["levels"].append(level.getLevel())
            json.dump(user_to_dict, f)
            #print(user_to_dict)

    def checkLevelExists(self, level_no):
        for level in self.levels:
            if level.level_no == level_no:
                return self.levels.index(level)
        return -1

    def addNewKey(self, level_no, key):
        level_index = self.checkLevelExists(level_no)
        if level_index == -1:
            # No level, then create it
            new_level = Level(level_no)
            self.levels.append(new_level)

        self.levels[level_index].addKeyToLevel(key)



@my_app.route("/")
def hello():
    return "Hello World!"

@my_app.route("/api/saveData", methods=["GET", "POST"])
def save():
    # If the request isn't POST, return 403
    if request.method != "POST":
        return {"status": "fail"}, 403

    incoming_key = Key(
        request.args.get("timestamp"),
        request.args.get("pressKey"),
        request.args.get("pressTime"),
        request.args.get("box"),
        request.args.get("boolStatus")
    )

    my_user = User(request.args.get("user_id"))
    my_user.addNewKey(
        request.args.get("level"),
        incoming_key
    )
    my_user.writeUserToFile()
    

    return {"status": "success"}, 201





my_app.run(debug=True)