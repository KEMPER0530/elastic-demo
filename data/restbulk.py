# coding: UTF-8
import pandas as pd
from collections import defaultdict
from collections import ChainMap
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

# ファイルをDataFrameに読み込む
files = 'areas.csv,categories.csv,prefs.csv,rating_votes.csv,ratings.csv,restaurants.csv,stations.csv'.split(
    ',')
d = {i: pd.read_csv(j, dtype='str').fillna('')
     for i, j in zip([i.replace('.csv', '') for i in files], files)}

# 軸になるレストランデータ
r = d['restaurants'].copy()

# 型変換
var_lst = ['id', 'pref_id', 'area_id', 'station_id1', 'station_time1', 'station_distance1', 'station_id2', 'station_time2', 'station_distance2', 'station_id3', 'station_time3', 'station_distance3', 'category_id1',
           'category_id2', 'category_id3', 'category_id4', 'category_id5', 'open_morning', 'open_lunch', 'open_late', 'photo_count', 'special_count', 'menu_count', 'fan_count', 'access_count', 'closed']

r['store_id'] = r['id'].astype('int')
r['open_morning'] = r['open_morning'].astype('int')
r['open_lunch'] = r['open_lunch'].astype('int')
r['open_late'] = r['open_late'].astype('int')
r['photo_count'] = r['photo_count'].astype('int')
r['special_count'] = r['special_count'].astype('int')
r['menu_count'] = r['menu_count'].astype('int')
r['fan_count'] = r['fan_count'].astype('int')
r['access_count'] = r['access_count'].astype('int')
r['closed'] = r['closed'].astype('int')

# r[var_lst] = r[var_lst].astype('int')

# エリア名の情報を結合する
area = d['areas'].set_index('id').to_dict()['name']
area['0'] = 'エリア不明？'
r['area_name'] = r['area_id'].apply(lambda x: area[x])

# 都道府県名をルックアップ〜結合する
pref = d['prefs'].set_index('id').to_dict()['name']
pref['0'] = '不明？'

r['pref_name'] = r['pref_id'].apply(lambda x: pref[x])
r['pref'] = r['pref_id'].apply(lambda x: x.rjust(
    2, '0') + '__' + pref[x])  # prefフィールドは、13__東京都　のような例


# 緯度経度を「location」フィールドに設定する
def dms2deg(_lat, _lon):
    """
    DMS形式(35.12.32.134)から、ミリ秒形式(DEG形式)に変換する。
    また、ミリビョウ形式の緯度と経度をElasticsearchのgeo_point形式（配列）に配置する。
    """
    def _dms2deg(dms_str):
        if dms_str:
            d, m, s, ms = map(int, dms_str.split('.'))
            deg = d + (m/60) + (s/3600) + (ms/(3600 * 1000))
            return deg
        return None
    lat = _dms2deg(_lat)
    lon = _dms2deg(_lon)
    if lat and lon:
        return [lon, lat]  # 経度 緯度の順
    return []


r['location'] = r.apply(lambda s: dms2deg(
    s['north_latitude'], s['east_longitude']), axis=1)


def myflatten(l):
    """
    2次元のリストを平坦化
    """
    return list(set(list(filter(lambda x: len(x) > 0, sum(l, [])))))


# 駅情報を結合する
_sta = {i[0]: i[1]
        for i in
        d['stations'].apply(
        lambda s: [s['id'], [s['name'], s['property']]],
        axis=1).to_list()
        }
sta = ChainMap(_sta, defaultdict(lambda: ['']))


staIdCols = 'station_id1,station_id2,station_id3'.split(',')
s1, s2, s3 = staIdCols
r['stas'] = r[staIdCols].apply(lambda s: myflatten(
    [sta[s[s1]], sta[s[s2]], sta[s[s3]]]
), axis=1)

# カテゴリ情報を結合する
# なお、カテゴリ情報は、大中小のように階層関係が存在するようなので、小カテゴリのラベルづけがされているデータについては、上位カテゴリも合わせて取り込む
# (豚骨ラーメン屋は、ラーメン屋であるため、このお店に元の「豚骨ラーメン屋」に加え、「ラーメン屋」もラベルづけする...ということ)
c = d['categories']
"""
【参考】d['categories']の調査
# 次の例をみると「0」となっており、id=0のレコードは存在しないので、無効データと想定
set(c.parent2)
# parent1を辿っていくと、次のpp1が最上位カテゴリと思われるのでそう考える(最大3階層)
p1 = c[c.id.isin(set(c.parent1))]
pp1 = c[c.id.isin(set(p1.parent1))]
pp1
id       name  name_kana parent1 parent2 similar
100         和食       わしょく       0       0
200       西洋料理   せいようりょうり       0       0
300       中華料理   ちゅうかりょうり       0       0
400  アジア・エスニック  あじあ・えすにっく       0       0
1000       スイーツ       すいーつ       0       0
1100      パン・軽食   ぱん・けいしょく       0       0
あと、similarにはおおよそ同義語が入っているように見えたので、実質カテゴリの別名（検索でヒットさせても良いワード）だと思って取り扱う。
"""
c_p = pd.merge(
    pd.merge(c, c, how='left', left_on='parent1',
             right_on='id', suffixes=['', '_1p']),
    c, how='left', left_on='parent1_1p', right_on='id', suffixes=['', '_2p']).fillna('')

cate = {i[0]: i[1]
        for i in
        c_p.apply(
        lambda s:
            [s['id'], [s['name'], s['name_1p'], s['name_2p'],
                       s['similar'], s['similar_1p'], s['similar_2p']]],
            axis=1).to_list()
        }
cate['0'] = ['']  # 手抜き
cate[''] = ['']  # 手抜き

catIdCols = 'category_id1,category_id2,category_id3,category_id4,category_id5'.split(
    ',')
c1, c2, c3, c4, c5 = catIdCols

r['cates'] = r[catIdCols].apply(lambda s: myflatten(
    [cate[s[c1]], cate[s[c2]], cate[s[c3]], cate[s[c4]], cate[s[c5]]]
), axis=1)

# くちコミ情報のフリーテキストを全て取り込んだロングテキスト情報を生成し、該当のお店のレコードに結合する（前準備)。

d['ratings']['kuchikomi'] = d['ratings'].apply(
    lambda s: s['title'] + s['body'], axis=1)

kuchikomi = d['ratings'].groupby('restaurant_id')['kuchikomi'].apply(
    lambda s: list(s)).reset_index()

# 元々、整数型のフィールドを、(前処理の都合で文字列型としていたため)int型に変換する。
dtype2int = {
    i: 'int' for i in 'photo_count,special_count,menu_count,fan_count,access_count'.split(',')}

# Elasticsearch(localhostの9200ポートで待機) にバルクロードする
endpoint = 'http://localhost:9200'
indexname = 'restdatademo'
es = Elasticsearch(endpoint, timeout=300,
                   max_retries=10, retry_on_timeout=True)

r['_index'] = indexname
r['_type'] = '_doc'

actions = pd.merge(r, kuchikomi, how='left', left_on='id', right_on='restaurant_id').fillna(
    '').astype(dtype2int).to_dict(orient='records')
# 補足： クチコミ情報はここで結合（他はルックアップ型だが、pandas.mergeでDataFrameを結合)

bulk(client=es, actions=actions, chunk_size=100)
