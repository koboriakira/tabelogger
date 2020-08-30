
## Docker上で実行する場合

Dockerコンテナを起動。

```bash
# 起動
docker run -d --restart=always -p 12345:8000 --name tabelogger tabelogger 

# 開発用
docker run -it --rm -v $(pwd):/work -p 12345:8000 tabelogger
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
