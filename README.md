# Funcy
Python library with fluent interface.

## How to install?
Run `pip install git+https://github.com/tushushu/funcy.git` to install `funcy`.

## How to build?
* Run `python setup.py bdist_wheel` to build the wheel file.
* Run `pip install {wheel file path}` to install `funcy` from the wheel file.

## Examples

### Word count
```Python
import re
from funcy import Iter


words = "I like you, and you like me!"
Iter(re.split("\s|,|!", words))\
.map(lambda x: (x, 1))\
.groupby(lambda x: x[0], lambda x: x[1])\
.map(lambda x: (x[0], sum(x[1])))\
.filter(lambda x: x != ' ')\
.to_dict()
```

Result:  
`{'I': 1, 'like': 2, 'you': 2, '': 2, 'and': 1, 'me': 1}`


### Cumulative sum
```Python
from funcy import Iter


arr = [1, 2, 3, 4, 5]
Iter(arr)\
.map(lambda x: [x])\
.reduce(lambda x, y: x + [x[-1] + y[0]])
```

Result:  
`[1, 3, 6, 10, 15]`


### Transpose 2D list
```Python
from funcy import Iter


mat = [
    [1, 2, 3], 
    [4, 5, 6], 
    [7, 8, 9]
]
Iter(zip(*mat)).map(list).to_list()
```

Result:  
`[[1, 4, 7], [2, 5, 8], [3, 6, 9]]`


### Find the indexes of all negative numbers
```Python
from funcy import Iter


arr = [1, -2, 3, -4, 5]
Iter(arr)\
.zip(range(len(arr)))\
.filter(lambda x: x[0] < 0)\
.map(lambda x: x[1])\
.to_list()
```

Result:  
`[1, 3]`
