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
        self.keys.clear()

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
            self.levels.clear()
            self.loadUserFromFile()

    def getFileName(self):
        return str(self.user_id) + ".json"

    def loadUserFromFile(self):
        with open(self.getFileName(), "r") as f:
            loadedDict = json.load(f)
        for levelDict in loadedDict["levels"]:
            level_load = Level(levelDict["level"])
            for keyDict in levelDict["keys"]:
                key_load = Key(
                    keyDict["timestamp"],
                    keyDict["press_key"],
                    keyDict["press_time"],
                    keyDict["box"],
                    keyDict["boolStatus"]
                )
                level_load.addKeyToLevel(key_load)
            self.levels.append(level_load)


    def writeUserToFile(self):
        with open(self.getFileName(), "w") as f:
            json.dump(self.getUser(), f)

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
            level_index = self.checkLevelExists(level_no)
        print("LEVEL INDEX:", level_index)
        self.levels[level_index].addKeyToLevel(key)

    def getUser(self):
        user_dict = {
            "user_id": self.user_id,
            "levels": []
        }
        for level in self.levels:
            user_dict["levels"].append(level.getLevel())
        return user_dict



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
    print("--------", len(my_user.levels))
    for i in my_user.levels:
        print("List item:")
        print(i.getLevel())
    my_user.addNewKey(
        request.args.get("level"),
        incoming_key
    )
    my_user.writeUserToFile()
    
    return {"status": "success"}, 201





my_app.run(debug=True)