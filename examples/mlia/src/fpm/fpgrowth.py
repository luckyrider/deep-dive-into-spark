'''
FP-Growth (FP means frequent pattern)

the FP-Growth algorithm needs:
1. FP-tree (class treeNode)
2. header table (item name -> [count, node link])

This finds frequent itemsets similar to apriori but does not 
find association rules.
'''
class treeNode:
    def __init__(self, name, count, parentNode):
        self.name = name  # item name
        self.count = count
        self.nodeLink = None
        self.parent = parentNode
        self.children = {}  # {item name -> treeNode}
    
    def increment(self, count):
        self.count += count
        
    def display(self, indent=1):
        print '  ' * indent, self.name, ' ', self.count
        for child in self.children.values():
            child.display(indent + 1)

def createTree(patternBase, minSupport=1):
    # go over pattern base twice
    # go through pattern base 1st time: counts item frequency, prune items, prepare header table
    headerTable = {}  # {item name -> support count}
    for pattern in patternBase:
        for item in pattern:
            headerTable[item] = headerTable.get(item, 0) + patternBase[pattern]
    for item in headerTable.keys():  # remove items not meeting minSupport
        if headerTable[item] < minSupport: 
            del(headerTable[item])
    frequentItems = set(headerTable.keys())  # set of frequent item names
    # print 'frequentItems: ',frequentItems
    if len(frequentItems) == 0: return None, None  # if no items meet min support -->get out
    for item in headerTable:
        # reformat headerTable to use Node link: {item name -> [support count, node link}
        headerTable[item] = [headerTable[item], None]
    # print 'headerTable: ', headerTable
    
    # go through pattern base 2nd time: create tree, add node link to header table
    fpTree = treeNode('Null Set', 1, None)
    for pattern, count in patternBase.items():
        effectiveItems = {}
        for item in pattern:  # put pattern items in order
            if item in frequentItems:
                effectiveItems[item] = headerTable[item][0]  # set support count for sorting
        if len(effectiveItems) > 0:
            orderedItems = [v[0] for v in sorted(effectiveItems.items(), key=lambda p: p[1], reverse=True)]
            updateTree(orderedItems, fpTree, headerTable, count)
    return fpTree, headerTable

'''
attach items on a path to parentNode
'''
def updateTree(items, parentNode, headerTable, count):
    # process first item on the path
    firstItem = items[0]
    if firstItem in parentNode.children:  # first item exists on the tree
        parentNode.children[firstItem].increment(count)  # enough just to increment count
    else:  # create node for firstItem and add to parentNode.children
        newNode = treeNode(firstItem, count, parentNode)
        parentNode.children[firstItem] = newNode
        # update header table
        if headerTable[firstItem][1] == None:  # linked list does not exist yet
            headerTable[firstItem][1] = parentNode.children[firstItem]
        else:
            updateLinkedList(headerTable[firstItem][1], newNode)

    # process remaining items on the path
    if len(items) > 1:  # call updateTree() with remaining ordered items
        updateTree(items[1::], parentNode.children[firstItem], headerTable, count)

'''
Add newNode to the tail of the linked list
'''
def updateLinkedList(linkedListNode, newNode):  # this version does not use recursion
    while (linkedListNode.nodeLink != None):  # Do not use recursion to traverse a linked list!
        linkedListNode = linkedListNode.nodeLink
    linkedListNode.nodeLink = newNode  # add newNode next to the last node of the linked list

'''
ascends from leaf node to root
'''
def ascendTree(fromNode, prefixPath):
    if fromNode.parent != None:  # not root
        prefixPath.append(fromNode.name)
        ascendTree(fromNode.parent, prefixPath)
    
def findConditionalPatternBase(basePat, treeNode):  # treeNode comes from header table
    conditionalPatternBase = {}
    while treeNode != None:
        prefixPath = []
        ascendTree(treeNode, prefixPath)
        if len(prefixPath) > 1:  # the first item is not prefix
            conditionalPatternBase[frozenset(prefixPath[1:])] = treeNode.count
        treeNode = treeNode.nodeLink
    return conditionalPatternBase

'''
@param pfTree: PF-Tree
@param headerTable: Header Table related to PF-Tree
@param minSupport: 
@param suffixPattern: suffix pattern to be appended to frequent patterns of the pfTree
@param frequentItemsets: all frequent patterns
'''
def mineTree(pfTree, headerTable, minSupport, suffixPattern, frequentItemsets):
    # sort conditionalFrequentItems in header table by support count
    # these frequent items are conditional, 
    # and must be appended to suffix pattern to form a real frequent pattern
    conditionalFrequentItems = [v[0] for v in sorted(headerTable.items(), key=lambda p: p[1])]
    for conditionalFrequentItem in conditionalFrequentItems:  # divide and conquer
        newSuffixPattern = suffixPattern.copy()
        newSuffixPattern.add(conditionalFrequentItem)
        frequentItemsets.append(newSuffixPattern)
        conditionalPatternBase = findConditionalPatternBase(conditionalFrequentItem, headerTable[conditionalFrequentItem][1])
        conditionalFpTree, conditionalHeaderTable = createTree(conditionalPatternBase, minSupport)
        if conditionalHeaderTable != None:
            # print 'conditional tree for: ',newSuffixPattern
            # conditionalFpTree.display(1)
            mineTree(conditionalFpTree, conditionalHeaderTable, minSupport, newSuffixPattern, frequentItemsets)

def loadDataset():
    dataset = [['r', 'z', 'h', 'j', 'p'],
               ['z', 'y', 'x', 'w', 'v', 'u', 't', 's'],
               ['z'],
               ['r', 'x', 'n', 'o', 's'],
               ['y', 'r', 'x', 'z', 'q', 't', 'p'],
               ['y', 'z', 'x', 'e', 'q', 's', 't', 'm']]
    return dataset

def createInitPatternBase(dataset):
    patternBase = {}
    for transaction in dataset:
        patternBase[frozenset(transaction)] = 1
    return patternBase

def test1():
    minSupport = 3
    dataset = loadDataset()
    initPatternBase = createInitPatternBase(dataset)
    fpTree, headerTable = createTree(initPatternBase, minSupport)
    fpTree.display()
    frequentItemsetList = []
    mineTree(fpTree, headerTable, minSupport, set([]), frequentItemsetList)
    print frequentItemsetList

import apriori

def test2():
    minSupport = 3
    dataset = apriori.dataset()
    initPatternBase = createInitPatternBase(dataset)
    fpTree, headerTable = createTree(initPatternBase, minSupport)
    fpTree.display()
    frequentItemsetList = []
    mineTree(fpTree, headerTable, minSupport, set([]), frequentItemsetList)
    print frequentItemsetList

if __name__ == "__main__":
    test1();
