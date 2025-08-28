INSTALAR DEPENDÊNCIAS DO PROJETO:

pip install pip-tools
pip-compile requirements.in
pip install -r requirements.txt

=============================================================

RODAR O PROJETO:

uvicorn main:app --reload
