import json
import os
from datetime import datetime
from collections import defaultdict

def obter_arquivo_vendas(mes=None):   
    if mes is None:
        mes = datetime.now().strftime("%Y-%m")
    return f"vendas_{mes}.json"

def carregar_vendas(nome_arquivo):
    print(f"🕵️ Tentando carregar o arquivo: {nome_arquivo}") 
    if os.path.exists(nome_arquivo):
        print("✅ Arquivo encontrado!") 
        try:
            with open(nome_arquivo, "r", encoding="utf-8") as f:
                if os.path.getsize(nome_arquivo) > 0:
                    return json.load(f)
                else:
                    print("❌ ERRO: O arquivo foi encontrado, mas está vazio.") 
                    return []
        except json.JSONDecodeError:
            print("❌ ERRO: O arquivo foi encontrado, mas o conteúdo JSON é inválido.") 
            return []
        except FileNotFoundError: 
            print("❌ ERRO: Arquivo não encontrado (verificação secundária).") 
            return []
    else:
        print("❌ Arquivo NÃO encontrado neste local.") 
        print(f"   O script está rodando no diretório: {os.getcwd()}")
    return []

def salvar_vendas(vendas, nome_arquivo):
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        json.dump(vendas, f, ensure_ascii=False, indent=4)

def formatar_dinheiro(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def exibir_vendas(nome_arquivo):
    vendas = carregar_vendas(nome_arquivo)

    if not vendas:
        print("\n🔹 Nenhuma venda registrada neste período.")
        return []

    print("\n=== 📜 LISTA DE VENDAS ===")
    for i, venda in enumerate(vendas):
        print(f"{i+1}️⃣ Cliente: {venda['cliente']} - Valor: {formatar_dinheiro(venda['valor'])}")

    return vendas

def apagar_venda(nome_arquivo):
    vendas = exibir_vendas(nome_arquivo)

    if not vendas:
        return

    try:
        indice = int(input("\nDigite o número da venda que deseja apagar: ").strip()) - 1
        if 0 <= indice < len(vendas):
            venda_removida = vendas.pop(indice)
            salvar_vendas(vendas, nome_arquivo)
            print(f"\n✅ Venda de {formatar_dinheiro(venda_removida['valor'])} para {venda_removida['cliente']} foi removida.")
        else:
            print("\n❌ Número inválido.")
    except ValueError:
        print("\n❌ Entrada inválida. Digite um número válido.")

def exibir_relatorio(nome_arquivo):
    vendas = carregar_vendas(nome_arquivo)

    if not vendas:
        print("\n🔹 Nenhuma venda registrada neste período.")
        return

    total_vendas = sum(venda["valor"] for venda in vendas)
    quantidade_vendas = len(vendas)
    media_vendas = total_vendas / quantidade_vendas
    comissão_vendedores = total_vendas * 0.03  # Comissão de 3% do total das vendas
    clientes_frequencia = defaultdict(int)
    clientes_valor = defaultdict(float)

    for venda in vendas:
        clientes_frequencia[venda["cliente"]] += 1
        clientes_valor[venda["cliente"]] += venda["valor"]

    cliente_mais_pedidos = max(clientes_frequencia, key=clientes_frequencia.get, default="Nenhum")
    cliente_mais_gastou = max(clientes_valor, key=clientes_valor.get, default="Nenhum")

    print("\n=== 📊 RELATÓRIO DE VENDAS ===")
    print(f"🟢 Total de vendas: {formatar_dinheiro(total_vendas)}")
    print(f"📌 Quantidade de vendas: {quantidade_vendas}")
    print(f"📊 Média de vendas: {formatar_dinheiro(media_vendas)}")
    print(f"⬆️ Maior venda: {formatar_dinheiro(max([v['valor'] for v in vendas], default=0))}")
    print(f"⬇️ Menor venda: {formatar_dinheiro(min([v['valor'] for v in vendas], default=0))}")
    print(f"📦 Cliente com mais pedidos: {cliente_mais_pedidos} ({clientes_frequencia[cliente_mais_pedidos]} pedidos)")
    print(f"💵 Cliente que mais gastou: {cliente_mais_gastou} ({formatar_dinheiro(clientes_valor[cliente_mais_gastou])})")
    print(f"💸 Comissão total do vendedor: {formatar_dinheiro(comissão_vendedores)}")

def comparar_meses(mes1, mes2):
    arquivo1 = obter_arquivo_vendas(mes1)
    arquivo2 = obter_arquivo_vendas(mes2)

    vendas1 = carregar_vendas(arquivo1)
    vendas2 = carregar_vendas(arquivo2)

    total1 = sum(venda["valor"] for venda in vendas1)
    total2 = sum(venda["valor"] for venda in vendas2)

    print("\n=== 📊 COMPARAÇÃO DE MESES ===")
    print(f"📆 {mes1}: {formatar_dinheiro(total1)}")
    print(f"📆 {mes2}: {formatar_dinheiro(total2)}")

    if total1 > total2:
        print(f"✅ O mês {mes1} teve mais vendas!")
    elif total2 > total1:
        print(f"✅ O mês {mes2} teve mais vendas!")
    else:
        print("⚖️ Ambos os meses tiveram o mesmo faturamento.")

while True:
    print("\n===== MENU =====")
    print("1️⃣ Adicionar novas vendas no mês atual")
    print("2️⃣ Ver todas as vendas do mês atual")
    print("3️⃣ Apagar uma venda do mês atual")
    print("4️⃣ Ver relatório do mês atual")
    print("5️⃣ Ver relatório de um mês específico")
    print("6️⃣ Comparar dois meses")
    print("7️⃣ Sair")

    opcao = input("Escolha uma opção: ").strip()
    arquivo_vendas_atual = obter_arquivo_vendas()

    if opcao == "1":
        vendas = carregar_vendas(arquivo_vendas_atual)

        while True:
            cliente = input("Digite o nome do cliente (ou 'sair' para finalizar): ").strip()
            if cliente.lower() == "sair":
                break

            valor = input(f"Digite o valor da venda para {cliente}: ").strip()
            try:
                valor = float(valor)
                if valor >= 0:
                    vendas.append({"valor": valor, "cliente": cliente})
                else:
                    print("❌ O valor deve ser positivo.")
            except ValueError:
                print("❌ Entrada inválida. Digite um número válido.")

        salvar_vendas(vendas, arquivo_vendas_atual)

    elif opcao == "2":
        exibir_vendas(arquivo_vendas_atual)

    elif opcao == "3":
        apagar_venda(arquivo_vendas_atual)

    elif opcao == "4":  # Ver relatório do mês atual
        exibir_relatorio(arquivo_vendas_atual)

    elif opcao == "5":
        mes = input("Digite o mês que deseja visualizar (YYYY-MM): ").strip()
        arquivo_escolhido = obter_arquivo_vendas(mes)
        if os.path.exists(arquivo_escolhido):
            exibir_relatorio(arquivo_escolhido)
        else:
            print("❌ Nenhum relatório encontrado para esse período.")

    elif opcao == "6":
        mes1 = input("Digite o primeiro mês para comparação (YYYY-MM): ").strip()
        mes2 = input("Digite o segundo mês para comparação (YYYY-MM): ").strip()
        comparar_meses(mes1, mes2)

    elif opcao == "7":
        print("🚪 Saindo do programa...")
        break

    else:
        print("❌ Opção inválida. Tente novamente.")