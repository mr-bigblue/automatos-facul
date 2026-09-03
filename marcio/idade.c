#include <stdio.h>
#include <time.h>

int main() {
    char nome[100];
    int dia_nasc, mes_nasc, ano_nasc;
    int dia_atual, mes_atual, ano_atual;
    int idade;

    printf("Digite o seu nome: ");
    scanf(" %[^\n]", nome);

    printf("Digite a data de nascimento separada por espacos (DD MM AAAA): ");
    scanf("%d %d %d", &dia_nasc, &mes_nasc, &ano_nasc);

    time_t t = time(NULL);
    struct tm tm = *localtime(&t);
    dia_atual = tm.tm_mday;
    mes_atual = tm.tm_mon + 1
    ano_atual = tm.tm_year + 1900

    idade = ano_atual - ano_nasc;

    if (mes_atual < mes_nasc || (mes_atual == mes_nasc && dia_atual < dia_nasc)) {
        idade--;
    }

    printf("\n--- RESULTADO ---\n");
    printf("Nome: %s\n", nome);
    printf("Idade: %d anos\n", idade);

    if (idade >= 18) {
        printf("Status: Pode tirar a carteira de motorista.\n");
    } else {
        printf("Status: Nao pode tirar a carteira de motorista.\n");
    }

    int c;
    getchar();

    return 0;
}