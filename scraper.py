import json
import xml.etree.ElementTree as ET
import urllib.request

def fetch_rss_news(url, source_name):
    news_list = []
    try:
        # 設定請求頭，模擬瀏覽器存取
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        )
        with urllib.request.urlopen(req, timeout=15) as response:
            xml_data = response.read()
            
        # 解析 XML 結構
        root = ET.fromstring(xml_data)
        for item in root.findall('.//item'):
            title = item.find('title').text if item.find('title') is not None else ''
            link = item.find('link').text if item.find('link') is not None else ''
            pub_date = item.find('pubDate').text if item.find('pubDate') is not None else ''
            
            # 清洗標題與時間字串
            title = title.strip()
            link = link.strip()
            
            if title and link:
                news_list.append({
                    "source": source_name,
                    "title": title,
                    "url": link,
                    "time": pub_date
                })
    except Exception as e:
        print(f"抓取 {source_name} 失敗: {e}")
    return news_list

def main():
    # 1. 定義兩家報社的 RSS 財經/證券/產業焦點網址
    # 註：若報社未來有變更 RSS 網址，直接替換此處即可
    ctee_url = "https://vocus.cc/rss/64f83b1efd89780001099fd1.xml" # 範例，工商時報焦點通常有提供公開RSS
    # 這裡我們使用兩家報社最核心的即時證券/產業 RSS 饋送
    urls = {
        "工商時報": "https://ctee.com.tw/feed", 
        "經濟日報": "https://money.udn.com/rss/news/1001/5591/5607" 
    }
    
    all_news = []
    for source, url in urls.items():
        print(f"正在抓取 {source}...")
        all_news.extend(fetch_rss_news(url, source))
        
    # 2. 將所有新聞寫入 news.json
    with open('news.json', 'w', encoding='utf-8') as f:
        json.dump(all_news, f, ensure_ascii=False, indent=4)
    print(f"排程執行成功！共抓取 {len(all_news)} 則頭條新聞。")

if __name__ == "__main__":
    main()
