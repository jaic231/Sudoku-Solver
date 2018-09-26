import time, sys
possibilities = {"1", "2", "3", "4", "5", "6", "7", "8", "9"}
size = 9
dic = {}
connected = {}
for i in range(3 * size): dic[i] = set()
for i in range(size**2):
    row, col = i//size, i%size
    block = 3 * (row//3) + (col//3)
    dic[row].add(i)
    dic[col+size].add(i)
    dic[block+2*size].add(i)
for i in range(size**2):
    row, col = i//size, i%size
    block = 3 * (row//3) + (col//3)
    connected[i] = dic[row].union(dic[col+size]).union(dic[block+2*size])
    connected[i].remove(i)

def findSmall(puz):
    index, setlen, finSymb = -1, size + 1, set()
    for i in range(len(puz)):
        if puz[i] != ".": continue
        poss = possibilities - {puz[index] for index in connected[i]}
        if not poss: return "","",""
        elif len(poss) == 1: puz = ''.join([puz[:i], poss.pop(), puz[i+1:]])
        elif len(poss) < setlen: index, setlen, finSymb = i, len(poss), poss
    return puz, index, finSymb

def findSym(puz):
    symb, minLen, finPoss = "0", size**2 + 1, set()
    for cs in dic.values():
        inds = {}
        for idx in cs:
            if puz[idx] != ".": continue
            poss = possibilities - {puz[index] for index in connected[idx]}
            if not poss: return "",""
            for sym in poss:
                try: inds[sym].add(idx)
                except KeyError: inds[sym] = {idx}
        if not inds: continue
        for sym, ind in inds.items():
            if len(ind) == 1: return sym, ind
            if len(ind) < minLen and len(ind) > 0: finPoss, minLen, symb = ind, len(ind), sym
    return symb, finPoss

def bruteForce(puz):
    puz, ind, symPoss = findSmall(puz)
    if not puz: return ""
    if "." not in puz: return puz
    symb, indPoss = findSym(puz)
    if not symb: return ""
    if len(symPoss) <= len(indPoss):
        for i in symPoss:
            subpuz = ''.join([puz[:ind], i, puz[ind+1:]])
            bF = bruteForce(subpuz)
            if bF: return bF
    else:
        for i in indPoss:
            subpuz = ''.join([puz[:i], symb, puz[i+1:]])
            bF = bruteForce(subpuz)
            if bF: return bF
    return ""

def main():
    totstart = time.clock()
    if len(sys.argv) > 1:
        puz = sys.argv[1]
        print(bruteForce(puz))
    else:
        with open("sudpuz.txt") as f:
            for line in f:
                print(bruteForce(line[:-1]))
    print(str(time.clock() - totstart) + "s")
main()
