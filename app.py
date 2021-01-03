from flask import Flask, jsonify, request

my_app = Flask(__name__)


@my_app.route("/")
def hello():
    return "Hello World!"

@my_app.route("/api/saveData", methods=["GET", "POST"])
def save():
    # If the request isn't POST, return 403
    if request.method != "POST":
        return {"status": "fail"}, 403

    # Get the values
    values = {
        "timestamp_id": request.args.get("timestamp_id"),
        "level": request.args.get("level"),
        "pressTime": request.args.get("pressTime"),
        "pressKey": request.args.get("pressKey"),
        "box": request.args.get("box"),
        "bool": request.args.get("bool")
    }


    # Check if file exists
    # {timestamp_id}.json
    if False:
        # If it doesn't, create it
        pass
    
    



    return {"status": "success"}, 201


my_app.run(debug=True)