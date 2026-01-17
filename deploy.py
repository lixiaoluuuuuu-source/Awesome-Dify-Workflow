import os
import requests

def main():
    # 从环境变量获取密钥和应用 ID
    dify_api_key = os.getenv("DIFY_API_KEY")
    dify_app_id = os.getenv("DIFY_APP_ID")
    
    if not dify_api_key or not dify_app_id:
        print("Error: DIFY_API_KEY 或 DIFY_APP_ID 未设置")
        return
    
    # Dify 部署接口（根据实际接口调整）
    url = f"https://api.dify.ai/v1/apps/{dify_app_id}/deploy"
    headers = {
        "Authorization": f"Bearer {dify_api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        print("部署成功！", response.json())
    except Exception as e:
        print("部署失败：", str(e))

if __name__ == "__main__":
    main()
