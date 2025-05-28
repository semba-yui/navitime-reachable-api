#!/bin/bash
# サンプル実行スクリプト

# 環境変数の確認
if [ -z "$RAPIDAPI_KEY" ]; then
    echo "エラー: 環境変数 RAPIDAPI_KEY が設定されていません。"
    echo "以下のコマンドを実行してください:"
    echo "export RAPIDAPI_KEY='your_api_key_here'"
    exit 1
fi

# Poetry環境のアクティベート確認
if ! command -v poetry &> /dev/null; then
    echo "エラー: Poetry がインストールされていません。"
    echo "mise install を実行してください。"
    exit 1
fi

# 依存関係のインストール
echo "依存関係をインストール中..."
poetry install

# デフォルトパラメータで実行（茅場町から30分以内、乗り換え1回以内）
echo "茅場町駅から30分以内の駅・バス停を検索中..."
poetry run python src/main.py

echo ""
echo "完了しました！"
echo "結果ファイル:"
echo "  - csv/stations.csv (駅一覧)"
echo "  - csv/bus_stops.csv (バス停一覧)"
echo "  - reachable_map.html (地図)"