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

    def __init__(self, level_no,):
        self.level_no = level_no
        self.keys = []
        #self.keys.clear()

    def getLevel(self):
        level_to_dict = {
            "level": self.level_no,
            "keys": []
        }
        for key in self.keys:
            level_to_dict["keys"].append(key.getKey())
        return level_to_dict
    
    def checkKeyExists(self,key):
        # True -> Level has that key.
        # False -> Level does'nt have it.
        for existingKey in self.keys:
            if existingKey.timestamp == key.timestamp:
                return True

    def addKeyToLevel(self, key):
        # Check existing keys in case of added before
        if not self.checkKeyExists(key):
            self.keys.append(key)

    def __repr__(self):
        return str(self.getLevel())


class User:
    # (int) user_id = 999
    # (list) levels = [ {level: 1}, {level: 2} ]
    def __init__(self, user_id):
        self.user_id = int(user_id)
        self.levels = []
        if path.exists(self.getFileName()):
            #self.levels.clear()
            self.loadUserFromFile()

    def getFileName(self):
        return "data/" + str(self.user_id) + ".json"

    def loadUserFromFile(self):
        self.levels.clear()
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
        self.levels.clear()

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
            #print("\n\nself.levels:\n", self.levels)
            #print("\n\nnew_level:\n", new_level)
            self.levels.append(new_level)
            level_index = self.checkLevelExists(level_no)
        #print("\n\nself.levels:\n", self.levels)
        #print("\n\nself.levels[level_index]:\n", self.levels[level_index].getLevel())
        #print("\n\nkey:\n", key.getKey())
        #print("\n\ngetUser:\n", self.getUser())
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

    #print("\n\nINCOMING KEY:\n", incoming_key.getKey())

    my_user = User(request.args.get("user_id"))
    #print("\n\nUSER CREATED.\n", my_user.getUser())
    my_user.addNewKey(
        request.args.get("level"),
        incoming_key
    )
    #print("\n\nKEY ADDED.\n", my_user.getUser(), "\n\n")

    current_user = my_user.getUser()
    my_user.writeUserToFile()
    
    del my_user
    return jsonify(current_user), 201





my_app.run(debug=True)