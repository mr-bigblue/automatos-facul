import sys
from lexico import analisar_lexico

class AnalisadorSintatico:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.token_atual = self.tokens[self.pos] if self.tokens else None

    def obter_atributo(self, atributo):
        if not self.token_atual:
            return None
        if isinstance(self.token_atual, dict):
            return self.token_atual.get(atributo)
        return getattr(self.token_atual, atributo, None)

    def avancar(self):
        self.pos += 1
        self.token_atual = self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def erro(self, mensagem):
        if self.token_atual:
            linha = self.obter_atributo('linha')
            coluna = self.obter_atributo('coluna')
            print(f"Erro de Sintaxe (Parse Error): Linha {linha}, Coluna {coluna} - {mensagem}")
        else:
            print(f"Erro de Sintaxe (Parse Error): Fim de arquivo inesperado. {mensagem}")
        sys.exit(1)

    def consumir_valor(self, valor_esperado):
        valor_atual = self.obter_atributo('valor')
        if valor_atual == valor_esperado:
            self.avancar()
        else:
            self.erro(f"Esperado '{valor_esperado}', mas encontrado '{valor_atual if valor_atual else 'EOF'}'.")

    def analisar(self):
        while self.token_atual:
            tipo = self.obter_atributo('tipo')
            valor = self.obter_atributo('valor')
            
            if tipo == 'PREPROCESSADOR':
                self.avancar()
            elif tipo == 'PALAVRA_CHAVE' and valor in ['int', 'float', 'char', 'void'
                self.analisar_declaracao()
            elif tipo == 'PALAVRA_CHAVE' and valor == 'if':
                self.analisar_if()
            elif tipo == 'PALAVRA_CHAVE' and valor == 'return':
                self.analisar_return()
            elif tipo == 'IDENTIFICADOR':
                self.analisar_atribuicao_ou_chamada()
            elif tipo == 'DELIMITADOR' and valor == '}':
                self.avancar()
            else:
                self.erro(f"Instrucao nao reconhecida iniciada com '{valor}'.")
        print("Analise sintatica concluida com sucesso.")

    def analisar_declaracao(self):
        self.avancar()
        tipo = self.obter_atributo('tipo')
        if tipo == 'IDENTIFICADOR':
            self.avancar()
        else:
            self.erro("Esperado um identificador apos o tipo.")
            
        valor = self.obter_atributo('v
        if valor == '=':
            self.avancar()
            self.analisar_expressao()
        elif valor == '(':
            self.avancar()
            self.consumir_valor(')')
            if self.obter_atributo('valor') == '{':
                self.avancar()
                return
                
        valor = self.obter_atributo('valor')
        if valor == ';':
            self.avancar()
        else:
            self.erro("Esperado delimitador ';' no final da instrucao.")

    def analisar_expressao(self):
        tipo = self.obter_atributo('tipo')
        if tipo in ['NUMERO_INTEIRO', 'NUMERO_REAL', 'IDENTIFICADOR', 'TEXTO', 'CARACTERE']:
            self.avancar()
            while self.token_atual and self.obter_atributo('tipo') == 'OPERADOR':
                self.avancar()
                tipo = self.obter_atributo('tipo')
                if tipo in ['NUMERO_INTEIRO', 'NUMERO_REAL', 'IDENTIFICADOR']:
                    self.avancar(
                else
                    self.erro("Esperado valor ou variavel apos o operador."...
        else:
            self.erro("Esperado um valor ou expressao valida.")

    def analisar_atribuicao_ou_chamada(self):
        self.avancar()
        valor = self.obter_atributo('valor')
        
        if valor == '=':
            self.avancar()
            self.analisar_expressao()
            self.consumir_valor(';')
        elif valor == '(':
            self.avancar()
            if self.obter_atributo('valor') != ')':
                self.analisar_expressao()
            self.consumir_valor(')')
            self.consumir_valor(';')
        else:
            self.erro("Esperado atribuicao '=' ou chamada de funcao '()'.")

    def analisar_if(self):
        self.consumir_valor('if')
        valor = self.obter_atributo('valor')
        
        if valor == '(':
            self.avancar()
        else:
            self.erro("Esperado delimitador '(' apos instrucao 'if'.")
            
        self.analisar_expressao()
        self.consumir_valor(')')
        self.consumir_valor('{')

    def analisar_return(self):
        self.consumir_valor('return')
        self.analisar_expressao()
        self.consumir_valor(';')

def principal():
    if len(sys.argv) < 2:
        print("Uso: python sintatico.py <arquivo.c>")
        sys.exit(1)
        
    arquivo = sys.argv[1]
    try:
        with open(arquivo, 'r', encoding='utf-8') as f:
            codigo = f.read()
    except FileNotFoundError:
        print(f"Arquivo '{arquivo}' nao encontrado.")
        sys.exit(1)
        
    tokens, erros_lexicos = analisar_lexico(codigo)
    
    if erros_lexicos:
        for erro in erros_lexicos:
            print(erro)
        sys.exit(1)
        
    parser = AnalisadorSintatico(tokens)
    parser.analisar()

if __name__ == '__main__':
    principal()