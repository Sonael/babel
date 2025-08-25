# Prova de Conceito: Esteganografia de Código com a Biblioteca de Babel

## Descrição do Projeto

Este projeto é uma **Prova de Conceito (PoC)** que explora uma abordagem inovadora de **comando e controle (C2)** utilizando a **esteganografia de código**. A técnica consiste em ocultar um *payload* malicioso em uma plataforma online aparentemente inofensiva: a Biblioteca de Babel.

O objetivo é demonstrar como uma string de código malicioso pode ser codificada, armazenada remotamente de forma discreta e, em seguida, recuperada e executada por uma aplicação cliente. Este método ilustra um vetor de ataque, onde a *payload* não reside no sistema local.

## Como Funciona

O projeto é dividido em três componentes principais:

1.  **`encoder.py`**: Este módulo é responsável pela **codificação e decodificação** da *payload*. Ele converte a string de código ASCII em um formato de codificação específico, que utiliza caracteres como `.` e letras do alfabeto, tornando-o compatível com a Biblioteca de Babel. Ele também é capaz de reverter esse processo, transformando a string de volta ao seu formato original.

2.  **`babel.py`**: Este módulo lida com a **interação com a Biblioteca de Babel**. Ele utiliza a biblioteca `requests` para enviar requisições POST para a API da biblioteca, tanto para **buscar** a localização de uma string codificada (retornando as coordenadas de hexágono, parede, prateleira, volume e página) quanto para **navegar** até essa localização e recuperar o conteúdo do "livro" correspondente.

3.  **`main.py`**: O script principal que orquestra todo o processo. Ele demonstra o fluxo completo da PoC:

      * Uma string de código malicioso (por exemplo, `subprocess.Popen('calc.exe')`) é definida.
      * A string é codificada usando o `encoder.py`.
      * A string codificada é usada para buscar sua localização na Biblioteca de Babel via `babel.py`.
      * As coordenadas do livro são usadas para navegar e recuperar o conteúdo.
      * O conteúdo recuperado é decodificado.
      * A string decodificada é passada para a função `subprocess.run()`, simulando a execução do *payload*.

## Instalação

Para rodar esta PoC, você precisará ter o Python 3 instalado e as bibliotecas necessárias.

1.  **Clone o repositório:**

    ```bash
    git clone https://github.com/Sonael/babel.git
    cd babel
    ```

2.  **Crie e ative um ambiente virtual (recomendado):**

    ```bash
    python -m venv venv
    # No Windows
    .\venv\Scripts\activate
    # No macOS/Linux
    source venv/bin/activate
    ```

3.  **Instale as dependências:**

    ```bash
    pip install -r requirements.txt
    ```

## Uso

Para executar a prova de conceito, basta rodar o script principal:

```bash
python main.py
```

O script irá imprimir a string codificada, a resposta da Biblioteca de Babel e o resultado da execução do `subprocess`.

## Considerações de Segurança

Este projeto é estritamente para **fins educacionais e de pesquisa em segurança cibernética**. Ele demonstra uma técnica potencialmente maliciosa e não deve ser utilizado para atividades ilegais. O `subprocess.run()` com uma string de entrada não validada pode ser perigoso, e esta abordagem é usada aqui apenas para ilustrar o potencial de execução de código remoto.