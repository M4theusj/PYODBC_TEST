import pyodbc

def obter_input(label, limite=30, numerico=False):
    while True:
        entrada = input(f"{label}: ").strip()
        if numerico:
            if entrada.isdigit():
                return int(entrada)
            print("Valor inválido! Insira um número.")
        elif 0 < len(entrada) <= limite:
            return entrada
        print(f"Entrada inválida! Máximo de {limite} caracteres.")

def cadastraDono():
    cad = [obter_input("Nome do dono"), obter_input("Telefone")]
    inst_consulta.execute("SELECT COALESCE(MAX(id), 0) + 1 FROM donos")
    id_novo = inst_consulta.fetchone()[0]
    inst_cadastro.execute(f"INSERT INTO donos (id, nome_dono, telefone) VALUES ({id_novo}, '{cad[0].title()}', '{cad[1]}')")
    conn.commit()

def cadastraPet():
    inst_consulta.execute("SELECT * FROM donos")
    donos = inst_consulta.fetchall()
    if not donos:
        print("Não há donos cadastrados no sistema!")
        cadastraDono()
        return
    print(f"{'ID':<10} {'NOME':<30} {'TELEFONE':<15}\n{'-'*55}")
    for id_dono, nome_dono, tel_dono in donos:
        print(f"{id_dono:<10} {nome_dono:<30} {tel_dono:<15}")

    donoPet = obter_input("Informe o ID do dono do pet [0 para cancelar]", numerico=True)
    if donoPet == 0: return
    while not any(d[0] == donoPet for d in donos):
        donoPet = obter_input("ID inválido! Digite novamente [0 para cancelar]", numerico=True)
        if donoPet == 0: return

    cad = [obter_input(f"{x.capitalize()} do pet") for x in ["tipo", "nome"]]
    idade = obter_input("Idade do pet", numerico=True)
    inst_consulta.execute("SELECT COALESCE(MAX(id), 0) + 1 FROM petshop")
    id_novo = inst_consulta.fetchone()[0]
    inst_cadastro.execute(f"INSERT INTO petshop (id, tipo_pet, nome_pet, idade, id_dono) VALUES ({id_novo}, '{cad[0].title()}', '{cad[1].title()}', {idade}, {donoPet})")
    conn.commit()

def deletaPet():
    inst_consulta.execute("SELECT tipo_pet, nome_pet FROM petshop")
    pets = inst_consulta.fetchall()
    if not pets:
        print("Não há pets cadastrados.")
        return
    for tipo, nome in pets:
        print(f"{tipo:<30} {nome:<30}")

    deletar_todos = input("Deletar todos os pets? [sim/não]: ").strip().lower() == "sim"
    if deletar_todos:
        inst_deleta.execute("DELETE FROM petshop")
    else:
        nome_pet = obter_input("Digite o nome do pet a ser deletado")
        inst_deleta.execute(f"DELETE FROM petshop WHERE nome_pet = '{nome_pet}'")
    conn.commit()

def consultaPet():
    inst_consulta.execute("SELECT tipo_pet, nome_pet, idade, nome_dono, telefone FROM petshop JOIN donos ON donos.id "
                          "= petshop.id_dono")
    pets = inst_consulta.fetchall()
    if not pets:
        print("Não há pets cadastrados.")
        return
    print(f"{'TIPO':<30} {'NOME':<30} {'IDADE':<10} {'DONO':<30} {'TELEFONE':<15}\n{'-'*115}")
    for tipo, nome, idade, dono, tel in pets:
        print(f"{tipo:<30} {nome:<30} {idade:<10} {dono:<30} {tel:<15}")

try:
    conn = pyodbc.connect(
        'DRIVER={SQL Server};SERVER=localhost;DATABASE=petshop;UID=sa;PWD=*123456HAS*'
    )
    inst_cadastro = conn.cursor()
    inst_deleta = conn.cursor()
    inst_consulta = conn.cursor()
except Exception as e:
    print("Erro na conexão:", e)
    conexao = False
else:
    conexao = True

while conexao:
    print("\nMENU\n0 - Sair\n1 - Cadastrar dono\n2 - Cadastrar pet\n3 - Deletar pet\n4 - Consultar pets")
    opcao = obter_input("Escolha", numerico=True)
    match opcao:
        case 0:
            conexao = False
        case 1:
            cadastraDono()
        case 2:
            cadastraPet()
        case 3:
            deletaPet()
        case 4:
            consultaPet()
            input("Pressione qualquer tecla para continuar")
