"""
データ処理とCSV出力を行うモジュール
"""

import pandas as pd
from pathlib import Path
from typing import Dict, Tuple, List, Optional


class DataProcessor:
    """APIレスポンスデータを処理し、CSV形式で出力するクラス"""
    
    def process_reachable_data(
        self, 
        data: Dict,
        max_transfers: Optional[int] = None
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        到達可能エリアデータを処理し、駅とバス停のDataFrameを作成
        
        Args:
            data: APIレスポンスデータ
            max_transfers: 最大乗り換え回数でフィルタリング
            
        Returns:
            (駅のDataFrame, バス停のDataFrame)
        """
        stations = data.get("stations", [])
        bus_stops = data.get("bus_stops", [])
        
        # 駅データの処理
        stations_df = self._process_stations(stations, max_transfers)
        
        # バス停データの処理
        bus_stops_df = self._process_bus_stops(bus_stops, max_transfers)
        
        return stations_df, bus_stops_df
    
    def _process_stations(
        self, 
        stations: List[Dict],
        max_transfers: Optional[int] = None
    ) -> pd.DataFrame:
        """
        駅データを処理してDataFrameに変換
        
        Args:
            stations: 駅データのリスト
            max_transfers: 最大乗り換え回数
            
        Returns:
            駅のDataFrame
        """
        if not stations:
            return pd.DataFrame(columns=[
                "駅名", "緯度", "経度", "種類", "路線", "所要時間（分）", "乗り換え回数"
            ])
        
        processed_stations = []
        for station in stations:
            # 乗り換え回数でフィルタリング
            if max_transfers is not None and station.get("transfers", 0) > max_transfers:
                continue
            
            # 路線情報の処理
            lines = station.get("lines", [])
            if isinstance(lines, list):
                lines_str = ", ".join(lines)
            else:
                lines_str = str(lines) if lines else ""
            
            processed_stations.append({
                "駅名": station.get("name", ""),
                "緯度": station.get("lat", 0),
                "経度": station.get("lon", 0),
                "種類": "駅",
                "路線": lines_str,
                "所要時間（分）": station.get("time", 0),
                "乗り換え回数": station.get("transfers", 0)
            })
        
        df = pd.DataFrame(processed_stations)
        
        # 所要時間でソート
        if not df.empty:
            df = df.sort_values("所要時間（分）")
        
        return df
    
    def _process_bus_stops(
        self, 
        bus_stops: List[Dict],
        max_transfers: Optional[int] = None
    ) -> pd.DataFrame:
        """
        バス停データを処理してDataFrameに変換
        
        Args:
            bus_stops: バス停データのリスト
            max_transfers: 最大乗り換え回数
            
        Returns:
            バス停のDataFrame
        """
        if not bus_stops:
            return pd.DataFrame(columns=[
                "バス停名", "緯度", "経度", "種類", "路線", "所要時間（分）", "乗り換え回数"
            ])
        
        processed_bus_stops = []
        for bus_stop in bus_stops:
            # 乗り換え回数でフィルタリング
            if max_transfers is not None and bus_stop.get("transfers", 0) > max_transfers:
                continue
            
            # 路線情報の処理
            lines = bus_stop.get("lines", [])
            if isinstance(lines, list):
                lines_str = ", ".join(lines)
            else:
                lines_str = str(lines) if lines else ""
            
            processed_bus_stops.append({
                "バス停名": bus_stop.get("name", ""),
                "緯度": bus_stop.get("lat", 0),
                "経度": bus_stop.get("lon", 0),
                "種類": "バス停",
                "路線": lines_str,
                "所要時間（分）": bus_stop.get("time", 0),
                "乗り換え回数": bus_stop.get("transfers", 0)
            })
        
        df = pd.DataFrame(processed_bus_stops)
        
        # 所要時間でソート
        if not df.empty:
            df = df.sort_values("所要時間（分）")
        
        return df
    
    def save_to_csv(self, df: pd.DataFrame, filepath: Path) -> None:
        """
        DataFrameをCSVファイルに保存
        
        Args:
            df: 保存するDataFrame
            filepath: 保存先のファイルパス
        """
        df.to_csv(filepath, index=False, encoding="utf-8-sig")
    
    def load_from_csv(self, filepath: Path) -> pd.DataFrame:
        """
        CSVファイルからDataFrameを読み込み
        
        Args:
            filepath: 読み込むファイルパス
            
        Returns:
            読み込んだDataFrame
        """
        return pd.read_csv(filepath, encoding="utf-8-sig")