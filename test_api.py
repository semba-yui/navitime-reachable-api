#!/usr/bin/env python3
"""
NAVITIME Reachable API のエンドポイントをテストするスクリプト
"""

import os
import requests
import json
from pprint import pprint


def test_endpoint(endpoint_name, params, headers):
    """エンドポイントをテスト"""
    base_url = "https://navitime-reachable.p.rapidapi.com"
    url = f"{base_url}/{endpoint_name}"
    
    print(f"\n{'='*60}")
    print(f"Testing: {endpoint_name}")
    print(f"URL: {url}")
    print(f"Params: {params}")
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Success! Response keys: {list(data.keys())}")
            
            # レスポンスの構造を表示
            if "items" in data:
                print(f"  - items count: {len(data['items'])}")
                if data['items']:
                    print(f"  - first item keys: {list(data['items'][0].keys())}")
                    print(f"  - first item sample:")
                    pprint(data['items'][0], indent=4, depth=2)
            
            # 全体のレスポンスを保存
            with open(f"response_{endpoint_name}.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Response saved to: response_{endpoint_name}.json")
            
            return True
        else:
            print(f"Failed with status: {response.status_code}")
            if response.text:
                print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"Error: {e}")
        return False


def main():
    # APIキーの確認
    api_key = os.environ.get("RAPIDAPI_KEY")
    if not api_key:
        print("Error: RAPIDAPI_KEY environment variable not set")
        return
    
    headers = {
        "x-rapidapi-host": "navitime-reachable.p.rapidapi.com",
        "x-rapidapi-key": api_key
    }
    
    # 茅場町の座標
    lat = 35.6817137
    lon = 139.7777797
    
    # テストするエンドポイント
    endpoints = [
        # README.mdのサンプルから
        "reachable_motorcycle",
        # 公共交通機関系の可能性があるもの
        "reachable_transit",
        "reachable_transit_walking",
        "reachable_train",
        "reachable_bus",
        "reachable_public",
        "reachable_public_transport",
        # 徒歩系
        "reachable_walking",
        "reachable_walk",
        "reachable_on_foot",
        # 一般的な名前
        "reachable",
        "reachable_area",
        "reachable_polygon"
    ]
    
    # 基本パラメータ
    base_params = {
        "start": f"{lat},{lon}",
        "term": "30",
        "partition_count": "36",
        "datum": "wgs84",
        "coord_unit": "degree"
    }
    
    # 成功したエンドポイントを記録
    successful_endpoints = []
    
    for endpoint in endpoints:
        params = base_params.copy()
        
        # motorcycle用の追加パラメータ
        if "motorcycle" in endpoint:
            params["motorcycle_fare"] = "toll"
        
        if test_endpoint(endpoint, params, headers):
            successful_endpoints.append(endpoint)
    
    print(f"\n{'='*60}")
    print("Summary:")
    print(f"Successful endpoints: {successful_endpoints}")


if __name__ == "__main__":
    main()