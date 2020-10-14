# Instalacion

https://rasa.com/docs/rasa/installation<br>

## MacOS y Ubuntu
`virtualenv env -p python3`<br>
`source env/bin/activate`<br>
`pip install rasa==2.0.0rc1`<br>
`pip install -U rasa-x==0.33.0rc1 --extra-index-url https://pypi.rasa.com/simple`<br>

## Windows
`pip3 install -U pip` <br>
`python3 -m venv ./venv`<br>
`.\venv\Scripts\activate`<br>
`pip install rasa==2.0.0rc1`<br>
`pip install -U rasa-x==0.33.0rc1 --extra-index-url https://pypi.rasa.com/simple

# Development
`.\venv\Scripts\activate` o `source env/bin/activate` para ejectutar el virtual env <br>
`rasa x`
