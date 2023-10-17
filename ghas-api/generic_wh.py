from flask import Flask, request
import json
import pprint

app = Flask(__name__)

@app.route('/', methods=['POST'])
def foo():
    data = json.loads(request.data)
    #print(print(data["repository"]["full_name"]))
    #print(data)
    if data["action"] == "resolved": 
        print(f"WARNING: Secret scanning alert resolved: { data['alert']['resolution'] }.")
    return "OK"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4466)



