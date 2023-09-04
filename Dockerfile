FROM python:3.11

# Set environment variables
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TERM xterm
ENV TZ Asia/Tokyo

ENV PYTHONUNBUFFERED 1

# 作業ディレクトリの作成
RUN mkdir /TrueFalseGPT

WORKDIR /mysite

RUN pip3 install --upgrade pip

# Langchanのインストールに必要
RUN pip install --default-timeout=100 future

ADD requirements.txt /mysite/

RUN pip3 install --no-cache-dir -r requirements.txt

ADD . /mysite/

EXPOSE 8000
