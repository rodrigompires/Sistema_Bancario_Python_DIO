from datetime import datetime
import json
import os


clientes = []
contas_clientes = []
ARQUIVO_DADOS = "banco_de_dados.json"

def cadastrar_cliente ():
    print("\n=== CADASTRO DE CLIENTE ===\n")

    # Para cada campo, fiz uma validação de campo vazio, digito numerico e etc
    while True:
        try:
            nome_cliente = input("Nome Completo: ").strip().title()
            if nome_cliente.isdigit():
                raise TypeError("O nome não pode ser um número!")
            if not nome_cliente:
                raise ValueError("O campo não pode ficar em branco!")
            break
        except (ValueError, TypeError) as e:
            print(f'❌ ERRO: {e} Tente novamente!')

    while True:
        try:
            data_nascimento = input("Data de Nascimento (ex: ddmmaaa): ").strip()
            if not data_nascimento.isdigit() or len(data_nascimento) != 8:
                raise ValueError("Data inválida! Deve conter apenas números e 8 dígitos!")

            dia = int(data_nascimento[0:2])
            mes = int(data_nascimento[2:4])
            ano = int(data_nascimento[4:8])

            if not (1 <= dia <= 31 and 1 <= mes <= 12 and 1900 <= ano <= 2025):
                raise ValueError("Data fora do intervalo válido!")
            
            data_nascimento_formatada = f'{dia:02d}/{mes:02d}/{ano}'
            break
        except ValueError as e:
            print(f'❌ ERRO: {e}')

    while True:
        try:
            cpf_cliente = input("CPF: Digite apenas números (ex: 11111111111): ").strip()
            if not cpf_cliente.isdigit() or len(cpf_cliente) != 11:
                raise ValueError ("❌ CPF Inválido! Deve conter apenas números e ter 11 dígitos.")
            
            for cliente in clientes:
                if cliente["cpf"] == cpf_cliente:
                    raise ValueError("⚠️ Este CPF já está cadastrado!")
            break
        except ValueError as e:
            print(f'❌ Erro: {e}')
    
    while True:
        try:
            logradouro = input("Logradouro: ").strip().title()
            if not logradouro:
                raise ValueError("O campo logradouro não pode ser vazio!")
            break
        except ValueError as e:
            print(f"❌ ERRO: {e} Tente novamente!")

    while True:
        try:
            numero = input("Número: ").strip()
            if not numero:
                raise ValueError("O campo número não pode ser vazio!")
            break
        except ValueError as e:
            print(f"❌ ERRO: {e} Tente novamente!")

    while True:
        try:
            bairro = input("Bairro: ").strip().title()
            if not bairro:
                raise ValueError("O campo bairro não pode ser vazio!")
            break
        except ValueError as e:
            print(f"❌ ERRO: {e} Tente novamente!")
    
    while True:
        try:
            cidade = input("Cidade: ").strip().title()
            if not cidade:
                raise ValueError("O campo cidade não pode ser vazio!")
            break
        except ValueError as e:
            print(f"❌ ERRO: {e} Tente novamente!")
    
    while True:
        try:
            sigla_estado = input("Sigla do Estado (ex: SP, RJ, MG): ").strip().title()
            if not sigla_estado:
                raise ValueError("O campo estado não pode ser vazio!")
            if len(sigla_estado) != 2 or sigla_estado.isdigit():
                raise ValueError("A sigla do estado deve ter exatamente 2 letras!")
            break
        except ValueError as e:
            print(f"❌ ERRO: {e} Tente novamente!")
    
    endereco = f'{logradouro}, {numero}, {bairro}, {cidade} / {sigla_estado}'

    cliente = {
        "nome": nome_cliente,
        "data_nascimento": data_nascimento_formatada,
        "cpf": cpf_cliente,
        "endereco": endereco
    }

    clientes.append(cliente)
    print(f'\n✅ Cliente {nome_cliente} cadastrado com sucesso!')
    salvar_dados()


