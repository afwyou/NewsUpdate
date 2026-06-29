import json
import urllib.request
import re

def fetch_ctee_newspaper_headlines():
    url = "https://newspaper.ctee.com.tw/"
    news_list = []
    
    try:
        # 1. 模擬瀏覽器發出請求，下載網頁原始碼
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        )
        with urllib.request.urlopen(req, timeout=15) as response:
            html = response.read().decode('utf-8')
            
        # 2. 精準鎖定頭條區塊 (使用正則表達式撈取新聞標題與連結)
        # 工商時報報紙首頁的頭條連結格式通常包含 /share-content/
        pattern = r'<a\s+[^>]*href="([^"]*share-content[^"]*)"[^>]*>([\s\S]*?)<\/a>'
        matches = re.findall(pattern, html)
        
        seen_urls = set()
        for link, title_html in matches:
            # 補足相對路徑網址
            full_url = link if link.startswith('http') else f"https://newspaper.ctee.com.tw{link}"
            
            # 清洗標題，移除 HTML 標籤（如 <span> 或 <h3> 等）與空白
            title = re.sub(r'<[^>]+>', '', title_html).strip()
            
            # 過濾掉空標題、重複的連結，以及非頭條的雜訊
            if title and full_url not in seen_urls and len(title) > 4:
                seen_urls.add(full_url)
                news_list.append({
                    "source": "工商時報 (報紙頭條)",
                    "title": title,
                    "url": full_url,
                    "time": "今日頭條"
                })
                
    except Exception as e:
        print(f"抓取工商時報報紙頭條失敗: {e}")
        
    return news_list

def main():
    print("正在精準抓取《工商時報》報紙頭條焦點...")
    headlines = fetch_ctee_newspaper_headlines()
    
    # 將抓取到的頭條存進 news.json
    with open('news.json', 'w', encoding='utf-8') as f:
        json.dump(headlines, f, ensure_ascii=False, indent=4)
        
    print(f"更新成功！共抓取到 {len(headlines)} 則今日報紙大頭條。")

if __name__ == "__main__":
    main()
