FROM python:3

ADD main.py /
ADD venv-unix /
CMD ["python", "-m", "pip", "install", "-r", "requirements.txt"]
CMD [ "PYTHON", "./main.py"]