def ordenar_por_nota_global(filmes):
    #Ordena a lista de filmes em ordem decrescente da nota global.
  
    n = len(filmes)
    for i in range(n):
        max_idx = i
        for j in range(i + 1, n):
            if filmes[j][4] > filmes[max_idx][4]:  # Comparando média global
                max_idx = j
        # Troca os elementos
        filmes[i], filmes[max_idx] = filmes[max_idx], filmes[i]
    return filmes

def ordenar_por_nota_usuario_e_global(filmes):
   # Ordena a lista de filmes primeiro pela nota do usuário (filme[6]) desc,
   # e depois pela nota global (filme[4]) desc.
   
    n = len(filmes)
    for i in range(n):
        max_idx = i
        for j in range(i + 1, n):
            # Compara nota do usuário
            nota_user_j = filmes[j][6]
            nota_user_max = filmes[max_idx][6]

            if nota_user_j > nota_user_max:
                max_idx = j
            elif nota_user_j == nota_user_max:
                # Se iguais, compara pela nota global
                if filmes[j][4] > filmes[max_idx][4]:
                    max_idx = j

        filmes[i], filmes[max_idx] = filmes[max_idx], filmes[i]
    return filmes

