import dataset
import recommendations
import traceback
from importlib import reload
from datetime import datetime
import json
import sys
import subprocess
def main(delta):
    print(delta)
    dataset.load('dataset/')

    
    parts = 1000
    count = len(dataset.user_books.keys())
    start = int(count / parts) * delta
    end = int(count / parts) * (delta + 1)
    recs = {}
    ct = end - start
    n = 0

    for user in list(dataset.user_books.keys())[0:5000]:
        n += 1
        time = datetime.now()
        try:
            rec = recommendations.get_response(user, dataset)
            recs[user] = rec
        except:
            traceback.print_exc()
            recs[user] = {}
        if n % 10 == 0:
            print(f"calculated {n}/{ct} users")
    with open(f"part_{delta}.json", "w") as f:
        f.write(json.dumps(recs))


if __name__ == "__main__":
    main(0)  
    
    
