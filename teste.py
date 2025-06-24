# Verifica se um caractere é um dígito (0 a 9)
def e_digito(c):
    return c >= '0' and c <= '9'

# Converte uma string numérica (como '123') para inteiro
# Retorna -1 se a string tiver qualquer caractere não numérico
def string_para_inteiro(s):
    num = 0
    for c in s:
        if not e_digito(c):
            return -1  # erro: string não numérica
        num = num * 10 + (ord(c) - ord('0'))  # conversão manual de char para número
    return num

# Remove espaços em branco no início e no final da string
def remover_espacos(s):
    inicio = 0
    while inicio < len(s) and s[inicio] == ' ':
        inicio += 1

    fim = len(s) - 1
    while fim >= 0 and s[fim] == ' ':
        fim -= 1

    if inicio > fim:
        return ""  # string vazia (só espaços)
    else:
        resultado = ""
        for i in range(inicio, fim + 1):
            resultado += s[i]
        return resultado

def consultas():
    while True:
        comando = input(">>> ")  # Lê o comando digitado

        if comando == "sair":
            break  # Encerra o programa

        # Verifica comando que começa com "prefixo "
        if len(comando) >= 8 and comando[:8] == "prefixo ":
            prefix = remover_espacos(comando[8:])  # remove espaços após o comando
            pesquisa_por_prefixo(prefix)

        # Verifica comando que começa com "user "
        elif len(comando) >= 5 and comando[:5] == "user ":
            parte = remover_espacos(comando[5:])
            user_id = string_para_inteiro(parte)
            if user_id != -1:
                pesquisa_por_usuario(user_id)
            else:
                print("UserID inválido.")

        # Verifica comando que começa com "top" e um número
        elif len(comando) >= 3 and comando[:3] == "top":
            i = 3
            num_str = ""

            # Lê todos os dígitos após "top"
            while i < len(comando) and e_digito(comando[i]):
                num_str += comando[i]
                i += 1

            n = string_para_inteiro(num_str)

            # Lê o gênero dentro das aspas simples
            genero = ""
            while i < len(comando) and comando[i] != "'":
                i += 1  # pula até encontrar a aspa de abertura
            i += 1  # pula a aspa inicial

            while i < len(comando) and comando[i] != "'":
                genero += comando[i]
                i += 1

            if n != -1:
                pesquisa_por_genero(n, genero)
            else:
                print("Comando top inválido.")

        # Verifica comando que começa com "tags" e contém duas strings entre aspas
        elif len(comando) >= 4 and comando[:4] == "tags":
            partes = []
            atual = ""
            lendo = False

            # Extrai duas strings entre aspas simples
            for c in comando[4:]:
                if c == "'":
                    lendo = not lendo
                    if not lendo:
                        partes.append(remover_espacos(atual))
                        atual = ""
                elif lendo:
                    atual += c

            if len(partes) == 2:
                pesquisa_por_tags(partes[0], partes[1])
            else:
                print("Formato esperado: tags 'tag1' 'tag2'")

        else:
            print("Comando não reconhecido.")
