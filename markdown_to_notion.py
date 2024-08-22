from openai import OpenAI 
import re


def extract_values_from_markdown(markdown_text):
    """
    使用 OpenAI API 从 Markdown 文本中提取 title, tags, url, description_content.
    
    参数:
    - markdown_text: 包含 Markdown 内容的字符串.
    
    返回:
    - title: 提取的标题.
    - tags: 提取的标签列表.
    - url: 提取的URL.
    - description_content: 提取的描述内容.
    """
    completion = client.chat.completions.create(
        model="glm-4",
        messages=[
            {"role": "system", "content": "你是一个聪明且富有创造力的助手，能够从复杂的文本中提取关键信息，并将其以结构化的形式输出。"},
            {"role": "user", "content": (
                f"请从以下Markdown文本中提取以下信息：\n"
                f"1. **title**: 标题应该是文本中最能代表主要主题的短语或句子。\n"
                f"2. **tags**: 标签应该是与主题相关的关键字或短语，可以是文本中明确标注的标签或从内容中推测的标签。\n"
                f"3. **url**: 提取最相关的URL链接，这通常是指向主要资源或示例的链接。\n"
                f"4. **description_content**: 这是一个简要总结，包含文本的核心内容，应该包括最重要的信息或功能点。\n\n"
                f"请根据这些说明从以下Markdown文本中提取信息：\n{markdown_text}"
            )}
        ],
        top_p=0.7,
        temperature=0.9
    )

    # 获取AI返回的内容
    extracted_data = completion.choices[0].message.content
    
    # 打印返回的内容以进行调试
    print("Extracted Data:", extracted_data)
    
    # 手动解析返回的内容
    try:
        # 提取 title
        title = extracted_data.split("**title**:")[1].split("\n")[0].strip().strip('"')
        
        # 提取 tags 部分
        tags_section = extracted_data.split("**tags**:")[1].split("**url**:")[0].strip()
        tags_list = re.findall(r'-\s*["“]?(.*?)["”]?\n', tags_section)
        tags = [{"name": tag} for tag in tags_list if tag]

        # 提取 URL
        url_match = re.search(r'\((http[s]?://[^\)]+)\)', extracted_data)
        url = url_match.group(1) if url_match else ''

        # 提取 description_content
        description_content = extracted_data.split("**description_content**:")[1].strip()
        
    except Exception as e:
        print("Error parsing data:", str(e))
        return None, None, None, None
    
    return title, tags, url, description_content

# 示例Markdown文本
if __name__ == "__main__":
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
    
    # 测试提取功能
    title, tags, url, description_content = extract_values_from_markdown(markdown_text)
    
    if title and tags and url and description_content:
        print(f"title = {title}")
        print(f"tags = {tags}")
        print(f"url = {url}")
        print(f"description_content = {description_content}")
    else:
        print("Failed to extract data.")
