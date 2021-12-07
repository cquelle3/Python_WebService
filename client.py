import requests
import sys
import json

def main():
    print('Client Started (Press CTRL+C to quit)')
    try:
        while(True):
            data = input("")
            try:
                route = data.split(' ', 1)
                if route[0] == "/at":
                    r = requests.post("http://localhost:8080" + route[0], data=route[1])
                    print(r.text)
                elif route[0] == "/sp":
                    r = requests.post("http://localhost:8080" + route[0], data=route[1])
                    try:
                        parsed = json.loads(r.text)
                        print(json.dumps(parsed, indent=4))
                    except:
                        print(r.text)
                else:
                    r = requests.get("http://localhost:8080" + route[0])
                    try:
                        parsed = json.loads(r.text)
                        print(json.dumps(parsed, indent=4))
                    except:
                        print(r.text)
            except:
                print("*Could not connect to web service")

    except KeyboardInterrupt:
        sys.exit()

if __name__ == "__main__":
    main()