import requests
import json

#获取database所有数据
def get_notion_database_content(database_id, auth_token):
    """
    获取Notion数据库的全部内容，并将其写入到本地JSON文件。
    
    参数:
    - database_id: Notion数据库的ID。
    - auth_token: Notion API的授权令牌。
    
    返回:
    - 无返回值，JSON数据将被写入到本地文件中。
    """
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    
    response = requests.post(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        with open("notion_database_content.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    else:
        response.raise_for_status()



#获取某一行的数据
def get_notion_page_data(database_id, page_id, auth_token):
    """
    获取Notion数据库中某一行（页面）的数据，并转换为JSON格式。
    
    参数:
    - database_id: Notion数据库的ID。
    - page_id: 页面ID（即行ID）。
    - auth_token: Notion API的授权令牌。
    
    返回:
    - 页面数据的JSON格式（Python字典）。
    """
    url = f"https://api.notion.com/v1/pages/{page_id}"
    
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        page_data = response.json()
        with open("notion_page_data.json", "w", encoding="utf-8") as f:
            json.dump(page_data, f, ensure_ascii=False, indent=4)
        return page_data
    else:
        response.raise_for_status()

# 获取整个数据库的内容并保存到本地文件
# get_notion_database_content(database_id, auth_token)

# 获取特定页面的数据并保存到本地文件
# page_data = get_notion_page_data(database_id, page_id, auth_token)