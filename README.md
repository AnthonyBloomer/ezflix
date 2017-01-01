# ezflix

Command line utility to search for TV shows on EZTV and open in Peerflix automatically.

#### Install 

```
pip install -r requirements.txt
```

#### Usage

Run ```python eztv.py [query]``` then from the list, select the TV episode you want to watch. 

#### Example 

```bash
python eztv.py "The Man in the High Castle"
```

You can also pass an optional argument "latest" to watch the latest episode. For example:

```bash
python eztv.py "South Park" latest
```


#### Requires

[Peerflix](https://github.com/mafintosh/peerflix)
