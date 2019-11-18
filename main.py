import json
import traceback

from app import App

# Constants
POOL    = 10
URL     = "https://www.cermati.com/karir"

if __name__ == "__main__":
    try:
        obj  = App(URL, POOL)
        data = obj.run()
    except:
        data = None
        traceback.print_exc()

    if data:
        with open("output.json", "w") as output:
            output.write(json.dumps(data, indent=4))
    else:
        print ("Failed")
