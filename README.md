# Chatbot Jovem Programador

Chatbot local de perguntas e respostas baseado no conteúdo do programa Jovem Programador. O sistema utiliza análise semântica com o modelo `all-MiniLM-L6-v2` para identificar e retornar informações relevantes. Funciona completamente offline após a instalação.

---

## Visão geral

O chatbot extrai e organiza blocos de informação de um arquivo HTML estruturado. Ao receber uma pergunta, compara semanticamente com os textos disponíveis e retorna a resposta mais próxima com base em similaridade.

---

## Capturas de tela

Print do terminal com os comandos Git executados:
![Reconhecimento](src/img/214121729471248.png)

Print do terminal com exibição de resposta do chatbot:
![Resposta](src/img/912491729471248.png)

---

## Estrutura do projeto

```
PI/
│
├── index.py                # Script principal do chatbot
├── requirements.txt        # Lista de bibliotecas necessárias
└── src/
    ├── html/               # Contém o HTML fonte com os dados do programa
    └── img/                # Imagens usadas neste README
```

---

## Como executar

1. Clone este repositório ou baixe os arquivos.

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Verifique se o arquivo `Jovem_Programador.html` está presente na pasta `src/html/`.

4. Execute o programa:

```bash
python index.py
```

5. Faça perguntas relacionadas ao conteúdo para tirar suas dúvidas.

---

## Requisitos

- Python 3.8 ou superior
- Git instalado
- Acesso à internet apenas para instalação de dependências

---
