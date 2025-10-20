# 📂 Banco Real Madruga — Sistema Bancário em Python #

Um sistema bancário simples em linha de comando (CLI) para fins didáticos — cadastro de clientes, criação de contas, depósitos, saques, extrato e persistência local em JSON. Ideal para estudos de Python, manipulação de arquivos e estruturas de dados.

<br><br>
## ✨ Principais funcionalidades

✅ Cadastro de clientes com validações (nome, data de nascimento, CPF, endereço).

✅ Criação de contas atreladas a clientes.

✅ Depósito e saque com geração sequencial de documento (DOC).

✅ Exibição de extrato formatado (colunas alinhadas, totais e rodapé).

✅ Listagens de clientes e contas com layout tipo “extrato” — blocos individuais com separadores dinâmicos.

✅ Persistência local em arquivo JSON (banco_de_dados.json) com tratamento robusto de arquivo não existente, vazio ou corrompido.

✅ Mensagens amigáveis e tratamento de erros controlado (sem stacktrace para o usuário).

<br><br>
## 🛠️ Requisitos

Python 3.8+ (testado em Python 3.11)

Nenhuma dependência externa (apenas bibliotecas padrão: json, os, datetime)

<br><br>
## 🚀 Como executar

1. Clone o repositório:

   <img width="355" height="39" alt="image" src="https://github.com/user-attachments/assets/5f7f5d76-0240-4eed-98dc-7b17fdc2d4c3" />

2. Execute o script:
   
   <img width="223" height="27" alt="image" src="https://github.com/user-attachments/assets/af725594-b8e2-471d-93e4-6c77e10cc3c1" />

<br><br>
## 📁 Arquivos gerados

banco_de_dados.json — arquivo onde os dados de clientes e contas são salvos automaticamente.

Criado automaticamente se não existir.

Se estiver vazio ou corrompido, o sistema recria um banco limpo (com aviso).

Exemplo de estrutura do JSON salvo:

<img width="447" height="614" alt="image" src="https://github.com/user-attachments/assets/0a5abe46-1090-4352-b4bd-e726caf9d8a0" />

<br><br>
## 📋 Menu e comandos (fluxo do programa)

Ao rodar, você verá o menu:

<img width="582" height="310" alt="image" src="https://github.com/user-attachments/assets/7322ee3f-1ff1-4755-bf35-2a66e4ea4924" />


## Ações disponíveis

1 — Cadastrar cliente (validações de CPF, data, campos obrigatórios).

2 — Criar conta (vincula por CPF; agência fixa 0001; conta sequencial).

D — Depositar (solicita número da conta, valor e descrição).

S — Sacar (valida saldo disponível).

E — Exibir extrato (formato tabular com colunas DATA, HISTÓRICO, DOC, VALOR).

3 — Listar clientes (blocos individuais com separadores dinâmicos).

4 — Listar contas (blocos individuais com separadores dinâmicos).

0 — Encerrar.

## Design das telas / saída

Extrato: colunas com larguras pré-definidas (DATA, HISTÓRICO, DOC, VALOR) e rodapé com SALDO ATUAL, LIMITE, SALDO + LIMITE.

Listagens (clientes/contas): cada registro é impresso em um bloco com:

<img width="458" height="109" alt="image" src="https://github.com/user-attachments/assets/c06b6317-fbc0-4801-a2fb-b1b5cd5799f2" />

<br></br>
Extrato

<img width="529" height="290" alt="image" src="https://github.com/user-attachments/assets/10bb422a-8327-41ae-afe4-47fced4de7eb" />

<br></br>
Lista de Clientes

<img width="448" height="307" alt="image" src="https://github.com/user-attachments/assets/ebd5ccaa-7a49-4ad8-8e48-b225a91aad7c" />

<br></br>
Lista de Contas

<img width="482" height="439" alt="image" src="https://github.com/user-attachments/assets/aa238b46-77e4-4cc2-a359-9efbf06400a7" />

Separadores aumentam dinamicamente para combinar com a maior linha do bloco (melhora leitura quando endereços são longos).

<br><br>
## 🧰 Como os dados são mantidos

Sempre que funções que alteram o estado são chamadas (cadastrar_cliente, criar_conta_cliente, depositar, sacar) o arquivo é atualizado chamando salvar_dados().

A função carregar_dados() verifica:

Se o arquivo existe → carrega.

Se não existe → cria um arquivo novo e vazio (avisa no terminal).

Se está vazio ou JSON inválido → recria banco limpo e avisa.

Tratamento de erros é amigável ao usuário (mensagens claras), evitando stacktraces desnecessários no fluxo normal.

<br><br>
## 🛠️ Melhorias sugeridas (próximos passos)

✅ Exportar extrato/contas para CSV.

✅ Implementar importação de CSV/JSON para recuperação de dados.

✅ Adicionar testes unitários (pytest).

✅ Interface web simples (Flask/FastAPI) ou GUI (Tkinter) para demonstração.

✅ Histórico de auditoria (quem realizou a operação / quando).

<br><br>
## 🤝 Contribuição

Contribuições são bem-vindas!

Abra uma issue para bugs ou sugestões.

Para Pull Requests: por favor inclua descrição clara e testes/exemplos quando aplicável.



