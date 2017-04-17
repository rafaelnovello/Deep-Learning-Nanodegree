# Aplicativo de identificação de digitos escritos manualmente.

## Instalação

**Para baixar apenas este diretório, [click AQUI](https://minhaskamal.github.io/DownGit/#/home?url=https://github.com/rafaelnovello/Deep-Learning-Foundation/tree/master/MNIST)**

Instale os pacotes necessários:

```bash
$ pip install -r requirements.txt
```

## Treinar o modelo

O aplicativo web depende do modelo treinado. Este processo acontece no arquivo TFLearn_Digit_Recognition.ipynb. Basta executar todo o notebook para iniciar, treinar e salvar o modelo treinado como MNIST.tfl

## Executar o aplicativo web

Com as dependencias instaladas, execute os seguintes passos para rodar o web app:

```bash
$ export FLASK_APP=app.py
$ flask run
```
