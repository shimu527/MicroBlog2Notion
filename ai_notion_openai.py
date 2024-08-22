import requests
import re
import random
from markdown_to_notion import extract_values_from_markdown  # 导入 extract_values_from_markdown 函数
import config  # 导入配置文件




#数据处理
def parse_description(content):
    """
    解析包含数学公式的字符串，将其转换为Notion识别的富文本格式。
    """
    # 正则表达式匹配 $...$ 中的内容
    pattern = re.compile(r'(\$.*?\$)')
    
    # 初始化结果列表
    description = []
    
    # 使用 split 保留分隔符进行拆分
    parts = pattern.split(content)
    
    for part in parts:
        if part.startswith('$') and part.endswith('$'):
            # 移除 $ 符号，并作为数学公式处理
            equation_content = part[1:-1]
            description.append({
                "type": "equation",
                "equation": {
                    "expression": equation_content
                }
            })
        else:
            # 处理普通文本
            if part:  # 跳过空字符串
                description.append({
                    "type": "text",
                    "text": {
                        "content": part
                    }
                })
    
    return description




def add_row_to_notion_database(database_id, title, tags, url, description_content, auth_token):
    """
    向Notion数据库中添加一行新的数据。
    """
    url_endpoint = "https://api.notion.com/v1/pages"
    
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

        # 获取现有的标签和颜色
    existing_tags = fetch_existing_tags(database_id, auth_token)
    
    # 检查并处理传入的标签
    for tag in tags:
        tag_name = tag["name"]
        
        if tag_name in existing_tags:
            # 如果标签已存在，检查颜色是否匹配
            if "color" in tag:
                if tag["color"] != existing_tags[tag_name]:
                    raise ValueError(f"Color mismatch for tag '{tag_name}': expected '{existing_tags[tag_name]}', got '{tag['color']}'")
            else:
                # 如果标签存在但没有指定颜色，使用现有的颜色
                tag["color"] = existing_tags[tag_name]
        else:
            # 如果标签不存在，为其分配颜色
            if "color" not in tag or not tag["color"]:
                tag["color"] = get_random_color()
    
    # 使用 parse_description 函数将 description_content 解析为富文本格式
    description = parse_description(description_content)
    
    data = {
        "parent": {"database_id": database_id},
        "properties": {
            "Name": {
                "title": [
                    {
                        "text": {
                            "content": title
                        }
                    }
                ]
            },
            "Tags": {
                "multi_select": tags
            },
            "URL": {
                "url": url
            },
            "Description": {
                "rich_text": description
            }
        }
    }
    
    response = requests.post(url_endpoint, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

# Notion支持的所有颜色
notion_colors = [
    "default",
    "gray", "brown", "orange", "yellow", "green", "blue", "purple", "pink", "red"
]

def get_random_color():
    """
    从Notion支持的颜色列表中随机选择一个颜色。
    
    返回:
    - 一个随机选择的颜色（字符串）。
    """
    return random.choice(notion_colors)


def fetch_existing_tags(database_id, auth_token):
    """
    获取数据库中现有的标签及其颜色。
    
    参数:
    - database_id: Notion数据库的ID。
    - auth_token: Notion API的授权令牌。
    
    返回:
    - 一个字典，其中键是标签的名称，值是标签的颜色。
    """
    url = f"https://api.notion.com/v1/databases/{database_id}"
    
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Notion-Version": "2022-06-28"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        properties = data['properties']
        tags_property = properties.get('Tags', {})
        
        if tags_property.get('type') == 'multi_select':
            options = tags_property['multi_select']['options']
            return {option['name']: option['color'] for option in options}
        else:
            raise ValueError("The 'Tags' property is not of type 'multi_select'.")
    else:
        response.raise_for_status()




# 示例用法
database_id = "4ef8e1cd5cf74779bebf6c7aabcc710e"
auth_token = "secret_v7Nehqb2F7gDo1MJtnbjubKEcdVkwH5ce3aXrUVil5K"
page_id = "4d6470a832e943ba814bad07cb5e8d51"



# # 定义新行的值
# title = "New Project"
# tags = [{"name": "从来没有"}, {"name": "不好"}]
# url = "https://example.com"
# description_content = "ceshicesh测试$ssdsd^2$你好吗$fdf^2$时代的" # 定义包含数学公式和普通文本的描述字符串



# 使用 Markdown 文本，通过 OpenAI API 提取所需的数据
markdown_text = """
> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [web.okjike.com](https://web.okjike.com/originalPost/66c3db06d5f82749c472ac5c)

> ⭕️ 轻量级 LLM 网页数据爬取 分享一个最近在用的数据爬取工具，parsera，有点类似 jina ✅ 支持多种 LLM api，包括本地 ✅ 官方提供免费 api ✅ 支持提取多种类型的文本数据 ✅ ......

[![](https://cdnv2.ruguoapp.com/FrUiVLnSvlzCTGnSnQNMaW_MTBNLv2.jpg?imageMogr2/auto-orient/heic-exif/1/format/jpeg/thumbnail/!120x120r/gravity/Center/crop/!120x120a0a0)](/u/4E822130-4B7B-4DB9-A4CA-B326397ADB32)[不务正业小胡同学](/u/4E822130-4B7B-4DB9-A4CA-B326397ADB32)[1 天前](/originalPost/66c3db06d5f82749c472ac5c)

⭕️ 轻量级 LLM 网页数据爬取  
分享一个最近在用的数据爬取工具，parsera，有点类似 jina  
✅ 支持多种 LLM api，包括本地  
✅ 官方提供免费 api  
✅ 支持提取多种类型的文本数据  
✅ 自动内容发现，多页面爬取  
🔗 [github.com](https://github.com/raznem/parsera)![](https://cdnv2.ruguoapp.com/Fo14Pgc4Q2pHVw0l0fEAANFRx_ktv3.jpg?imageMogr2/auto-orient/thumbnail/400x2000%3E/quality/70/interlace/1)[JitHub 程序员](/topic/55e02198dcef9f0e00d7b3c3)
"""

# 从 extract_values_from_markdown 函数中获取 title, tags, url, description_content
title, tags, url, description_content = extract_values_from_markdown(markdown_text)

# 使用默认值避免 NoneType 错误
title = title or 'Untitled'
tags = tags or []
url = url or 'https://example.com'
description_content = description_content or ''

# 调用函数添加新行
new_page_data = add_row_to_notion_database(database_id, title, tags, url, description_content, auth_token)

# 打印新创建的页面数据
print(new_page_data)
