FROM python:3.11

ENV PYTHONUNBUFFERED 1

# 作業ディレクトリの作成
RUN mkdir /TrueFalseGPT

WORKDIR /mysite

RUN pip install --upgrade pip

ADD requirements.txt /mysite/

RUN pip3 install -r requirements.txt

ADD . /mysite/

EXPOSE 8000
