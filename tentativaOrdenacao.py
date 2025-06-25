import random

def ordenar_por_nota_global(filmes, inicio=0, fim=None):
    if fim is None:
        fim = len(filmes) - 1
    if inicio < fim:
        p = particiona_hoare_global(filmes, inicio, fim)
        ordenar_por_nota_global(filmes, inicio, p)
        ordenar_por_nota_global(filmes, p + 1, fim)
def particiona_hoare_global(filmes, inicio, fim):
    pivot_index = random.randint(inicio, fim)
    pivot = filmes[pivot_index][4]  # nota global
    filmes[inicio], filmes[pivot_index] = filmes[pivot_index], filmes[inicio]

    i = inicio - 1
    j = fim + 1
    while True:
        while True:
            i += 1
            if filmes[i][4] > pivot:  # maior vai pro início
                continue
            break
        while True:
            j -= 1
            if filmes[j][4] < pivot:  # menor vai pro final
                continue
            break
        if i >= j:
            return j
        filmes[i], filmes[j] = filmes[j], filmes[i]

def ordenar_por_nota_usuario_e_global(filmes, inicio=0, fim=None):
    if fim is None:
        fim = len(filmes) - 1
    if inicio < fim:
        p = particiona_hoare_usuario_global(filmes, inicio, fim)
        ordenar_por_nota_usuario_e_global(filmes, inicio, p)
        ordenar_por_nota_usuario_e_global(filmes, p + 1, fim)

def particiona_hoare_usuario_global(filmes, inicio, fim):
    pivot_index = random.randint(inicio, fim)
    pivot = filmes[pivot_index]
    filmes[inicio], filmes[pivot_index] = filmes[pivot_index], filmes[inicio]

    i = inicio - 1
    j = fim + 1
    while True:
        while True:
            i += 1
            if compara_filmes(filmes[i], pivot) < 0:
                continue
            break
        while True:
            j -= 1
            if compara_filmes(filmes[j], pivot) > 0:
                continue
            break
        if i >= j:
            return j
        filmes[i], filmes[j] = filmes[j], filmes[i]

def compara_filmes(a, b):
    if a[6] > b[6]:
        return -1
    elif a[6] < b[6]:
        return 1
    else:
        if a[4] > b[4]:
            return -1
        elif a[4] < b[4]:
            return 1
        else:
            return 0
