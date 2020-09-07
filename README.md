## Docker上で実行する場合

Dockerコンテナを起動。

```bash
# イメージ作成（プロジェクト直下で）
docker build -t tabelogger-web -f ./docker/web/Dockerfile .
docker build -t tabelogger-mysql -f ./docker/mysql/Dockerfile .

# Dockerネットワークを作成
docker network create tabelogger-network

# 起動
docker run -d --network=tabelogger-network --restart=always -p 12345:8000 --name tabelogger tabelogger-web
docker run -d --network=tabelogger-network --rm -e MYSQL_ALLOW_EMPTY_PASSWORD=yes --name=tabelogger-db tabelogger-mysql

# 開発用
docker run -it --network=tabelogger-network --rm -v $(pwd):/work -p 12345:8000 tabelogger-web
docker run -it --rm -e MYSQL_ALLOW_EMPTY_PASSWORD=yes --name=tabelogger-db tabelogger-mysql bash
```

つぎにサーバを起動。

```bash
uvicorn tabelogger.main:app --reload --host 0.0.0.0 --port 8000
```

その後つぎのようにcurlを飛ばすか、 http://localhost:12345/docs を確認しながらリクエストを作成・実行する。


```bash
curl -X GET "http://localhost:12345/scrape?url=https%3A%2F%2Ftabelog.com%2Ftokyo%2FA1315%2FA131501%2FR1644%2FrstLst%2F1%2F%3Fsvd%3D20200313%26svt%3D1900%26svps%3D2&limit_page_count=1" 
```

## 開発する
