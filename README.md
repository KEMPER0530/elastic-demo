# Elasticsearch

Elasticsearch on docker.

# Features

Elasticsearch のクエリ練習用の機能です。
[ライブドアグルメデータ](http://blog.livedoor.jp/techblog/archives/65836960.html)を編集し、Elasticsearch へ登録してクエリの検証を実施します。

# Requirement

- elasticsearch:7.16.2
  - analysis-kuromoji
- kibana:7.16.2
- logstash:7.16.2
- Python:3

# Installation

### テストデータの解凍

ディレクトリ移動

```bash
$ cd data
```

データの解凍

```bash
$ tar -zxvf ldgourmet.tar.gz
```

### elasticsearch の起動

```bash
$ cd /elastic-demo
```

```bash
$ docker-compose up -d
```

```bash
$ docker-compose ps

     Name                    Command               State                     Ports
-----------------------------------------------------------------------------------------------------
es_docker         /bin/tini -- /usr/local/bi ...   Up      0.0.0.0:9200->9200/tcp, 9300/tcp
kibana_docker     /bin/tini -- /usr/local/bi ...   Up      0.0.0.0:5601->5601/tcp
logstash_docker   /usr/local/bin/docker-entr ...   Up      0.0.0.0:5000->5000/tcp, 5044/tcp, 9600/tcp
```

### マッピング定義の作成

```bash
$ cd data
```

```bash
$ curl -H "Content-Type: application/json" -XPOST 'http://localhost:9200/restdatademo/_doc?pretty' -d @schema.json
```

### データ投入

```bash
$ python restbulk.py
```

# Usage

### Elasticsearch のヘルスチェックを行う

#### GET /\_cat/health?v

```bash
$ curl "localhost:9200/_cat/health?v"
```

### Node の状態確認

#### GET /\_cat/nodes?v

```bash
$ curl "localhost:9200/_cat/nodes?v"
```

### index のリストアップ

#### GET /\_cat/indices?v

```bash
$ curl "localhost:9200/_cat/indices?v"
```

### index の作成

#### PUT /restdatademo?pretty

```bash
$ curl -X PUT "localhost:9200/restdatatest2?pretty"
```

### index にデータ登録(index 作成前に実行も可能。リプレイスも可能)

#### PUT /restdatademo/\_doc/1?pretty

```bash
$ curl -X PUT -H 'Content-Type:application/json' "localhost:9200/restdatademo/_doc/1?pretty" -d '{"name": "TEST STORE"}'
```

### id 指定でデータ所得

#### GET /restdatademo/\_doc/1?pretty

```bash
$ curl "localhost:9200/restdatademo/_doc/Pob1PX4BSuCe35FEr26s?pretty"
```

### id ランダム生成でデータ突っ込む

#### POST /restdatademo/\_doc?pretty

```bash
$ curl -X POST -H 'Content-Type:application/json' "localhost:9200/restdatademo/_doc/?pretty" -d '{"name": "TEST STORE"}'
```

### document のアップデート

#### POST /restaurants/\_update/1?pretty

```bash
$ curl -X POST -H 'Content-Type:application/json' "localhost:9200/restdatademo/_update/Pob1PX4BSuCe35FEr26s?pretty" -d '{"doc": {"name": "鮨与志テスト"}}'
```

### bulk を使用して複数 ドキュメントを index,データの最後の行は、改行文字\ n で終わる必要がある

#### POST /restdatatest2/\_doc/\_bulk?pretty

```bash
$ curl -X POST "localhost:9200/restdatatest2/_doc/_bulk?pretty" -H 'Content-Type: application/json' -d'
{"index":{"_id":"1"}}
{"name": "TEST STORE1" }
{"index":{"_id":"2"}}
{"name": "TEST STORE2" }
'
```

```bash
$ curl -X POST "localhost:9200/restaurants/_doc/_bulk?pretty" -H 'Content-Type: application/json' -d'
{"update":{"_id":"1"}}
{"doc": { "name": "TEST STORE3" } }
{"delete":{"_id":"2"}}
'
```

### index 削除

#### DELETE /restdatatest2?pretty

```bash
$ curl -X DELETE "localhost:9200/restdatatest2?pretty"
```

### doc 削除

#### DELETE /restdatademo/\_doc/?pretty

```bash
$ curl -X DELETE "localhost:9200/restdatademo/_doc/FYoEP34BSuCe35FERRr_?pretty"
```

### json による検索 API(default10 件)

```bash
$ curl -X GET "localhost:9200/restdatademo/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": { "match_all": {} },
  "sort": [
    {
      "store_id": { "order": "asc" }
    }
  ]
}
'
```

### 検索数とどこから検索かを指定

```bash
curl -X GET "localhost:9200/restdatademo/_search" -H 'Content-Type: application/json' -d'
{
  "query": { "match_all": {} },
  "from": 10,
  "size": 10,
  "sort": [
    { "store_id": "asc" }
  ]
}
'

```

### 返却する JSON のフィールドを選択

```bash
curl -X GET "localhost:9200/restdatademo/_search" -H 'Content-Type: application/json' -d'
{
  "query": { "match_all": {} },
  "_source": ["store_id", "name"]
}
'
```

### filter する際は下記

```bash
curl -X GET "localhost:9200/restdatademo/_search" -H 'Content-Type: application/json' -d'
{
  "query": {
    "bool": {
      "must": { "match_all": {} },
      "filter": {
        "range": {
          "store_id": {
            "gte": 200,
            "lte": 300
          }
        }
      }
    }
  }
}
'
```

## kibana の接続先

http://localhost:5601

## 参考：Elasticsearch の資料

- [公式](https://www.elastic.co/guide/jp/index.html)
- [公式 query](https://www.elastic.co/guide/en/elasticsearch/reference/current/_executing_searches.html)
- [Elasticsearch の curl を使った index の削除](https://qiita.com/fujieee/items/5f3795d8213373b3b450)
- [SQL と Elasticsearch とのクエリの比較](https://qiita.com/NAO_MK2/items/630f2c4caa0e8a42407c)
- [Elasticsearch と SQL 対比しながら理解](https://qiita.com/kieaiaarh/items/5ea4e8a188bd9814000d)
- [速習 Elasticsearch Search query 基本クエリ(match_phrase, multi_match)編](https://qiita.com/doiken_/items/670dd8a8518ebdd0b104)
- [【Elasticsearch】よく使うコマンド一覧](https://qiita.com/mug-cup/items/ba5dd0a14838e83e69ac)
