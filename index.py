from rich.console import Console
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer, util
import os
import time
import pyfiglet

console = Console()

# Escreve texto no terminal, letra por letra, com cor e atraso ajustável.
def escrever_lento(texto, cor="green", delay=0.02):
    for char in texto:
        console.print(char, end="", style=cor, soft_wrap=True, highlight=False)
        time.sleep(delay)
    print()

# Extrai blocos de conteúdo de um HTML estruturado com accordion.
def extrair_blocos_accordion(html):
    soup = BeautifulSoup(html, "html.parser")
    blocos = []

    # Busca o contêiner principal com ID específico.
    container = soup.find("div", id="accordionExample")
    if not container:
        return blocos  # Retorna lista vazia se contêiner não existir.

    # Itera sobre blocos diretos dentro do accordion.
    for bloco_div in container.find_all("div", recursive=False):
        # Coleta os títulos (h3, h4).
        titulos_tags = bloco_div.find_all(["h4", "h3"])
        titulos = [t.get_text(strip=True) for t in titulos_tags if t.get_text(strip=True)]
        titulo_composto = " - ".join(titulos) if titulos else None

        # Localiza corpo do conteúdo ou usa o próprio bloco.
        corpo_tag = bloco_div.find("div", class_="card-body") or bloco_div
        conteudo_textos = []

        if corpo_tag:
            # Coleta textos de parágrafos, listas, etc.
            for elem in corpo_tag.find_all(["p", "li", "h4", "h3", "span", "div"], recursive=True):
                texto = elem.get_text(strip=True)
                if texto:
                    conteudo_textos.append(texto)

            # Adiciona inputs preenchidos manualmente, se existirem.
            inputs = corpo_tag.select(".form-control")
            for inp in inputs:
                valor = inp.get("value", "") or inp.text.strip()
                if valor:
                    conteudo_textos.append(f"[Campo preenchido] {valor}")

        conteudo = "\n".join(conteudo_textos)

        # Só adiciona blocos completos com título e conteúdo.
        if titulo_composto and conteudo:
            blocos.append((titulo_composto, conteudo))

    return blocos

# Prepara blocos em formato de texto único para embeddings.
def montar_textos_para_embeddings(blocos):
    return [f"{titulo}\n{conteudo}" for titulo, conteudo in blocos]

# Limpa tela e exibe título ASCII formatado.
def exibir_titulo():
    os.system("cls" if os.name == "nt" else "clear")
    ascii_title = pyfiglet.figlet_format("CHATBOT")
    console.print(ascii_title, style="bold #630dc9", justify="left")
    console.print("Bem-vindo(a) ao Programa Jovem Programador, uma iniciativa do Sindicato das Empresas de", justify="left")
    console.print("Processamento de Dados do Estado de Santa Catarina (SEPROSC).\n", justify="left")

# Função principal. Executa o programa interativo.
def main():
    exibir_titulo()

    # Lê HTML de entrada localizado em src/html/
    with open("src/html/Jovem_Programador.html", "r", encoding="utf-8") as f:
        html = f.read()

    # Extrai blocos e transforma para o modelo.
    blocos = extrair_blocos_accordion(html)
    textos = montar_textos_para_embeddings(blocos)

    # Carrega modelo de linguagem semântico.
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(textos, convert_to_tensor=True)

    resposta_padrao = "Informação não encontrada. Pergunte de outra forma."

    while True:
        # Coleta pergunta do usuário.
        pergunta = input("Faça uma pergunta sobre o programa: ").strip()
        if pergunta.lower() == 'sair':
            break  # Encerra o programa.

        # Codifica pergunta e mede similaridade com blocos.
        emb_pergunta = model.encode(pergunta, convert_to_tensor=True)
        similaridades = util.cos_sim(emb_pergunta, embeddings)[0]
        max_sim = similaridades.max().item()
        idx = similaridades.argmax().item()

        print()
        if max_sim < 0.5:
            # Similaridade baixa. Retorna resposta padrão.
            console.print("Resposta:", style="bold red", end=" ")
            escrever_lento(resposta_padrao, cor="red")
        else:
            # Alta similaridade. Retorna conteúdo correspondente.
            titulo, conteudo = blocos[idx]
            console.print("Pergunta reconhecida:", style="bold cyan", end=" ")
            console.print(titulo, style="yellow")
            console.print("Resposta:", style="bold green", end=" ")
            escrever_lento(conteudo, cor="green")

        # Espera nova pergunta.
        input("\nPressione Enter para fazer outra pergunta...")
        exibir_titulo()

# Ponto de entrada do programa.
if __name__ == "__main__":
    main()
