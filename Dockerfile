FROM ubuntu:18.04

# 以降の作業は/work直下で
WORKDIR /work

# Debパッケージのインストール
RUN apt-get update \
  && apt-get -y upgrade \
  && apt-get install -y wget \
    python3.8 \
    python3-pip \
    mysql-server \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# ファイルの追加
ADD ./docker ./docker
ADD ./tabelogger ./tabelogger
ADD ./requirements.txt ./requirements.txt
ADD ./setup.py ./setup.py

# pythonモジュールのインストール
RUN alias python=python3.8 && \
  python3.8 -m pip install --upgrade pip && \
  python3.8 -m pip install -r requirements.txt

# mysqlの設定
RUN service mysql start \
  && mysql -uroot < ./docker/mysql/init.ddl \
  && mysql -uroot tabelogger < ./docker/mysql/create_stores.sql

# bashrcの設定
RUN echo "export PYTHONIOENCODING=utf-8" >> ~/.bashrc \
  && echo "export LC_ALL=C.UTF-8" >> ~/.bashrc \
  && echo "export LANG=C.UTF-8" >> ~/.bashrc \
  && echo "service mysql start" >> ~/.bashrc \
  && echo "alias python=python3.8" >> ~/.bashrc \
  && echo 'alias pip="python -m pip"' >> ~/.bashrc


# 実行時の初期設定
# 仮想環境を実行
# CMD /bin/bash
CMD ["/bin/bash", "/work/docker/init.sh"]
