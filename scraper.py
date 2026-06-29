import json
import urllib.request
import re

def fetch_ctee_headlines():
    """抓取工商時報報紙頭條"""
    url = "https://newspaper.ctee.com.tw/"
    news_list = []
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req, timeout=15) as response:
            html = response.read().decode('utf-8')
        
        # 使用更寬鬆、適應力更強的正則表達式抓取包含 share-content 的連結與標題
        pattern = r'<a\s+[^>]*href="([^"]*share-content[^"]*)"[^>]*>([\s\S]*?)<\/a>'
        matches = re.findall(pattern, html)
        
        seen_urls = set()
        for link, title_html in matches:
            full_url = link if link.startswith('http') else f"https://newspaper.ctee.com.tw{link}"
            # 移除所有 HTML 標籤，只留下純文字標題
            title = re.sub(r'<[^>]+>', '', title_html).strip()
            # 移除換行符號與多餘空白
            title = title.replace('\n', '').replace('\r', '').strip()
            
            if title and len(title) > 5 and full_url not in seen_urls:
                seen_urls.add(full_url)
                news_list.append({
                    "source": "工商時報",
                    "title": title,
                    "url": full_url,
                    "time": "今日頭條"
                })
    except Exception as e:
        print(f"抓取工商時報失敗: {e}")
    return news_list

def fetch_edn_headlines():
    """抓取經濟日報焦點頭條 (備用與豐富水源)"""
    url = "https://money.udn.com/money/index"
    news_list = []
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req, timeout=15) as response:
            html = response.read().decode('utf-8')
        
        # 抓取經濟日報首頁的重點新聞連結
        pattern = r'<a\s+[^>]*href="([^"]*/story/[^"]*)"[^>]*title="([^"]+)"'
        matches = re.findall(pattern, html)
        
        seen_urls = set()
        for link, title in matches:
            if "money.udn.com" not in link:
                full_url = f"https://money.udn.com{link}"
            else:
                full_url = link
            
            title = title.strip()
            if title and len(title) > 5 and full_url not in seen_urls:
                seen_urls.add(full_url)
                news_list.append({
                    "source": "經濟日報",
                    "title": title,
                    "url": full_url,
                    "time": "焦點頭條"
                })
    except Exception as e:
        print(f"抓取經濟日報失敗: {e}")
    return news_list

def main():
    print("開始執行財經報紙頭條爬蟲...")
    
    all_news = []
    # 同時抓取兩家
    all_news.extend(fetch_ctee_headlines())
    all_news.extend(fetch_edn_headlines())
    
    # 如果真的不幸都沒抓到，放一則測試公告，避免網頁完全空白噴錯
    if not all_news:
        all_news.append({
            "source": "系統通知",
            "title": "今天暫時沒有抓取到報紙頭條，請稍後再試。",
            "url": "https://newspaper.ctee.com.tw/",
            "time": ""
        })
        
    # 寫入 news.json
    with open('news.json', 'w', encoding='utf-8') as f:
        json.dump(all_news, f, ensure_ascii=False, indent=4)
        
    print(f"執行完畢！成功寫入 {len(all_news)} 則新聞至 news.json")

if __name__ == "__main__":
    main()
