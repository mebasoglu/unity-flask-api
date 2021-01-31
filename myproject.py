from os import path
from datetime import datetime
import json
from flask import Flask, jsonify, request, redirect, url_for, render_template

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
        # self.keys.clear()

    def getLevel(self):
        level_to_dict = {
            "level": self.level_no,
            "keys": []
        }
        for key in self.keys:
            level_to_dict["keys"].append(key.getKey())
        return level_to_dict

    def checkKeyExists(self, key):
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
        self.page_url = ""
        self.user_id = int(user_id)
        self.levels = []
        if path.exists(self.getFileName()):
            # self.levels.clear()
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
        self.page_url = loadedDict["page_url"]

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
            "page_url": self.page_url,
            "levels": []
        }
        for level in self.levels:
            user_dict["levels"].append(level.getLevel())
        return user_dict


class Box:
    # (string) box_name
    # (int) level
    # (int) timestamp
    def __init__(self, box_name, level, timestamp):
        self.box_name = box_name
        self.level = int(level)
        self.timestamp = timestamp

    def getBox(self):
        return {
            "box_name": self.box_name,
            "level": self.level,
            "timestamp": self.timestamp
        }


class BoxInfo:
    # (int) user_id = 123
    # (list) boxes = [Box1, Box2]
    def __init__(self, user_id):
        self.user_id = int(user_id)
        self.boxes = []
        if path.exists(self.getFileName()):
            self.loadBoxInfoFromFile()

    def getFileName(self):
        return "data/" + str(self.user_id) + "_boxes.json"
    
    def loadBoxInfoFromFile(self):
        with open(self.getFileName(), "r") as f:
            loadedDict = json.load(f)
        for box in loadedDict["boxes"]:
            box_load = Box(box["box_name"], box["level"], box["timestamp"])
            self.boxes.append(box_load)

    def getBoxInfo(self):
        info_dict = {
            "user_id": self.user_id,
            "boxes": []
        }
        for box in self.boxes:
            info_dict["boxes"].append(box.getBox())
        return info_dict
        
    def writeBoxInfoToFile(self):
        print(
            "Box info: ",
            self.getBoxInfo()
        )
        with open(self.getFileName(), "w") as f:
            json.dump(self.getBoxInfo(), f)

    def addNewBox(self, box):
        self.boxes.append(box)


@my_app.route("/", methods=["GET", "POST"])
def index():
    now = datetime.now()
    timestamp = int(datetime.timestamp(now))
    url = url_for("view_survey") + "?timestamp=" + str(timestamp)
    if request.method == "POST":
        return redirect(url)
    return render_template("intro_form.html")


@my_app.route("/survey", methods=["GET", "POST"])
def view_survey():
    if request.method == "POST":
        timestamp = request.form["timestamp"]
        print("TAYMSITEMP: ", timestamp)
        print("----A: ", request.form["A"])
        survey_result = {
            "A": request.form["A"],
            "GE": request.form["GE"],
            "L": request.form["L"],
            "F": request.form["F"],
            "I": request.form["I"],
            "D": request.form["D"],
            "E": request.form["E"],
            "U": request.form["U"],
            "S": request.form["S"],
            "G": request.form["G"],
            "S1": request.form["S1"],
            "H": request.form["H"],
            "E1": request.form["E1"],
            "P": request.form["P"],
            "I1": request.form["I1"],
            "A5": request.form["A5"],
            "A1": request.form["A1"],
            "I2": request.form["I1"],
            "N": request.form["N"],
            "D1": request.form["D1"],
            "A2": request.form["A2"],
            "J": request.form["J"],
            "A3": request.form["A3"],
            "A4": request.form["A4"]
        }
        with open(f"data/{timestamp}_survey.json", "w") as f:
            json.dump(survey_result, f)
        url = url_for("view_colour") + "?timestamp=" + timestamp
        return redirect(url)
    return render_template("survey.html")


