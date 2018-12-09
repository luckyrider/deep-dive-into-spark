# Apriori Explained

## Essentials


## Example

### Dataset
```
dataset = [
[1,3,4],
[2,3,5],
[1,2,3,5],
[2,5]
]

### Config
* minSupport = 0.5
* minConfidence = 0.7

### Result
```
supports = {
frozenset([5]): 0.75, 
frozenset([3]): 0.75, 
frozenset([2, 3, 5]): 0.5, 
frozenset([1, 2]): 0.25, 
frozenset([1, 5]): 0.25, 
frozenset([3, 5]): 0.5, 
frozenset([4]): 0.25, 
frozenset([2, 3]): 0.5, 
frozenset([2, 5]): 0.75, 
frozenset([1]): 0.5, 
frozenset([1, 3]): 0.5, 
frozenset([2]): 0.75
}
```

```
L_list = [
L1 = [frozenset([1]), frozenset([3]), frozenset([2]), frozenset([5])], 
L2 = [frozenset([1, 3]), frozenset([2, 5]), frozenset([2, 3]), frozenset([3, 5])], 
L3 = [frozenset([2, 3, 5])], []
]
```

```
rules = [
(frozenset([1]), frozenset([3]), 1.0), 
(frozenset([5]), frozenset([2]), 1.0), 
(frozenset([2]), frozenset([5]), 1.0), 
(frozenset([3, 5]), frozenset([2]), 1.0), 
(frozenset([2, 3]), frozenset([5]), 1.0)
]
```

