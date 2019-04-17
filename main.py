import random
import time

#   index: índice do elemento da sequência desejado
#   m: produto dos dois primos escolhidos para cálculo da sequência
#   x0: primeiro número da sequência (semente)
#   timecheck: se não for None, imprime o tempo levado para gerar o número
def bbs(index, m, x0, timecheck = None):
    if timecheck != None:
        timeStart = time.time()
    if index == 0: # caso especial
        return x0
    if index == 1: # fim da recursão
        return pow(x0, 2) % (m)
    else:
        result = pow(bbs(index-1, m, x0), 2, m) # aplicação da fórmula
        if timecheck != None:
            print(time.time() - timeStart)
        return result

#   state: numero inicial a ser shiftado
#   a, b, c: parametros de cada shift a ser aplicado (numero de casas decimais)
#   size: tamanho desejado do numero gerado (nao alterara o tamanho do resultado se for None)
#   timecheck: se nao for None, imprime o tempo levado para gerar o numero
def xorshift(state, a, b, c, size = None, timecheck = None):
    if timecheck != None:
        timeStart = time.time()
    state = state % 2**size
    state ^= (state << a) # aplicacao da primeira operacao
    state ^= (state >> b) # aplicacao da segunda operacao
    state ^= (state << c) # aplicacao da terceira operacao

    if size == None:
        return state

    if size < state.bit_length(): # reduz o numero ao tamanho desejado, caso seja muito grande
        state = state % 2**size
    elif size > state.bit_length(): # se o resultado for menor que o tamanho desejado,
                                     # gera-se mais uma parte do numero e a concatena
                                     # com o resultado anterior
        overflow = size - state.bit_length() # tamanho restante
        result = xorshift(state, a, b, c, overflow)
        state = (state << result.bit_length()) | (result)

    if timecheck != None:
        print(time.time() - timeStart)
    return state

# def solovay_strassen(number, accuracy):
#     if number < 2:
#         return False
#     if number != 2 and number % 2 == 0:
#         return False
#     for i in range(accuracy):
#         a = (random.getrandbits(number.bit_length()+1) % (number - 1)) + 1
#         j = (number + jacobi(a, number)) % number
#         m = modulo(a, int((number - 1) / 2), number)
#         if j == 0 or m != j:
#             return False
#     return True
#     # if number == 1:
#     #     return False
#     # if number == 2:
#     #     return True
#     # for k in range(accuracy):
#     #     a = 0
#     #     while a < 2:
#     #         a = random.getrandbits(number.bit_length()+1) % number
#     #     # print("////////////////")
#     #     # print(a)
#     #     x = jacobi(a, number)
#     #     # print(x)
#     #     # print((a**((number - 1) / 2)) % number)
#     #     if x == 0 or (int(pow(a, (number - 1) / 2)) % number) != (x % number):
#     #         return False
#     # return True
#
# def modulo(b, e, m):
#     x = 1
#     y = b
#     while e > 0:
#         if (e % 2) == 1:
#             x = (x * y) % m
#         y = (y * y) % m
#         e = int(e / 2)
#     return x % m
#
# def jacobi(a, b):
#     if a == 0:
#         return 0
#     j = 1
#     if a < 0:
#         a = -a
#         if b % 4 == 3:
#             j = -j
#     if a == 1:
#         return j
#     while a != 0:
#         if a < 0:
#             a = -a
#             if b % 4 == 3:
#                 j = -j
#         while a % 2 == 0:
#             a = a / 2
#             if b % 8 == 3 or b % 8 == 5:
#                 j = -j
#         temp = a
#         a = b
#         b = temp
#         if a % 4 == 3 and b % 4 == 3:
#             j = -j
#         a = a % b
#         if a > b / 2:
#             a = a - b
#     if b == 1:
#         return j
#     return 0

#   number: numero a ser testado
#   accuracy: numero de possiveis testemunhas
def fermat(number, accuracy):
    if number == 1: # caso especial
        return False
    accuracylist = []
    while len(accuracylist) < accuracy:
        a = random.randint(number+1, number**2) # gera a possivel testemunha
        while a % number == 0: # continua tentando gerar ate' que nao seja divisivel por number
            a = random.randint(number+1, number**2)
        accuracylist.append(a)
    for a in accuracylist:
        if pow(a, number - 1, number) != 1: # aplica o teste
                return False
    return True

#   number: numero a ser testado
#   accuracy: acuracia do teste
def miller_rabin(number, accuracy):
    if number == 1: # casos especiais
        return False
    if number == 2 or number == 3: # casos especiais
        return True
    # a secao abaixo escreve number como 2**r * d - 1
    ##############################
    d = number - 1
    r = 0
    while d % 2 == 0:
        d >>= 1
        r+=1
    ##############################
    a = 0
    for k in range(accuracy):
        a = random.randint(2, number - 1) # pega a aleatorio entre 2 e number - 1
        x = pow(a, d, number)
        if x == 1 or x == number - 1: # casos em que a primeira proposicao se satisfaz
            continue
        cont = False
        for i in range(r - 1):
            x = pow(x, 2, number)
            if x == number - 1: # segunda proposicao se satisfaz
                cont = True
                break
        if cont:
            continue
        return False # segunda proposicao nao se satisfez para nenhum i entre 0 e r-1
    return True


if __name__ == "__main__":
    sizelist = [40, 56, 80, 128, 168, 224, 256, 512, 1024, 2048, 4096]
    for size in sizelist:
        result = 0
        compost = True
        timeStart = time.time()
        while compost:
            a = random.randint(1, size / 2)
            c = random.randint(1, size / 2)
            b = random.randint(a + c, size)
            result = xorshift(random.randint(2**(size-1), 2**size), a, b, c, size)
            if result.bit_length() != size:
                timeStart = time.time()
                continue
            compost = not fermat(result, 10)
        print(time.time() - timeStart)
        print(result)
        print(result.bit_length())
