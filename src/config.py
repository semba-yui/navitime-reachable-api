"""
設定管理モジュール
"""

import os
from pathlib import Path


class Config:
    """アプリケーションの設定を管理するクラス"""
    
    def __init__(self):
        """設定の初期化"""
        # APIキーを環境変数から取得
        self.api_key = os.environ.get("RAPIDAPI_KEY", "")
        
        if not self.api_key:
            raise ValueError(
                "環境変数 RAPIDAPI_KEY が設定されていません。\n"
                "export RAPIDAPI_KEY='your_api_key' を実行してください。"
            )
        
        # デフォルトの設定値
        self.default_lat = 35.6817137  # 茅場町駅の緯度
        self.default_lon = 139.7777797  # 茅場町駅の経度
        self.default_time_limit = 30  # デフォルトの到達時間（分）
        self.default_max_transfers = 1  # デフォルトの最大乗り換え回数
        
        # 出力ディレクトリ
        self.output_dir = Path("csv")
        self.map_filename = "reachable_map.html"
        
        # API設定
        self.api_timeout = 30  # APIタイムアウト（秒）
        self.api_retry_count = 3  # APIリトライ回数