@my_app.route("/colourblindtest", methods=["GET", "POST"])
def view_colour():
    if request.method == "POST":
        timestamp = request.form["timestamp"]
        survey_result = {
            "12": request.form["12"],
            "74": request.form["74"],
            "6": request.form["6"],
            "16": request.form["16"],
            "2": request.form["2"],
            "29": request.form["29"],
            "7": request.form["7"],
            "45": request.form["45"],
            "5": request.form["5"],
            "97": request.form["97"],
            "8": request.form["8"],
            "42": request.form["42"],
            "3": request.form["3"]
        }
        with open(f"data/{timestamp}_colour.json", "w") as f:
            json.dump(survey_result, f)
        url = url_for("view_video") + "?timestamp=" + timestamp
        return redirect(url)
        
    return render_template("colourblindtest.html")

@my_app.route("/video", methods=["GET", "POST"])
def view_video():
    if request.method == "POST":
        timestamp = request.form["timestamp"]
        survey_result = {
            "Arousal1": request.form["Arousal1"],
            "Valence1": request.form["Valence1"],
            "Arousal2": request.form["Arousal2"],
            "Valence2": request.form["Valence2"],
            "Arousal3": request.form["Arousal3"],
            "Valence3": request.form["Valence3"],
            "Arousal4": request.form["Arousal4"],
            "Valence4": request.form["Valence4"],
            "Arousal5": request.form["Arousal5"],
            "Valence5": request.form["Valence5"],
            "Arousal6": request.form["Arousal6"],
            "Valence6": request.form["Valence6"],
            "Arousal7": request.form["Arousal7"],
            "Valence7": request.form["Valence7"],
            "Arousal8": request.form["Arousal8"],
            "Valence8": request.form["Valence8"]
        }
        with open(f"data/{timestamp}_video.json", "w") as f:
            json.dump(survey_result, f)
        url = url_for("view_textures") + "?timestamp=" + timestamp
        return redirect(url)
        
    return render_template("video.html")

@my_app.route("/textures", methods=["GET", "POST"])
def view_textures():
    if request.method == "POST":
        timestamp = request.form["timestamp"]
        survey_result = {
            "T1": request.form["T1"],
            "T2": request.form["T2"],
            "T3": request.form["T3"],
            "T4": request.form["T4"],
            "T5": request.form["T5"],
            "T6": request.form["T6"],
            "T7": request.form["T7"],
            "T8": request.form["T8"],
            "T9": request.form["T9"],
            "T10": request.form["T10"],
            "T11": request.form["T11"],
            "T12": request.form["T12"]
        }
        with open(f"data/{timestamp}_textures.json", "w") as f:
            json.dump(survey_result, f)
        url = url_for("view_game_description") + "?timestamp=" + timestamp
        return redirect(url)
        
    return render_template("textures.html")

@my_app.route("/game_description", methods=["GET", "POST"])
def view_game_description():
    if request.method == "POST":
        timestamp = request.form["timestamp"]
        url = url_for("static", filename="game2501/index.html") + "?timestamp=" + timestamp
        return redirect(url)
        
    return render_template("game_description.html")

# @my_app.route("/game", methods=["GET", "POST"])
# def view_game():
#     if request.method == "POST":
#         timestamp = request.form["timestamp"]
#         url = url_for("NEXT") + "?timestamp=" + timestamp
#         return redirect(url)
        
#     return render_template("game2501/index.html")

@my_app.route("/hello")
def hello():
    return "Hello World!"


@my_app.route("/api/saveData", methods=["GET", "POST"])
def save():
    # If the request isn't POST, return 403
    # if request.method != "POST":
    #    return {"status": "fail"}, 403

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

@my_app.route("/debriefsheet", methods=["GET", "POST"])
def debriefsheet():
    if request.method == "POST":
        return redirect(url_for("thanks"))
    return render_template("debriefsheet.html")

@my_app.route("/thanks")
def thanks():
    return render_template("thanks.html")

@my_app.route("/api/saveBox", methods=["GET", "POST"])
def save_box():
    # GET (user_id, box_name, level)
    incoming_box = Box(
        request.args.get("box_name"),
        request.args.get("level"),
        request.args.get("timestamp")
    )
    print("Gelen kutu: ", incoming_box.getBox())
    my_box_info = BoxInfo(request.args.get("user_id"))
    my_box_info.addNewBox(incoming_box)
    my_box_info.writeBoxInfoToFile()

    return jsonify(my_box_info.getBoxInfo()), 201

if __name__ == "main":
    my_app.run()