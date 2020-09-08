FROM python:3.8.5-slim

# 以降の作業は/work直下で
WORKDIR /work

# Debパッケージのインストール
RUN apt-get update \
  && apt-get -y upgrade \
  && apt-get install -y wget \
  # && apt-get install -y default-mysql-client \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# ファイルの追加
ADD ./tabelogger /work/tabelogger
ADD ./requirements.txt /work/requirements.txt
ADD ./setup.py /work/setup.py

# pythonモジュールのインストール
RUN pip install --upgrade pip \
  && pip install -r requirements.txt

# 実行時の初期設定
# 仮想環境を実行
# CMD /bin/bash
# CMD ["/bin/bash", "/work/docker/init.sh"]
CMD ["uvicorn","tabelogger.main:app","--reload","--host","0.0.0.0","--port","8000"]
