# navitime-reachable-api

NAVITIME Reachable API を使用して、指定地点から一定時間内に到達可能な駅・バス停を検索し、CSVファイルへ出力および地図上で可視化するツールです。

## 要件

- 茅場町（35.6817137,139.7777797）へ30分以内に到達でき、かつ乗り換え1回以内で到達できる駅やバス停を探す。
  - なお、緯度経度や乗り換え回数、n分以内と言った値はユーザーが入力できるようにする。
- 駅やバス停はそれぞれ csv にまとめる。
- 範囲を map に可視化する。

### 対象ユーザー

- 私のみ

### アウトプット

- 駅やバス停の緯度経度
- 駅やバス停の名称
- 駅やバス停の種類
- 駅やバス停の線路
- インタラクティブな map による可視化

### 地図上の表示

- ポリゴン（30分圏内）
- マーカー（駅：色＝所要分・ツールチップ＝駅名＋分数＋乗換）

### 環境要件

- Python
- Poetry

### 主要ライブラリ

- requests
- pandas
- geopandas
- shapely
- folium

### API

Navitime の Reachable API (RapidAPI)を使用する。

- https://rapidapi.com/navitimejapan-navitimejapan/api/navitime-reachable

#### リクエスト例

```sh
curl --request GET \
    --url 'https://navitime-reachable.p.rapidapi.com/reachable_motorcycle?start=35.689457%2C139.691935&term=30&partition_count=36&motorcycle_fare=toll&datum=wgs84&coord_unit=degree' \
    --header 'x-rapidapi-host: navitime-reachable.p.rapidapi.com' \
    --header 'x-rapidapi-key: API_KEY'
```

なお、API キーは環境変数で管理する。

## セットアップ

### 1. 環境構築

```bash
# mise のインストール（未インストールの場合）
# https://mise.jdx.dev/

# 環境のセットアップ
mise install

# 依存関係のインストール
poetry install
```

### 2. API キーの設定

RapidAPI から NAVITIME Reachable API のキーを取得し、環境変数に設定します。

```bash
export RAPIDAPI_KEY="your_api_key_here"
```

## 使い方

### 基本的な使い方

```bash
# デフォルト設定で実行（茅場町から30分以内、乗り換え1回以内）
poetry run python src/main.py

# または同梱のスクリプトを使用
./run_sample.sh
```

### オプション指定

```bash
# 東京駅から20分以内、乗り換えなしで検索
poetry run python src/main.py --lat 35.6812 --lon 139.7671 --time 20 --transfers 0

# 出力ディレクトリと地図ファイル名を指定
poetry run python src/main.py --output-dir results --map-file tokyo_reachable.html
```

### コマンドラインオプション

- `--lat`: 起点の緯度（デフォルト: 35.6817137 茅場町駅）
- `--lon`: 起点の経度（デフォルト: 139.7777797 茅場町駅）
- `--time`: 到達時間（分）（デフォルト: 30）
- `--transfers`: 最大乗り換え回数（デフォルト: 1）
- `--output-dir`: CSV出力ディレクトリ（デフォルト: csv/）
- `--map-file`: 地図HTMLファイル名（デフォルト: reachable_map.html）

## 出力ファイル

- `csv/stations.csv`: 到達可能な駅の一覧
- `csv/bus_stops.csv`: 到達可能なバス停の一覧
- `reachable_map.html`: インタラクティブな地図（ブラウザで開いて確認）
