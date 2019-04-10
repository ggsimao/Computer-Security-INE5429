import random

def bbs(index, p, q, x0):
    return pow(x0, pow(2, index) * carmichael(p*q)) % (p * q)

def carmichael(n):
    primeProducts = set()
    nTemp = n
    toAdd = 2
    while toAdd <= nTemp:
        if (nTemp / toAdd) < 1:
            break
        if (nTemp / toAdd).is_integer():
            nTemp = nTemp / toAdd
            primeProducts.add(toAdd)
        else:
            toAdd+=1
    returnValue = 1
    for p in primeProducts:
        returnValue *= (1 - 1/p)
    returnValue *= n
    if n >= 8 and ((n & (n - 1)) == 0):
        returnValue /= 2
    print("returnValue = " + str(int(returnValue)))
    return int(returnValue)

if __name__ == "__main__":
    print(str(bbs(5, 67, 89, random.getrandbits(8))))
