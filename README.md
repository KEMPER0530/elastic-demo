# Elasticsearch

Elasticsearch on docker.

# Features

Elasticsearch を利用したレストラン検索を実施する練習用のリポジトリです。
[ライブドアグルメデータ](https://github.com/livedoor/datasets)を編集し、
Elasticsearch へ登録してクエリの検証を実施します。

# Requirement

- elasticsearch:7.16.2
  - analysis-kuromoji
- kibana:7.16.2
- logstash:7.16.2
- Python:3

# Installation

### テストデータの取得

[こちら](https://github.com/livedoor/datasets)から「ldgourmet.tar.gz」を取得してください。

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

# Data Content

| No  | 物理名            | 論理名             | 型      | kuromoji |
| :-- | :---------------- | :----------------- | :------ | :------: |
| 1   | id                | 店舗 ID            | integer |    -     |
| 2   | name              | 店舗名             | text    |    ○     |
| 3   | property          | 支店名             | text    |    ○     |
| 4   | alphabet          | 店名欧文           | text    |    ○     |
| 5   | name_kana         | 店名ひらがな       | text    |    ○     |
| 6   | pref_id           | 都道府県 ID        | integer |    -     |
| 7   | area_id           | エリア ID          | integer |    -     |
| 8   | station_id1       | 最寄り駅 ID_1      | integer |    -     |
| 9   | station_time1     | 時間(分)\_1        | integer |    -     |
| 10  | station_distance1 | 距離(m)\_1         | integer |    -     |
| 11  | station_id2       | 最寄り駅 ID_2      | integer |    -     |
| 12  | station_time2     | 時間(分)\_2        | integer |    -     |
| 13  | station_distance2 | 距離(m)\_2         | integer |    -     |
| 14  | station_id3       | 最寄り駅 ID_3      | integer |    -     |
| 15  | station_time3     | 時間(分)\_3        | integer |    -     |
| 16  | station_distance3 | 距離(m)\_3         | integer |    -     |
| 17  | category_id1      | カテゴリ ID_1      | integer |    -     |
| 18  | category_id2      | カテゴリ ID_2      | integer |    -     |
| 19  | category_id3      | カテゴリ ID_3      | integer |    -     |
| 20  | category_id4      | カテゴリ ID_4      | integer |    -     |
| 21  | category_id5      | カテゴリ ID_5      | integer |    -     |
| 22  | zip               | 郵便番号           | text    |    -     |
| 23  | address           | 住所               | text    |    ○     |
| 24  | north_latitude    | 北緯               | float   |    -     |
| 25  | east_longitude    | 東経               | float   |    -     |
| 27  | description       | 備考               | text    |    ○     |
| 28  | purpose           | お店利用目的       | text    |    ○     |
| 29  | open_morning      | モーニング有無     | integer |    -     |
| 30  | open_lunch        | ランチ有無         | integer |    -     |
| 31  | open_late         | 23 時以降営業有無  | integer |    -     |
| 32  | photo_count       | 写真アップロード数 | integer |    -     |
| 33  | special_count     | 特集掲載数         | integer |    -     |
| 34  | menu_count        | メニュー投稿数     | integer |    -     |
| 35  | fan_count         | ファン数           | integer |    -     |
| 36  | access_count      | 類型アクセス数     | integer |    -     |
| 37  | created_on        | 作成日             | text    |    -     |
| 38  | modified_on       | 更新日             | text    |    -     |
| 39  | closed            | 閉店               | integer |    -     |
| 40  | area_name         | エリア名           | text    |    ○     |
| 41  | pref_name         | 都道府県名         | text    |    ○     |
| 42  | pref              | 都道府県 ID        | text    |    ○     |
| 43  | location          | 位置情報           | array   |    ○     |
| 44  | stas              | 駅名               | array   |    ○     |
| 45  | cates             | カテゴリ名         | array   |    ○     |
| 46  | restaurant_id     | 店舗 ID            | integer |    -     |
| 47  | kuchikomi         | 口コミ             | text    |    ○     |

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
$ curl -X POST "localhost:9200/restdatatest2/_doc/_bulk?pretty" -H 'Content-Type: application/json' -d'
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
      "id": { "order": "asc" }
    }
  ]
}
'
```

### 検索数とどこから検索かを指定

```bash
$ curl -X GET "localhost:9200/restdatademo/_search" -H 'Content-Type: application/json' -d'
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

### 返却する JSON のフィールドを選択

```bash
$ curl -X GET "localhost:9200/restdatademo/_search" -H 'Content-Type: application/json' -d'
{
  "query": { "match_all": {} },
  "_source": ["store_id", "name"]
}
'
```

### filter する際は下記

```bash
$ curl -X GET "localhost:9200/restdatademo/_search" -H 'Content-Type: application/json' -d'
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
