# Elasticsearch

Elasticsearch on docker.

## kibanaの接続先

http://localhost:5601

## テストデータの解凍

```bash
$ cd data && tar -zxvf ./data/ldgourmet.tar.gz
```

## テストデータを csv から json へ変更

```bash
$ python ./data/csv2json.py restaurants.csv > restaurants.json
$ python ./data/csv2json.py areas.csv > areas.json
$ python ./data/csv2json.py categories.csv > categories.json
$ python ./data/csv2json.py prefs.csv > prefs.json
$ python ./data/csv2json.py rating_votes.csv > rating_votes.json
$ python ./data/csv2json.py ratings.csv > ratings.json
$ python ./data/csv2json.py stations.csv > stations.json
```

## スキーマ定義

```bash
$ curl -H "Content-Type: application/json" -XPOST 'http://localhost:9200/restaurants/_doc' -d @schema.json
```

## データ投入

```bash
$ curl -H "Content-Type: application/json" -XPOST 'http://localhost:9200/restaurants/_doc/_bulk?pretty' --data-binary "@restaurants.json"
```
```bash
$ curl -H "Content-Type: application/json" -XPOST 'http://localhost:9200/areas/_doc/_bulk?pretty' --data-binary "@areas.json"
```
```bash
$ curl -H "Content-Type: application/json" -XPOST 'http://localhost:9200/categories/_doc/_bulk?pretty' --data-binary "@categories.json"
```
```bash
$ curl -H "Content-Type: application/json" -XPOST 'http://localhost:9200/prefs/_doc/_bulk?pretty' --data-binary "@prefs.json"
```
```bash
$ curl -H "Content-Type: application/json" -XPOST 'http://localhost:9200/rating_votes/_doc/_bulk?pretty' --data-binary "@rating_votes.json"
```
```bash
$ curl -H "Content-Type: application/json" -XPOST 'http://localhost:9200/ratings/_doc/_bulk?pretty' --data-binary "@ratings.json"
```
```bash
$ curl -H "Content-Type: application/json" -XPOST 'http://localhost:9200/stations/_doc/_bulk?pretty' --data-binary "@stations.json"
```

## Elasticsearchの資料
 - [公式](https://www.elastic.co/guide/jp/index.html)
 - [Elasticsearch の curl を使った index の削除](https://qiita.com/fujieee/items/5f3795d8213373b3b450)
 - [SQL と Elasticsearch とのクエリの比較](https://qiita.com/NAO_MK2/items/630f2c4caa0e8a42407c)
 - [ElasticsearchとSQL対比しながら理解](https://qiita.com/kieaiaarh/items/5ea4e8a188bd9814000d)

## API

## GET /\_cat/health?v

Elasticsearch のヘルスチェックを行う

```bash
curl "localhost:9200/_cat/health?v"
```

## GET /\_cat/nodes?v

Node の状態確認

```bash
curl "localhost:9200/_cat/nodes?v"
```

## GET /\_cat/indices?v

index のリストアップ

```bash
curl "localhost:9200/_cat/indices?v"
```

## PUT /restaurants?pretty

index の作成

```bash
curl -X PUT "localhost:9200/restaurants?pretty"
```

## PUT /restaurants/\_doc/1?pretty

index にデータ突っ込む。index 作成前に実行も可能。リプレイスも可能。

```bash
curl -X PUT -H 'Content-Type:application/json' "localhost:9200/restaurants/_doc/1?pretty" -d '{"name": "John Doe"}'
```

## GET /restaurants/\_doc/1?pretty

id 指定でデータ所得

```bash
curl "localhost:9200/restaurants/_doc/1?pretty"
```

## DELETE /restaurants?pretty

index 削除

```bash
 curl -X DELETE "localhost:9200/restaurants?pretty"
```

## POST /restaurants/\_doc?pretty

id ランダム生成でデータ突っ込む

```bash
curl -X POST -H 'Content-Type:application/json' "localhost:9200/restaurants/_doc/?pretty" -d '{"name": "ddddd"}'
```

## POST /restaurants/\_doc/1/\_update?pretty

document のアップデート

```bash
curl -X POST -H 'Content-Type:application/json' "localhost:9200/restaurants/_doc/1/_update?pretty" -d '{"doc": {"name": "Jane Doe"}}'
```

```bash
curl -X POST -H 'Content-Type:application/json' "localhost:9200/restaurants/_doc/1/_update?pretty" -d '{"doc": {"name": "Jane Doe", "age": 20}}'
```

現在のソースドキュメントを参照してスクリプトを実行する

```bash
curl -X POST -H 'Content-Type:application/json' "localhost:9200/restaurants/_doc/1/_update?pretty" -d '{"script" : "ctx._source.age += 5"}'
```

## DELETE /restaurants/\_doc/2?pretty

document の削除

```bash
curl -X DELETE "localhost:9200/restaurants/_doc/2?pretty"
```

## POST /restaurants/\_doc/\_bulk?pretty

bulk を使用して複数 ドキュメントを index
データの最後の行は、改行文字\ n で終わる必要がある

```bash
curl -X POST "localhost:9200/restaurants/_doc/_bulk?pretty" -H 'Content-Type: application/json' -d'
{"index":{"_id":"1"}}
{"name": "John Doe" }
{"index":{"_id":"2"}}
{"name": "Jane Doe" }
'

```

```bash
curl -X POST "localhost:9200/restaurants/_doc/_bulk?pretty" -H 'Content-Type: application/json' -d'
{"update":{"_id":"1"}}
{"doc": { "name": "John Doe becomes Jane Doe" } }
{"delete":{"_id":"2"}}
'

```

## GET /restaurants/\_search?q=\*&sort=account_number:asc&pretty

URL による検索 API(default10 件)

```bash
curl "localhost:9200/restaurants/_search?q=*&sort=id:asc&pretty"
```

json による検索 API(default10 件)

```bash
curl -X GET "localhost:9200/restaurants/_search" -H 'Content-Type: application/json' -d'
{
  "query": { "match_all": {} },
  "sort": [
    { "id": "asc" }
  ]
}
'

```

検索数とどこから検索かを指定

```bash
curl -X GET "localhost:9200/restaurants/_search" -H 'Content-Type: application/json' -d'
{
  "query": { "match_all": {} },
  "from": 10,
  "size": 10,
  "sort": [
    { "id": "asc" }
  ]
}
'

```

返却する JSON のフィールドを選択

```bash
curl -X GET "localhost:9200/restaurants/_search" -H 'Content-Type: application/json' -d'
{
  "query": { "match_all": {} },
  "_source": ["id", "name"]
}
'

```

query による検索は下記参照

> https://www.elastic.co/guide/en/elasticsearch/reference/current/_executing_searches.html

filter する際は下記
gte は greater than or equal の略？

```bash
curl -X GET "localhost:9200/restaurants/_search" -H 'Content-Type: application/json' -d'
{
  "query": {
    "bool": {
      "must": { "match_all": {} },
      "filter": {
        "range": {
          "id": {
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
