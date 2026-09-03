import re

class No:
    def __init__(self, valor, esquerda=None, direita=None):
        self.valor = valor
        self.esquerda = esquerda
        self.direita = direita

class Analisador:
    def __init__(self, texto):
        self.tokens = re.findall(r'\d+|\+|\-|\*|\/|\^|\(|\)', texto)
        self.pos = 0

    def atual(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def avancar(self):
        self.pos += 1

    def fator(self):
        token = self.atual()
        if token == '(':
            self.avancar()
            no = self.expressao()
            self.avancar()
            return no
        self.avancar()
        return No(token)

    def potencia(self):
        no = self.fator()
        while self.atual() == '^':
            operador = self.atual()
            self.avancar()
            direita = self.fator()
            no = No(operador, no, direita)
        return no

    def termo(self):
        no = self.potencia()
        while self.atual() in ('*', '/'):
            operador = self.atual()
            self.avancar()
            direita = self.potencia()
            no = No(operador, no, direita)
        return no

    def expressao(self):
        no = self.termo()
        while self.atual() in ('+', '-'):
            operador = self.atual()
            self.avancar()
            direita = self.termo()
            no = No(operador, no, direita)
        return no

def imprimir_arvore(no, prefixo="", eh_ultimo=True, eh_raiz=True):
    if not no:
        return
    
    if eh_raiz:
        print(f"({no.valor})" if no.valor in "+-*/^" else no.valor)
        prefixo_filhos = prefixo
    else:
        marcador = "└── " if eh_ultimo else "├── "
        print(prefixo + marcador + (f"({no.valor})" if no.valor in "+-*/^" else no.valor))
        prefixo_filhos = prefixo + ("    " if eh_ultimo else "│   ")
        
    if no.esquerda or no.direita:
        imprimir_arvore(no.esquerda, prefixo_filhos, False, False)
        imprimir_arvore(no.direita, prefixo_filhos, True, False)

def resolver(no, passos):
    if not no.esquerda and not no.direita:
        return float(no.valor)
        
    esq = resolver(no.esquerda, passos)
    dir = resolver(no.direita, passos)
    
    op = no.valor
    if op == '+':
        res = esq + dir
    elif op == '-':
        res = esq - dir
    elif op == '*':
        res = esq * dir
    elif op == '/':
        res = esq / dir
    elif op == '^':
        res = esq ** dir
        
    if isinstance(res, float) and res.is_integer():
        res = int(res)
    if isinstance(esq, float) and esq.is_integer():
        esq = int(esq)
    if isinstance(dir, float) and dir.is_integer():
        dir = int(dir)
        
    passos.append(f"Calcular {esq} {op} {dir} = {res}")
    return res

def principal():
    texto = input("Digite a expressao matematica: ")
    texto = texto.replace(" ", "")
    if not texto:
        return

    analisador = Analisador(texto)
    arvore = analisador.expressao()

    print("\n--- Estrutura da Arvore Sintatica ---")
    imprimir_arvore(arvore)

    print("\n--- Ordem de Calculo ---")
    passos = []
    resultado_final = resolver(arvore, passos)
    
    for i, passo in enumerate(passos, 1):
        print(f"Passo {i}: {passo}")
        
    print(f"Resultado Final: {resultado_final}")

if __name__ == '__main__':
    principal()