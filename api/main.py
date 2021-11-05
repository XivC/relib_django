import dataset
import recommendations
import traceback
from importlib import reload
from datetime import datetime
if __name__ == "__main__":
    dataset.load('dataset/')

    delta = 0
    parts = 6
    count = len(dataset.user_books.keys())
    start = int(count / parts) * delta
    end = int(count / parts) * (delta + 1)
    recs = {}
    ct = end - start
    n = 0

    for user in list(dataset.user_books.keys())[start:end]:
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