def criar_conta_cliente ():
    print("\n=== CRIAÇÃO DE CONTA ===\n")

    while True:
        try:
            cpf = input("Informe o CPF do cliente (somente números): ").strip()

            if not cpf.isdigit():
                raise ValueError("Digite apenas números:")
            
            cliente = None
            for cl in clientes:
                if cl["cpf"] == cpf:
                    cliente = cl
                    break
            
            if not cliente:
                print(f'\n⚠️  Cliente não encontrado. Cadastre o cliente primeiro.')
                return
            

            agencia = "0001"
            numero_conta = len(contas_clientes) + 1
            saldo = 0
            conta = {
                "agencia": agencia,
                "numero_conta": numero_conta,
                "cliente": cliente,
                "saldo": saldo
            }
            contas_clientes.append(conta)
            print(f"\n✅ Conta criada com sucesso!")
            print(f"\n🏦 Agência: {agencia} | Conta nº: {numero_conta}")
            print(f"👤 Titular: {cliente['nome']}")
            print(f"💰 Saldo: {saldo}")
            break
        except ValueError as e:
            print(f"Erro: {e}. Tente novamente!")
        finally:
            print("\n=== FIM CRIAÇÃO DE CONTA ===\n")
    salvar_dados()


def gerar_numero_doc():
    """Crei essa função para que seja gerado um número de documento 
    sequencial para cada transação, 
    independente se for saque ou depósito
    """

    total_transacoes_banco = 0

    for conta in contas_clientes:
        total_transacoes_banco += len(conta.get("transacoes", []))
    
    proximo_doc = total_transacoes_banco + 1
    return str(proximo_doc).zfill(5)


