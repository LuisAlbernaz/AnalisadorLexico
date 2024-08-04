import re

palavrasReservadas = {'while', 'do'}
operadores = {'<', '=', '>', '+', '>=', '<=', '=='}
terminador = {';'}
identificadores = {'i', 'j'}
numeros = re.compile(r'^\d$')  
constantes = re.compile(r'^\d{2,}$')  

def identificar_token(token):
    if token in palavrasReservadas:
        return 'palavra reservada'
    elif token in operadores:
        return 'operador'
    elif token in terminador:
        return 'terminador'
    elif token in identificadores:
        return 'identificador'
    elif numeros.match(token):
        return 'número'
    elif constantes.match(token):
        return 'constante'
    else:
        return 'token desconhecido'

def analisador_lexico(codigo):
    tokens = re.findall(r'\w+|<=|>=|==|[<>=+;]', codigo)
    resultado = []
    simbolos = {}
    erros = []
    posicao = 0
    
    for token in tokens:
        tipo_token = identificar_token(token)
        linha, coluna = 0, posicao  
        if tipo_token == 'token desconhecido':
            erros.append(f"Erro: Token desconhecido '{token}' encontrado na posição ({linha}, {coluna}).")
        else:
            resultado.append((token, tipo_token, len(token), (linha, coluna)))
            if tipo_token in {'identificador', 'número', 'constante'} and token not in simbolos:
                simbolos[token] = len(simbolos) + 1
        posicao += len(token) + 1  
    
    return resultado, simbolos, erros

def gerar_saida(resultado, simbolos, erros, nome_arquivo="saida.txt"):
    with open(nome_arquivo, 'w') as f:
        f.write("Código do programa fonte: while i < 100 do i = i + j;\n\n")
        f.write("Tokens:\n")
        f.write("{:<10} {:<15} {:<10} {:<10}\n".format("token", "identificação", "tamanho", "posição (lin, col)"))
        for token, tipo, tamanho, posicao in resultado:
            f.write("{:<10} {:<15} {:<10} {}\n".format(token, tipo, tamanho, posicao))
        
        f.write("\nTabela de símbolos:\n")
        f.write("{:<10} {:<10}\n".format("índice", "símbolo"))
        for simbolo, indice in simbolos.items():
            f.write("{:<10} {:<10}\n".format(indice, simbolo))
        
        if erros:
            f.write("\nErros:\n")
            for erro in erros:
                f.write(f"{erro}\n")

codigo = "while i < 100 do i = i + j;"

resultado, simbolos, erros = analisador_lexico(codigo)

gerar_saida(resultado, simbolos, erros, "saida_codigo.txt")

print("Resultado para o código analisado:")
for token, tipo, tamanho, posicao in resultado:
    print(f"Token: {token}, Tipo: {tipo}, Tamanho: {tamanho}, Posição: {posicao}")

print("\nTabela de Símbolos:")
for simbolo, indice in simbolos.items():
    print(f"Índice: {indice}, Símbolo: {simbolo}")

print("\nErros:")
for erro in erros:
    print(erro)