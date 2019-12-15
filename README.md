# document-search-py-task
an interview coding task in python 

## goal

build a webserver API that accepts any number of words in english and returns a list of all documents containing ALL words in the query. 

## getting familiar with the repo
1. clone the repo locally
2. run the unit tests `cd src && python -m unittest -b test_index`
3. `index.py` contains a very naive document index implementation. For each query, it will iterate over each document, and look for each word. This can be done in a much more efficient way. 
4. Running `cd src && python __init__.py` will start a webserver which will search the index. You can use `curl` to query it for example: `http://localhost:8080/?q=hello+world` will return a JSON document with all of the documents containing both `hello` and `world`

## instructions
1. download and extract the full dataset into `data/` (see below)
2. implement a more efficient search index, while maintaing the existing interface (you should not modify the webserver code in this phase). the unit tests should still pass untouched. you may add more tests to help you develop faster. 

benchmarking the current solution with a tool such as [hey](https://github.com/rakyll/hey):

```
hey -n 30 -c 1 http://localhost:8080/\?q\=hello+world

Summary:
  Total:	10.8354 secs
  Slowest:	0.3826 secs
  Fastest:	0.3527 secs
  Average:	0.3612 secs
  Requests/sec:	2.7687

  Total data:	742740 bytes
  Size/request:	24758 bytes

Response time histogram:
  0.353 [1]	|■■■■
  0.356 [3]	|■■■■■■■■■■■■
  0.359 [10]	|■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
  0.362 [7]	|■■■■■■■■■■■■■■■■■■■■■■■■■■■■
  0.365 [2]	|■■■■■■■■
  0.368 [2]	|■■■■■■■■
  0.371 [2]	|■■■■■■■■
  0.374 [1]	|■■■■
  0.377 [1]	|■■■■
  0.380 [0]	|
  0.383 [1]	|■■■■


Latency distribution:
  10% in 0.3556 secs
  25% in 0.3572 secs
  50% in 0.3590 secs
  75% in 0.3655 secs
  90% in 0.3734 secs
  95% in 0.3826 secs
  0% in 0.0000 secs

```

3. `bottle.py` is a standalone webserver micro framework  written in python.  you can find its docs [here](https://bottlepy.org/docs/dev/). your second task is to modify the webserver code (and Index class if needed), such that the webserver response payload will contains a link to the document, following the link should serve the document contents. 


## dataset 

1. the data set is the ["Blog Authorship Corpus"](http://u.cs.biu.ac.il/~koppel/BlogCorpus.htm) 
2. the dataset contains xml files of public blog posts, a few example files are already available in the `data` directory. 
3. the first number in the file name is the document's id number. 
4. for the purposes of this task you may treat XML tags as normal words, this is not a text parsing excercise. 
