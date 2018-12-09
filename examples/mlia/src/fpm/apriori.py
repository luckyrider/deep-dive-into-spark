from numpy import *

def dataset():
    return [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]

'''
create C1, all single item itemsets
'''
def createC1(transactions):
    C1 = []
    for transaction in transactions:
        for item in transaction:
            if not [item] in C1:
                C1.append([item])  
    C1.sort()
    # use frozen set so we can use it as a key in a dictionary
    return map(frozenset, C1)

'''
filter candidate C to form L by excluding non-frequent itemsets.
@return: L, supports
'''
def filterCToFormL(C, transactions, minSupport):
    # calcuate support count for each itemset in C
    # # It's comparatively slower to read transactions, 
    # # so put transactions in outer loop.
    supportCounts = {}  # dict: itemset -> support count
    for transaction in transactions:
        for candidateItemset in C:
            if candidateItemset.issubset(transaction):
                if not supportCounts.has_key(candidateItemset): 
                    supportCounts[candidateItemset] = 1
                else:
                    supportCounts[candidateItemset] += 1
    
    # retain any itemset whose support >= minSupport
    numTransactions = float(len(transactions))
    L = []
    supports = {}  # dict: itemset -> support
    for key in supportCounts:
        support = supportCounts[key] / numTransactions
        supports[key] = support
        if support >= minSupport:
            L.insert(0, key)
    return L, supports

'''
Merge itemsets in L(k-item) to form a larger C((k+1)-item).
Two itemsets with identical first k-1 items are merged by 
appending the last item of each itemset to the k-1 items.
@param L: itemsets of k-item
@return: C itemsets of (k+1)-item
'''
def mergeLToFormLargerC(L):
    if (len(L) < 2):
        return []
    
    C = []
    k = len(L[0])
    lengthL = len(L)
    for i in range(lengthL):
        for j in range(i + 1, lengthL): 
            L1 = list(L[i])[:k - 1]
            L2 = list(L[j])[:k - 1]
            L1.sort()
            L2.sort()
            if L1 == L2:  # if first k-1 elements are equal
                C.append(L[i] | L[j])  # set union
    return C

'''
generate frequent itemsets:
D -> C1 -> L1 -> ... -> L(k-1) -> C(k) -> L(k) -> ... -> L(m)==null

D: dataset
C(k): candidate k-itemsets
L(k): large k-itemsets

@return: L_list [L1, L2, ...]
@return: supports
'''
def generateFrequentItemsets(dataset, minSupport=0.5):
    transactions = map(set, dataset)
    
    # generate L1
    C1 = createC1(transactions)
    L1, supports = filterCToFormL(C1, transactions, minSupport)
    L_list = [L1]  # [L1, L2, ...]
    
    k = 1  # current L
    L = L1
    while (len(L) > 0):  # if L is not empty, iterate
        C = mergeLToFormLargerC(L)
        L, supportL = filterCToFormL(C, transactions, minSupport)
        supports.update(supportL)
        L_list.append(L)
        k += 1
    return L_list, supports

'''
Mine frequent itemsets to extract association rules
@param L_list: [L1, L2, L3, ...]
@param supports: dict of itemset -> support 
'''
def mineAssociationRules(L_list, supports, minConf=0.7):
    rules = []
    for i in range(1, len(L_list)):  # only get the itemsets with two or more items
        for frequentItemset in L_list[i]:
            rules.extend(generateRulesForItemset(frequentItemset, supports, minConf))
    return rules

'''
HC: candidate H
HL: H with large confidence
'''
def generateRulesForItemset(itemset, supports, minConf):
    itemsetRules = []
    HC = [frozenset([item]) for item in itemset]  # initial consequent set H1 with 1-item
    sizeConsequent = 1  # consequent set size
    while (len(HC) <> 0 and sizeConsequent < len(itemset)):
        HL, rules = filterHCToFormHLAndGenerateRules(itemset, HC, supports, minConf)
        itemsetRules.extend(rules)
        HC = mergeLToFormLargerC(HL)  # create new candidates
        sizeConsequent += 1
    return itemsetRules

'''
filter HC to generate HL (consequent with large confidence),
and generate corresponding rules for HL
'''
def filterHCToFormHLAndGenerateRules(itemset, HC, supports, minConfidence=0.7):
    HL = []  # consequent list with large confidence
    rules = []
    for conseqent in HC:
        antecedent = itemset - conseqent
        confidence = supports[itemset] / supports[antecedent]
        if confidence >= minConfidence:
            HL.append(conseqent)
            rules.append((antecedent, conseqent, confidence))
    return HL, rules

def printRules(ruleList, itemMeaning):
    for ruleTuple in ruleList:
        for item in ruleTuple[0]:
            print itemMeaning[item]
        print "           -------->"
        for item in ruleTuple[1]:
            print itemMeaning[item]
        print "confidence: %f" % ruleTuple[2]
        print  # print a blank line

def itemMeaning():
    return {1:"toilet paper", 2:"diaper", 3:"milk", 4:"butter", 5:"beer"}

def test():
    L, supports = generateFrequentItemsets(dataset())
    print supports
    print L
    rules = mineAssociationRules(L, supports, minConf=0.7)
    print rules
    printRules(rules, itemMeaning())
    

if __name__ == "__main__":
    test()
