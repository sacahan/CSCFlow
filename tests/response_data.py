import json

response_data = {"swim": ["10", "400", "0"], "gym": ["44", "60", "0"]}
response_mapping = {
    "gym": {"path": "gym.0", "type": "integer"},
    "pool": {"path": "swim.0", "type": "integer"},
}

result = {}

for key, mapping in response_mapping.items():
    try:
        print(f"🔍 Mapping key: {key} with mapping: {mapping}")
        # mapping like: {'path': 'gym.0', 'type': 'integer'}

        value = response_data
        # 根據映射規則的路徑逐層提取資料。
        for path in mapping["path"].split("."):
            print(f"🔗 Extracting path: {path} <--> {value}")

            if isinstance(value, list):
                # 如果 value 是列表，嘗試將 path 轉換為整數索引。
                index = int(path)  # 假設 path 是有效的整數字串。
                value = value[index]
            elif isinstance(value, dict) and path in value:
                value = value[path]
            else:
                raise KeyError(f"Key '{path}' not found in the response data")

        # 如果提取的值是字串，嘗試將其轉換為整數。
        if isinstance(value, str):
            value = int(value)
        result[key] = value
    except Exception as e:
        # 如果資料轉換失敗，記錄錯誤並跳過該鍵。
        print(f"回應資料轉換失敗 {key}: {str(e)}")

print(result)  # 預期輸出: {'gym': 44, 'pool': 10}


str = "35,135"

json.loads(str)  # 這會引發錯誤，因為 str 不是有效的 JSON 格式
