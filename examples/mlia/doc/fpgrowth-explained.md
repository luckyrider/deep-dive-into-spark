# FP-growth

```
dataset = [
['r', 'z', 'h', 'j', 'p'],
['z', 'y', 'x', 'w', 'v', 'u', 't', 's'],
['z'],
['r', 'x', 'n', 'o', 's'],
['y', 'r', 'x', 'z', 'q', 't', 'p'],
['y', 'z', 'x', 'e', 'q', 's', 't', 'm']
]

frequent patterns:
[set(['y']), set(['y', 'x']), set(['y', 'z']), set(['y', 'x', 'z']), set(['s']), set(['x', 's']), set(['t']), set(['y', 't']), set(['x', 't']), set(['y', 'x', 't']), set(['z', 't']), set(['y', 'z', 't']), set(['x', 'z', 't']), set(['y', 'x', 'z', 't']), set(['r']), set(['x']), set(['x', 'z']), set(['z'])]
```

```
dataset = [
[1, 3, 4], 
[2, 3, 5], 
[1, 2, 3, 5], 
[2, 5]
]

frequent patterns (2/4):
[set([1]), set([1, 3]), set([2]), set([3]), set([2, 3]), set([5]), set([3, 5]), set([2, 3, 5]), set([2, 5])]

frequent patterns (3/4):
[set([2]), set([3]), set([5]), set([2, 5])]
```
