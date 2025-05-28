#!/usr/bin/env python3
"""
response.json を使用してアプリケーションをテストするスクリプト
"""

import json
import sys
from pathlib import Path

# srcディレクトリをパスに追加
sys.path.insert(0, str(Path(__file__).parent / "src"))

from data_processor import DataProcessor
from map_visualizer import MapVisualizer


def main():
    # response.jsonを読み込む
    response_file = Path("response.json")
    if not response_file.exists():
        print(f"エラー: {response_file} が見つかりません")
        return
    
    with open(response_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    print(f"レスポンスデータを読み込みました:")
    print(f"  - 件数: {data.get('count', 0)}")
    print(f"  - 単位: {data.get('unit', {})}")
    print()
    
    # 駅データの処理
    stations = []
    bus_stops = []
    coordinates = []
    
    for item in data.get("items", []):
        # 座標の取得
        if "coord" in item:
            coord_data = item["coord"]
            if isinstance(coord_data, dict):
                lat = coord_data.get("lat", 0)
                lon = coord_data.get("lon", 0)
                coord = [lat, lon]
                coordinates.append(coord)
                
                # ノード名の取得
                node_name = item.get("name", "")
                
                # 共通データ
                node_data = {
                    "name": node_name,
                    "lat": lat,
                    "lon": lon,
                    "time": item.get("time", 0),
                    "transfers": item.get("transit_count", 0),
                    "lines": [],  # 路線情報は含まれていない
                    "node_id": item.get("node_id", "")
                }
                
                # 実際のレスポンスでは全て駅として扱う
                if "バス" in node_name:
                    node_data["type"] = "bus_stop"
                    bus_stops.append(node_data)
                else:
                    node_data["type"] = "station"
                    stations.append(node_data)
    
    print(f"データ処理結果:")
    print(f"  - 駅: {len(stations)}件")
    print(f"  - バス停: {len(bus_stops)}件")
    print()
    
    # DataProcessorでCSV作成
    processor = DataProcessor()
    reachable_data = {
        "stations": stations,
        "bus_stops": bus_stops
    }
    
    stations_df, bus_stops_df = processor.process_reachable_data(reachable_data, max_transfers=1)
    
    # CSVディレクトリの作成
    csv_dir = Path("csv")
    csv_dir.mkdir(exist_ok=True)
    
    # CSV保存
    processor.save_to_csv(stations_df, csv_dir / "stations_test.csv")
    processor.save_to_csv(bus_stops_df, csv_dir / "bus_stops_test.csv")
    
    print(f"CSVファイルを保存しました:")
    print(f"  - csv/stations_test.csv ({len(stations_df)}件)")
    print(f"  - csv/bus_stops_test.csv ({len(bus_stops_df)}件)")
    print()
    
    # 地図の作成
    # 茅場町の座標
    center_lat = 35.6817137
    center_lon = 139.7777797
    
    visualizer = MapVisualizer(center_lat=center_lat, center_lon=center_lon)
    
    # 起点を追加
    visualizer.add_center_marker(center_lat, center_lon, "茅場町駅（起点）")
    
    # 駅とバス停を追加
    visualizer.add_stations(stations_df)
    visualizer.add_bus_stops(bus_stops_df)
    
    # ポリゴンの作成（簡易版）
    if coordinates:
        # 凸包を計算
        from api_client import NavitimeClient
        client = NavitimeClient("dummy_key")  # ポリゴン生成のみ使用
        polygon_coords = client._generate_polygon_from_points(coordinates)
        visualizer.add_reachable_polygon(polygon_coords)
    
    # 地図の保存
    map_file = Path("test_map.html")
    visualizer.save_map(map_file)
    print(f"地図を保存しました: {map_file}")
    print()
    
    # 統計情報
    print("統計情報:")
    print(f"  - 最短時間: {stations_df['所要時間（分）'].min() if not stations_df.empty else 'N/A'}分")
    print(f"  - 最長時間: {stations_df['所要時間（分）'].max() if not stations_df.empty else 'N/A'}分")
    print(f"  - 乗り換えなし: {len(stations_df[stations_df['乗り換え回数'] == 0])}駅")
    print(f"  - 乗り換え1回: {len(stations_df[stations_df['乗り換え回数'] == 1])}駅")


if __name__ == "__main__":
    main()