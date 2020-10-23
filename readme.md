# Instalacion

Para instalar seguir al pie de la letra las instrucciones completas en:<br/>
https://rasa.com/docs/rasa/installation<br/>

## MacOS y Ubuntu
Ayuda memoria (usar la guía oficial):

```
virtualenv env -p python3
source env/bin/activate
pip install rasa==2.0.0rc1
pip install -U rasa-x==0.33.0rc1 --extra-index-url https://pypi.rasa.com/simple
```

## Windows
Ayuda memoria (usar la guía oficial):
```
pip3 install -U pip
python3 -m venv ./venv
.\venv\Scripts\activate
pip install rasa==2.0.0rc1
pip install -U rasa-x==0.33.0rc1 --extra-index-url https://pypi.rasa.com/simple
```

# Development
Para trabajar una vez instalado:

Consola 1:
```
git pull
.\venv\Scripts\activate o source ./env/bin/activate
cd chatbot
rasa run actions
```
Consola 2:
```
git pull
.\venv\Scripts\activate o source ./env/bin/activate
cd chatbot
rasa train
rasa shell
```
Para testear:
```
rasa test nlu --nlu data/nlu.yml --cross-validation
```

# Git
Comandos básicos para GitHub
```
git pull
git status
git add (lo del status)
git commit -m "mensaje de commit" 
git push 
```
