from ezflix import Ezflix

ezflix = Ezflix(query="chernobyl")
shows = ezflix.search()
print("Found %s shows" % len(shows))
for s in shows:
    print(s["link"])
