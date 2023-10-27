import requests
import json

# with open("x.json", "r") as f:
#     d = f.read()


# r = requests.post("http://4.3.2.1/json/state", data=d)

# print(r)
def fetch_mode(filename: str):
    r = requests.get("http://4.3.2.1/json/state")
    with open(f"{filename}.json", "w") as f:
        f.write(r.content.decode())
        # json.dump(json.loads(r.content.decode()), f)

def send_request(data):
    r = requests.post("http://4.3.2.1/json/state", data=json.dumps(data))
    print(r.status_code)
if __name__ == "__main__":
    # fetch_mode("idle")
    send_request({"on": True, "ps": "2"})
    # r = requests.get("http://4.3.2.1/json/state")
    # with open("chase.json", "w") as f:
    #     f.write(r.content.decode())
    #     # json.dump(json.loads(r.content.decode()), f)

    # import time
    # r = requests.post("http://4.3.2.1/json/state", {"on": False})
    # time.sleep(5)
    # with open("chase.json", "r") as f:
    #     chase = json.load(f)
    # r2 = requests.post("http://4.3.2.1/json/state", chase)