def depositar(numero_conta, valor, transacao, /):
    if not isinstance(numero_conta, int):
        raise TypeError("❌ O número da conta deve ser um inteiro!")
    if not isinstance(valor, (int, float)):
        raise TypeError("❌ O valor deve ser numérico!")
    if valor <= 0:
        raise ValueError("❌ O valor do depósito deve ser maior que zero!")
    if not isinstance(transacao, str) or not transacao.strip():
        raise ValueError("❌ A descrição do depósito não pode estar vazia!")

    conta_encontrada = None
    for conta in contas_clientes:
        if conta["numero_conta"] == numero_conta:
            conta_encontrada = conta
            break

    if conta_encontrada is None:
        raise LookupError(f"⚠️  Conta nº {numero_conta} não encontrada.")
    
    if "transacoes" not in conta_encontrada:
        conta_encontrada["transacoes"] = []

    doc_numero = gerar_numero_doc()

    conta_encontrada["saldo"] += valor

    
    conta_encontrada["transacoes"].append({
        "doc": doc_numero,
        "tipo": "DEPÓSITO",
        "valor": valor,
        "descricao": transacao.strip(),
        "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    })

    print("\n✅ Depósito realizado com sucesso!")
    print(f"🏦 Conta nº: {numero_conta}")
    print(f"💰 Novo saldo: R$ {conta_encontrada['saldo']:.2f}")
    print("\n===========================\n")
    salvar_dados()


def sacar (*, numero_conta, valor_saque, transacao):
    if not isinstance(numero_conta, int):
        raise TypeError("⚠️ O número da conta deve ser um inteiro.")
    if not isinstance(valor_saque, (int, float)):
        raise TypeError("⚠️ O valor do saque deve ser numérico.")
    if valor_saque <= 0:
        raise ValueError("⚠️ O valor do saque deve ser maior que zero.")
    
    conta_encontrada = None
    for conta in contas_clientes:
        if conta["numero_conta"] == numero_conta:
            conta_encontrada = conta
            break

    if conta_encontrada is None:
        raise LookupError(f"⚠️ Conta nº {numero_conta} não encontrada.")
    
    saldo_atual = conta_encontrada["saldo"]

    if saldo_atual <= 0:
        raise ValueError(f"⚠️  O saldo da conta nº {numero_conta} é zero. Saque não permitido.")
    if valor_saque > saldo_atual:
        raise ValueError(f"⚠️ Saque de R$ {valor_saque:.2f} excede o saldo disponível de R$ {saldo_atual:.2f}.")
    
    
    if "transacoes" not in conta_encontrada:
        conta_encontrada["transacoes"] = []
    
    doc_numero = gerar_numero_doc()

    conta_encontrada["saldo"] -= valor_saque
    
    conta_encontrada["transacoes"].append({
        "doc": doc_numero,
        "tipo": "SAQUE",
        "valor": -valor_saque,
        "descricao": transacao,
        "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    })

    # Exibir resultado
    print("\n✅ Saque realizado com sucesso!")
    print(f"\n🏦 Conta nº: {numero_conta}")
    print(f"📄 DOC: {doc_numero}")
    print(f"💸 Valor sacado: R$ {valor_saque:.2f}")
    print(f"💰 Saldo atual: R$ {conta_encontrada['saldo']:.2f}")
    print("\n===========================\n")
    salvar_dados()


def exibir_extrato(numero_conta, *, incluir_detalhes=True):
    conta_encontrada = None
    for conta in contas_clientes:
        if conta["numero_conta"] == numero_conta:
            conta_encontrada = conta
            break

    if conta_encontrada is None:
        raise LookupError(f"⚠️ Conta nº {numero_conta} não encontrada.")

    if "transacoes" not in conta_encontrada:
        conta_encontrada["transacoes"] = []

    cliente = conta_encontrada['cliente']
    nome_cliente = cliente['nome'].upper()
    agencia = conta_encontrada['agencia']
    numero_conta = conta_encontrada['numero_conta']
    limite = conta_encontrada.get("limite", 0.00)
    saldo_atual = conta_encontrada['saldo']

    
    largura_data = 20
    largura_historico = 35
    largura_doc = 10
    largura_valor = 15

    largura_total = largura_data + largura_historico + largura_doc + largura_valor

    
    print("\n" + " " * ((largura_total - 14)//2) + "EXTRATO BANCÁRIO")
    print("-" * largura_total)

    
    if incluir_detalhes:
        print(f"Cliente: {nome_cliente}")
        print(f"Banco: REAL MADRUGA")
        print(f"Agência: {agencia}")
        print(f"Conta: {numero_conta}")
        print("-" * largura_total)

    
    print(f"{'DATA':<{largura_data}}{'HISTÓRICO':<{largura_historico}}"
          f"{'DOC':<{largura_doc}}{'VALOR':>{largura_valor}}")
    print("-" * largura_total)

    transacoes = conta_encontrada["transacoes"]

    if not transacoes:
        print("Nenhuma movimentação registrada.")
    else:
        transacoes_ordenadas = sorted(transacoes, key=lambda t: t.get("data-hora", ""))

        for t in transacoes_ordenadas:
            data = t.get("data", datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
            tipo = t.get("tipo", "MOVIMENTAÇÃO").upper()
            descricao = t.get("descricao", "")
            valor = abs(t.get("valor", 0))
            sinal = "C" if t.get("valor", 0) > 0 else "D"
            doc = t.get("doc", "00000")

            historico = tipo
            if descricao:
                historico += f" - {descricao}"
            historico = historico[:largura_historico]

            
            valor_formatado = f"{valor:,.2f} {sinal}"

            print(f"{data:<{largura_data}}{historico:<{largura_historico}}"
                  f"{doc:<{largura_doc}}{valor_formatado:>{largura_valor}}")

    
    print("-" * largura_total)
    print(f"{'SALDO ATUAL:':<{largura_data + largura_historico + largura_doc}}"
          f"{saldo_atual:>{largura_valor},.2f}")
    print(f"{'LIMITE:':<{largura_data + largura_historico + largura_doc}}"
          f"{limite:>{largura_valor},.2f}")
    print(f"{'SALDO + LIMITE:':<{largura_data + largura_historico + largura_doc}}"
          f"{(saldo_atual + limite):>{largura_valor},.2f}")
    print("-" * largura_total + "\n")


def listar_clientes():
    carregar_dados()

    if not clientes:
        print("\nNenhum cliente cadastrado ainda.")
        return

    
    largura_max = 0
    for cliente in clientes:
        linhas = [
            f"CLIENTE: {cliente['nome']}",
            f"CPF: {cliente['cpf']}",
            f"DATA NASC: {cliente['data_nascimento']}",
            f"ENDEREÇO: {cliente['endereco']}"
        ]
        largura_max = max(largura_max, max(len(linha) for linha in linhas))

    titulo = "LISTA DE CLIENTES - BANCO REAL MADRUGA"
    largura_total = max(largura_max, len(titulo)) + 4
    separador = "-" * largura_total

    
    print("\n" + titulo.center(largura_total))
    print(separador + "\n")

    
    for cliente in clientes:
        linhas = [
            f"CLIENTE: {cliente['nome']}",
            f"CPF: {cliente['cpf']}",
            f"DATA NASC: {cliente['data_nascimento']}",
            f"ENDEREÇO: {cliente['endereco']}"
        ]
        for linha in linhas:
            print(linha)
        print(separador + "\n")

    print("FIM LISTA DE CLIENTES".center(largura_total))
    print(separador + "\n")


def listar_contas():
    carregar_dados()

    if not contas_clientes:
        print("\nNenhuma conta cadastrada ainda.")
        return

    largura_max = 0
    for conta in contas_clientes:
        cliente = conta["cliente"]
        # saldo = conta.get("saldo", 0.0)
        # limite = conta.get("limite", 0.0)
        linhas = [
            f"AGÊNCIA: {conta['agencia']}",
            f"CONTA: {conta['numero_conta']}",
            f"TITULAR: {cliente['nome']}",
            f"CPF: {cliente['cpf']}",
            f"ENDEREÇO: {cliente['endereco']}",
            # f"SALDO ATUAL: R$ {saldo:,.2f}",
            # f"LIMITE: R$ {limite:,.2f}",
            # f"SALDO + LIMITE: R$ {saldo + limite:,.2f}"
        ]
        largura_max = max(largura_max, max(len(linha) for linha in linhas))

    titulo = "LISTA DE CONTAS - BANCO REAL MADRUGA"
    largura_total = max(largura_max, len(titulo)) + 4
    separador = "-" * largura_total

    print("\n" + titulo.center(largura_total))
    print(separador + "\n")

    for conta in contas_clientes:
        cliente = conta["cliente"]
        saldo = conta.get("saldo", 0.0)
        limite = conta.get("limite", 0.0)
        linhas = [
            f"AGÊNCIA: {conta['agencia']}",
            f"CONTA: {conta['numero_conta']}",
            f"TITULAR: {cliente['nome']}",
            f"CPF: {cliente['cpf']}",
            f"ENDEREÇO: {cliente['endereco']}",
            # f"SALDO ATUAL: R$ {saldo:,.2f}",
            # f"LIMITE: R$ {limite:,.2f}",
            # f"SALDO + LIMITE: R$ {saldo + limite:,.2f}"
        ]
        for linha in linhas:
            print(linha)
        print(separador + "\n")

    print("FIM LISTA DE CONTAS".center(largura_total))
    print(separador + "\n")


def salvar_dados():
    dados = {
        "clientes": clientes,
        "contas": contas_clientes
    }

    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii = False, indent = 4)
    print("Dados salvos com sucesso!")


def carregar_dados():

    """Criei essa função para carregar os dados do arquivo JSON, 
    criando um novo se não existir ou estiver corrompido, 
    utilizando globalmente as variaveis clientes e contas_clientes."""

    global clientes, contas_clientes

    try:
        if not os.path.exists(ARQUIVO_DADOS):
            raise FileNotFoundError("Arquivo de dados não encontrado.")
        
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
            conteudo = f.read().strip()
            if not conteudo:
                raise ValueError("Arquivo de dados vazio.")
            
            dados = json.loads(conteudo)
            clientes[:] = dados.get("clientes", [])
            contas_clientes[:] = dados.get("contas", [])
            print("📂  Dados carregados com sucesso!")

    except (FileNotFoundError, ValueError) as e:
        print(f"⚠️  {e} Recriando banco de dados limpo...")
        salvar_dados()
    except json.JSONDecodeError:
        print("❌  Erro ao ler o arquivo de dados (JSON inválido). Recriando banco limpo...")
        salvar_dados()
    except Exception as e:
        print(f"⚠️  Erro inesperado ao carregar dados: {e}")
        salvar_dados()



if __name__ == "__main__":
    carregar_dados()
    while True:
        menu = """
############# Seja Bem Vindo(a) ao Banco Real Madruga #############

============== MENU PRINCIPAL ==============

CADASTROS E ETC          | FINANCEIRO
           
[1] => Cadastrar Cliente | [D] => Depositar
[2] => Criar Conta       | [S] => Sacar
[3] => Listar Clientes   | [E] => Extrato
[4] => Listar Contas     |
[0] => Sair              |
                         |
============================================
"""
        print(menu)
        opcao = input("Escolha uma opção: ").strip().upper()

        if opcao == "1":
            cadastrar_cliente()

        elif opcao == "2":
            criar_conta_cliente()

        elif opcao == "3":
            listar_clientes()

        elif opcao == "4":
            listar_contas()

        elif opcao == "D":
            while True:
                    try:
                        numero_conta_str = input("Informe o número da conta: ").strip()
                        if not numero_conta_str:
                            raise ValueError("O campo não pode ficar em branco!")
                        if not numero_conta_str.isdigit():
                            raise ValueError("Deve conter apenas dígitos!")
                        numero_conta = int(numero_conta_str)
                        break
                    except ValueError as e:
                        print(f'\n❌ NÚMERO DA CONTA INVÁLIDO: {e} Tente novamente!')
                    
            while True:
                    try:
                        valor_str = input("Informe o valor do depósito (ex: 125,00) ").strip().replace(",", ".")
                        if not valor_str:
                            raise ValueError("O campo não pode ficar em branco!")
                        valor_deposito = float(valor_str)
                        if valor_deposito <= 0:
                            raise ValueError("O valor deve ser maior que zero!")
                        break
                    except ValueError as e:
                        print(f"\n❌ VALOR INVÁLIDO: {e} Tente novamente.")


            transacao = input("Digite uma descrição para o depósito (Inicial, PIX, etc): ").strip().upper()
            if not transacao:
                transacao = "Depósito sem descrição"


            try:
                depositar(numero_conta, valor_deposito, transacao)
            except LookupError as e:
                print(f"\n❌ ERRO: {e}")
            except TypeError as e:
                print(f"\n❌ ERRO DE TIPO: {e}")
            except ValueError as e:
                print(f"\n❌ ERRO DE VALOR: {e}")

        elif opcao == "S":
            while True:
                try:
                    numero_conta_str = input("Informe o número da conta: ").strip()
                    if not numero_conta_str:
                        raise ValueError("O campo não pode ficar em branco!")
                    if not numero_conta_str.isdigit():
                        raise ValueError("Deve conter apenas dígitos!")
                    numero_conta = int(numero_conta_str)
                    break
                except ValueError as e:
                    print(f'\n❌ NÚMERO DA CONTA INVÁLIDO: {e} Tente novamente!')
            while True:
                try:
                    valor_str = input("Informe o valor do SAQUE (ex: 125,00) ").strip().replace(",", ".")
                    if not valor_str:
                        raise ValueError("O campo não pode ficar em branco!")
                    valor_saque = float(valor_str)
                    if valor_saque <= 0:
                        raise ValueError("O valor deve ser maior que zero!")
                    break
                except ValueError as e:
                    print(f"\n❌ VALOR INVÁLIDO: {e} Tente novamente.")

            transacao = input("Informe a descrição do saque (ex: Em espécie, PIX, Transferência): ").strip().upper()
            if not transacao:
                transacao = "Saque em espécie"

            try:
                sacar(numero_conta = numero_conta, valor_saque = valor_saque, transacao = transacao)
            except LookupError as e:
                print(f"\n❌ ERRO: {e}")
            except TypeError as e:
                print(f"\n❌ ERRO DE TIPO: {e}")
            except ValueError as e:
                print(f"\n❌ ERRO DE VALOR: {e}")

        elif opcao == "E":
            while True:
                try:
                    numero_conta_str = input("Informe o número da conta para o extrato: ").strip()
                    if not numero_conta_str:
                        raise ValueError("O campo não pode ficar em branco!")
                    if not numero_conta_str.isdigit():
                        raise ValueError("Deve conter apenas dígitos!")
                    numero_conta = int(numero_conta_str)
                    break
                except ValueError as e:
                    print(f"\n❌ ERRO: {e} Tente novamente.")

            try:
                exibir_extrato(numero_conta, incluir_detalhes=True)
            except LookupError as e:
                print(f"\n❌ ERRO: {e}")

        elif opcao == "0":
            print("👋 Saindo do sistema...")
            break

        else:
            print("❌ Opção inválida, tente novamente.")
