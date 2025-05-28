#!/usr/bin/env python3
"""
NAVITIME Reachable API を使用して到達可能な駅・バス停を検索し、
CSVファイルへの出力と地図上での可視化を行うメインスクリプト
"""

import argparse
import sys
from pathlib import Path

from api_client import NavitimeClient
from data_processor import DataProcessor
from map_visualizer import MapVisualizer
from config import Config


def parse_arguments():
    """コマンドライン引数をパース"""
    parser = argparse.ArgumentParser(
        description="指定した地点から一定時間内に到達可能な駅・バス停を検索"
    )
    
    parser.add_argument(
        "--lat",
        type=float,
        default=35.6817137,
        help="起点の緯度 (デフォルト: 茅場町駅)",
    )
    
    parser.add_argument(
        "--lon",
        type=float,
        default=139.7777797,
        help="起点の経度 (デフォルト: 茅場町駅)",
    )
    
    parser.add_argument(
        "--time",
        type=int,
        default=30,
        help="到達時間（分） (デフォルト: 30分)",
    )
    
    parser.add_argument(
        "--transfers",
        type=int,
        default=1,
        help="最大乗り換え回数 (デフォルト: 1回)",
    )
    
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("csv"),
        help="出力ディレクトリ (デフォルト: csv/)",
    )
    
    parser.add_argument(
        "--map-file",
        type=Path,
        default=Path("reachable_map.html"),
        help="地図HTMLファイル名 (デフォルト: reachable_map.html)",
    )
    
    return parser.parse_args()


def main():
    """メイン処理"""
    args = parse_arguments()
    
    try:
        # 設定の初期化
        config = Config()
        
        # APIクライアントの初期化
        client = NavitimeClient(config.api_key)
        
        print(f"検索条件:")
        print(f"  起点: ({args.lat}, {args.lon})")
        print(f"  到達時間: {args.time}分以内")
        print(f"  最大乗り換え回数: {args.transfers}回")
        print()
        
        # APIから到達可能エリアのデータを取得
        print("NAVITIME APIからデータを取得中...")
        reachable_data = client.get_reachable_transit(
            lat=args.lat,
            lon=args.lon,
            time_limit=args.time,
            max_transfers=args.transfers
        )
        
        if not reachable_data:
            print("エラー: データの取得に失敗しました")
            sys.exit(1)
        
        # データ処理
        processor = DataProcessor()
        stations_df, bus_stops_df = processor.process_reachable_data(
            reachable_data, 
            max_transfers=args.transfers
        )
        
        # 出力ディレクトリの作成
        args.output_dir.mkdir(exist_ok=True)
        
        # CSVファイルへの出力
        station_csv = args.output_dir / "stations.csv"
        bus_csv = args.output_dir / "bus_stops.csv"
        
        processor.save_to_csv(stations_df, station_csv)
        processor.save_to_csv(bus_stops_df, bus_csv)
        
        print(f"\nCSVファイルを出力しました:")
        print(f"  駅: {station_csv} ({len(stations_df)}件)")
        print(f"  バス停: {bus_csv} ({len(bus_stops_df)}件)")
        
        # 地図の作成
        print(f"\n地図を作成中...")
        visualizer = MapVisualizer(center_lat=args.lat, center_lon=args.lon)
        
        # 起点を追加
        visualizer.add_center_marker(args.lat, args.lon, "起点")
        
        # 駅とバス停を追加
        visualizer.add_stations(stations_df)
        visualizer.add_bus_stops(bus_stops_df)
        
        # 到達可能エリアのポリゴンを追加
        if "coordinates" in reachable_data:
            visualizer.add_reachable_polygon(reachable_data["coordinates"])
        
        # 地図の保存
        visualizer.save_map(args.map_file)
        print(f"地図を保存しました: {args.map_file}")
        
    except KeyboardInterrupt:
        print("\n処理を中断しました")
        sys.exit(0)
    except Exception as e:
        print(f"\nエラーが発生しました: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()