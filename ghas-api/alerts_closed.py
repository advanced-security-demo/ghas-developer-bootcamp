from flask import Flask, request
import json

app = Flask(__name__)


@app.route('/', methods=['POST'])
def foo():
    data = json.loads(request.data)
    print(json.dumps(data, indent=4, sort_keys=True))
    #TODO: catch the event when a critical code scanning alert is dismissed
    return "OK"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4567)