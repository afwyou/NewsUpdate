import json
import urllib.request
import re

def fetch_ctee_headlines():
    """精準抓取工商時報報紙頭條（超強防阻擋與解碼版）"""
    url = "https://newspaper.ctee.com.tw/"
    news_list = []
    try:
        # 模擬完全真實的 Chrome 瀏覽器外殼，防止被網站防爬機制封鎖
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7'
        }
        
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as response:
            html = response.read().decode('utf-8', errors='ignore')
        
        # 工商時報實體報紙網頁的連結特徵，通常包含 share-content 或 content
        # 我們用最直覺的「雙引號」跟「單引號」通殺模式來搜尋連結
        pattern = r'href=["\']([^"\']*(?:share-content|content)[^"\']*)["\'][^>]*>([\s\S]*?)<\/a>'
        matches = re.findall(pattern, html)
        
        seen_urls = set()
        for link, title_html in matches:
            # 確保網址是完整的路徑
            if link.startswith('//'):
                full_url = f"https:{link}"
            elif link.startswith('/'):
                full_url = f"https://newspaper.ctee.com.tw{link}"
            elif not link.startswith('http'):
                full_url = f"https://newspaper.ctee.com.tw/{link}"
            else:
                full_url = link
                
            # 徹底清洗標題文字
            title = re.sub(r'<[^>]+>', '', title_html)  # 移除 HTML 標籤
            title = re.sub(r'\s+', ' ', title).strip() # 移除連續空白、換行
            
            # 過濾無效字串與重複內容
            if title and len(title) > 5 and "請登入" not in title and full_url not in seen_urls:
                seen_urls.add(full_url)
                news_list.append({
                    "source": "工商時報",
                    "title": title,
                    "url": full_url,
                    "time": "今日頭條"
                })
    except Exception as e:
        print(f"抓取工商時報失敗原因: {e}")
    return news_list

def fetch_edn_headlines():
    """抓取經濟日報焦點頭條（維持原先成功運作的邏輯）"""
    url = "https://money.udn.com/money/index"
    news_list = []
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req, timeout=15) as response:
            html = response.read().decode('utf-8', errors='ignore')
        
        pattern = r'<a\s+[^>]*href="([^"]*/story/[^"]*)"[^>]*title="([^"]+)"'
        matches = re.findall(pattern, html)
        
        seen_urls = set()
        for link, title in matches:
            full_url = link if "money.udn.com" in link else f"https://money.udn.com{link}"
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
    print("開始執行雙報頭條即時監控爬蟲...")
    
    all_news = []
    all_news.extend(fetch_ctee_headlines())
    all_news.extend(fetch_edn_headlines())
    
    if not all_news:
        all_news.append({
            "source": "系統通知",
            "title": "今天暫時沒有抓取到兩大報頭條，請稍後再試。",
            "url": "https://newspaper.ctee.com.tw/",
            "time": ""
        })
        
    with open('news.json', 'w', encoding='utf-8') as f:
        json.dump(all_news, f, ensure_ascii=False, indent=4)
        
    print(f"執行完畢！成功寫入 {len(all_news)} 則新聞至 news.json")

if __name__ == "__main__":
    main()
