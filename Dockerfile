FROM python:3

ADD main.py /
ADD venv-unix /
CMD [ "venv-unix/bin/python3", "./main.py"]