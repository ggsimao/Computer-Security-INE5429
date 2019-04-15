import random

def bbs(index, m, x0):
    if index == 0:
        return pow(x0, 2) % (m)
    elif index < 998:
        return pow(bbs(index-1, m, x0), 2) % (m)
    else:
        return pow(x0, pow(2, index) * carmichael(m)) % (m)

def carmichael(n):
    primeProducts = set()
    nTemp = n
    toAdd = 2
    while toAdd <= nTemp:
        print(toAdd)
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
    return int(returnValue)

def xorshift(size, state, a, b, c):
    state = state % 2**size
    oldsize = 2**state.bit_length()
    state ^= (state << a)
    state = state % oldsize
    state ^= (state >> b)
    oldsize = 2**state.bit_length()
    state ^= (state << c)
    state = state % oldsize

    if state == 0:
        state = 1

    if size > state.bit_length():
        overflow = size - state.bit_length()
        stateTemp = state % 2**overflow
        if stateTemp != 0:
            result = xorshift(overflow, stateTemp, a, b, c)
            state = (state << result.bit_length()) | (result)
        else:
            shiftAmount = state.bit_length() - overflow
            nextState = state >> shiftAmount
            result = xorshift(overflow, nextState, a, b, c)
            state = (state << result.bit_length()) | (result)

    return state

def solovay_strassen(number, accuracy):
    if number < 2:
        return False
    if number != 2 and number % 2 == 0:
        return False
    for i in range(accuracy):
        a = (random.getrandbits(number.bit_length()+1) % (number - 1)) + 1
        j = (number + jacobi(a, number)) % number
        m = modulo(a, int((number - 1) / 2), number)
        if j == 0 or m != j:
            return False
    return True
    # if number == 1:
    #     return False
    # if number == 2:
    #     return True
    # for k in range(accuracy):
    #     a = 0
    #     while a < 2:
    #         a = random.getrandbits(number.bit_length()+1) % number
    #     # print("////////////////")
    #     # print(a)
    #     x = jacobi(a, number)
    #     # print(x)
    #     # print((a**((number - 1) / 2)) % number)
    #     if x == 0 or (int(pow(a, (number - 1) / 2)) % number) != (x % number):
    #         return False
    # return True

def modulo(b, e, m):
    x = 1
    y = b
    while e > 0:
        if (e % 2) == 1:
            x = (x * y) % m
        y = (y * y) % m
        e = int(e / 2)
    return x % m

def jacobi(a, b):
    if a == 0:
        return 0
    j = 1
    if a < 0:
        a = -a
        if b % 4 == 3:
            j = -j
    if a == 1:
        return j
    while a != 0:
        if a < 0:
            a = -a
            if b % 4 == 3:
                j = -j
        while a % 2 == 0:
            a = a / 2
            if b % 8 == 3 or b % 8 == 5:
                j = -j
        temp = a
        a = b
        b = temp
        if a % 4 == 3 and b % 4 == 3:
            j = -j
        a = a % b
        if a > b / 2:
            a = a - b
    if b == 1:
        return j
    return 0

def miller_rabin(number, accuracy):
    if number == 1:
        return False
    if number == 2 or number == 3:
        return True
    d = number - 1
    r = 0
    while d % 2 == 0:
        d >>= 1
        r+=1
    a = 0
    for k in range(accuracy):
        a = 2 + (random.getrandbits(number.bit_length()+1) % (number - 3))
        x = (a**d) % number
        if x == 1 or x == number - 1:
            continue
        cont = False
        for i in range(r - 1):
            x = (x**2) % number
            if x == 1:
                return False
            if x == number - 1:
                cont = True
                break
        if cont:
            continue
        return False
    return True


if __name__ == "__main__":
    listofprimes = []
    for i in range(1, 100):
        if miller_rabin(i, 50):
            listofprimes.append(i)
    print(listofprimes)
    listofprimes = []
    for i in range(1, 100):
        if solovay_strassen(i, 50):
            listofprimes.append(i)
    print(listofprimes)
    # meuinputmarotao = "kkk"
    # while meuinputmarotao != "bbs" and input != "xorshift":
    #     meuinputmarotao = input("Escolha o gerador (bbs/xorshift): ")
    #     if meuinputmarotao == "bbs":
    #         p = 171669832909939861958115051553927939010937285163227785992618072924706999907173589031501998708227907986313758092365672654970079341235520693196160834863238835107985167297402467072359117491905351326487254879660501907553788181217053925870533532612131443518974810723306851639504210282064227773365630388224687721878830307935746864952347535940453520425766894194377078882259053722951569947299011706300591714448400965448853208406758662658635468006127800388270359337368217863551816447198854455118297856445738545696220598193729414883324936289986892456089922038323175653998357049731509017218180252307240382250611202127209333833665193365412639852270022552846842680264429527968361182748171512981494815905457530482912111558980692257384773663400516280431643129276148635276371940566959643
    #         q = 118530938077359217514788262274192349445270565577488943401931548764547409196924531259469473311379272479699652770078528240868238646814941249469020678356984479450452293100295999045108541336249743702062864056178767988659913205115029491637319098511757021243152171429570674889789646362575617523858902628920470156288225270457406516102220796187552449463862216865059493010641059606909427663130755742753065286918821701821230179146727654657775867749168745912077938014899917667798806480643599113093189245772245144641809156080199856663596294043362768366348528686481857456626654794287539531877226638139085957859063437378985167133884134696370802791884311031993006856649440664265360909325389294452782743811555401245128191080980055542893603339531202787930880737663189995794297800766304693
    #         seed = random.getrandbits(8)
    #         result = bbs(997, p * q, seed)
    #         print("Result = " + str(result))
    #         print("Size = " + str(result.bit_length()))
    #
    #     if meuinputmarotao == "xorshift":
    #         seed = random.getrandbits(4)
    #         result = xorshift(5, seed, 13, 17, 5) % 2**4
    #         print("Result = " + str(result))
    #         if solovay_strassen(result, 50):
    #             print("Probably prime")
    #         else:
    #             print("Compost")
