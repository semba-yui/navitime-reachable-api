"""
Foliumを使用して地図の可視化を行うモジュール
"""

import folium
import pandas as pd
from typing import List, Tuple, Optional
from pathlib import Path


class MapVisualizer:
    """地図の可視化を行うクラス"""
    
    def __init__(self, center_lat: float, center_lon: float, zoom_start: int = 13):
        """
        Args:
            center_lat: 地図の中心緯度
            center_lon: 地図の中心経度
            zoom_start: 初期ズームレベル
        """
        self.map = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=zoom_start
        )
        
        # 色の定義（所要時間に応じた色分け）
        self.time_colors = {
            10: "#2ECC40",  # 緑: 10分以内
            20: "#FFDC00",  # 黄: 20分以内
            30: "#FF851B",  # オレンジ: 30分以内
            float('inf'): "#FF4136"  # 赤: 30分超
        }
    
    def add_center_marker(self, lat: float, lon: float, name: str = "起点") -> None:
        """
        起点のマーカーを追加
        
        Args:
            lat: 緯度
            lon: 経度
            name: マーカーの名前
        """
        folium.Marker(
            location=[lat, lon],
            popup=name,
            tooltip=name,
            icon=folium.Icon(color="red", icon="star")
        ).add_to(self.map)
    
    def add_stations(self, stations_df: pd.DataFrame) -> None:
        """
        駅のマーカーを追加
        
        Args:
            stations_df: 駅データのDataFrame
        """
        for _, row in stations_df.iterrows():
            time = row.get("所要時間（分）", 0)
            transfers = row.get("乗り換え回数", 0)
            
            # 所要時間に応じた色を選択
            color = self._get_color_by_time(time)
            
            # ポップアップとツールチップのテキスト
            popup_text = f"""
            <b>{row.get('駅名', '')}</b><br>
            所要時間: {time}分<br>
            乗り換え: {transfers}回<br>
            路線: {row.get('路線', '')}
            """
            
            tooltip_text = f"{row.get('駅名', '')} ({time}分, 乗換{transfers}回)"
            
            folium.Marker(
                location=[row.get("緯度", 0), row.get("経度", 0)],
                popup=folium.Popup(popup_text, max_width=300),
                tooltip=tooltip_text,
                icon=folium.Icon(color=color, icon="train", prefix="fa")
            ).add_to(self.map)
    
    def add_bus_stops(self, bus_stops_df: pd.DataFrame) -> None:
        """
        バス停のマーカーを追加
        
        Args:
            bus_stops_df: バス停データのDataFrame
        """
        for _, row in bus_stops_df.iterrows():
            time = row.get("所要時間（分）", 0)
            transfers = row.get("乗り換え回数", 0)
            
            # 所要時間に応じた色を選択
            color = self._get_color_by_time(time)
            
            # ポップアップとツールチップのテキスト
            popup_text = f"""
            <b>{row.get('バス停名', '')}</b><br>
            所要時間: {time}分<br>
            乗り換え: {transfers}回<br>
            路線: {row.get('路線', '')}
            """
            
            tooltip_text = f"{row.get('バス停名', '')} ({time}分, 乗換{transfers}回)"
            
            folium.Marker(
                location=[row.get("緯度", 0), row.get("経度", 0)],
                popup=folium.Popup(popup_text, max_width=300),
                tooltip=tooltip_text,
                icon=folium.Icon(color=color, icon="bus", prefix="fa")
            ).add_to(self.map)
    
    def add_reachable_polygon(self, coordinates: List[List[float]]) -> None:
        """
        到達可能エリアのポリゴンを追加
        
        Args:
            coordinates: ポリゴンの座標リスト [[lat, lon], ...]
        """
        if not coordinates:
            return
        
        # 座標の形式を確認して変換
        polygon_coords = []
        for coord in coordinates:
            if isinstance(coord, list) and len(coord) >= 2:
                # 座標は既に [lat, lon] 形式と想定
                polygon_coords.append(coord)
        
        if polygon_coords:
            folium.Polygon(
                locations=polygon_coords,
                color="#0074D9",
                weight=2,
                fill=True,
                fillColor="#0074D9",
                fillOpacity=0.2,
                tooltip="到達可能エリア"
            ).add_to(self.map)
    
    def _get_color_by_time(self, time: int) -> str:
        """
        所要時間に応じた色を取得
        
        Args:
            time: 所要時間（分）
            
        Returns:
            色名
        """
        for threshold, color in sorted(self.time_colors.items()):
            if time <= threshold:
                return color.replace("#", "").lower()
        return "gray"
    
    def add_legend(self) -> None:
        """凡例を追加"""
        legend_html = '''
        <div style="position: fixed; 
                    top: 50px; right: 50px; width: 200px; height: 150px; 
                    background-color: white; z-index:9999; font-size:14px;
                    border:2px solid grey; border-radius: 5px">
        <p style="margin: 10px;"><b>所要時間</b></p>
        <p style="margin: 10px;"><i class="fa fa-circle" style="color:#2ECC40"></i> 10分以内</p>
        <p style="margin: 10px;"><i class="fa fa-circle" style="color:#FFDC00"></i> 20分以内</p>
        <p style="margin: 10px;"><i class="fa fa-circle" style="color:#FF851B"></i> 30分以内</p>
        </div>
        '''
        self.map.get_root().html.add_child(folium.Element(legend_html))
    
    def save_map(self, filepath: Path) -> None:
        """
        地図をHTMLファイルとして保存
        
        Args:
            filepath: 保存先のファイルパス
        """
        # 凡例を追加
        self.add_legend()
        
        # ファイルに保存
        self.map.save(str(filepath))