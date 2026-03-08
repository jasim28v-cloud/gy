import requests
from bs4 import BeautifulSoup
from datetime import datetime

def run_trends_scraper():
    # مصدر التريندات العالمية
    trends_url = "https://trends.google.com/trending/rss?geo=US"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    try:
        # الرابط الذكي المعتمد الذي أرسلته
        smart_ad_link = "https://data527.click/21330bf1d025d41336e6/57154ac610/?placementName=default"
        
        # 1. جلب بيانات التريند
        response = requests.get(trends_url, headers=headers, timeout=20)
        soup = BeautifulSoup(response.content, 'xml')
        items = soup.find_all('item')
        
        trends_html = ""
        for i, item in enumerate(items[:12]):
            title = item.title.text
            traffic = item.find('ht:approx_traffic').text if item.find('ht:approx_traffic') else "+5K"
            description = item.description.text if item.description else "موضوع رائج الآن عالمياً"
            
            trends_html += f'''
            <div class="t-card">
                <a href="{smart_ad_link}" target="_blank">
                    <div class="t-header">
                        <span class="t-number">#{i+1}</span>
                        <span class="t-traffic">{traffic} بحث</span>
                    </div>
                    <div class="t-body">
                        <h3>{title}</h3>
                        <p>{description[:90]}...</p>
                    </div>
                    <div class="t-footer">
                        <span class="t-tag">Trending Now</span>
                        <span class="t-btn">تحليل</span>
                    </div>
                </a>
            </div>'''

        # 2. بناء الواجهة النيون الفخمة
        update_time = datetime.now().strftime('%H:%M')
        full_html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VORTEX | رادار التريند</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Cairo:wght@400;700&display=swap" rel="stylesheet">
    <style>
        :root {{ --bg: #050505; --card: #0d0d0d; --neon: #00f2ff; --purple: #7000ff; }}
        body {{ background: var(--bg); color: #fff; font-family: 'Cairo', sans-serif; margin: 0; }}
        header {{ padding: 20px 5%; background: rgba(0,0,0,0.9); border-bottom: 1px solid var(--neon); display: flex; justify-content: space-between; position: sticky; top: 0; z-index: 100; }}
        .logo {{ font-family: 'Orbitron', sans-serif; color: var(--neon); font-size: 20px; text-decoration: none; text-shadow: 0 0 5px var(--neon); }}
        .container {{ max-width: 1100px; margin: 20px auto; padding: 0 15px; }}
        .trends-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; }}
        .t-card {{ background: var(--card); border: 1px solid #1a1a1a; border-radius: 15px; transition: 0.3s; }}
        .t-card:hover {{ border-color: var(--neon); transform: translateY(-5px); box-shadow: 0 0 15px rgba(0,242,255,0.1); }}
        .t-card a {{ text-decoration: none; color: inherit; display: block; padding: 20px; }}
        .t-header {{ display: flex; justify-content: space-between; margin-bottom: 15px; }}
        .t-traffic {{ color: var(--neon); font-size: 11px; font-weight: bold; border: 1px solid var(--neon); padding: 2px 8px; border-radius: 20px; }}
        .t-body h3 {{ font-size: 17px; margin: 0 0 10px; color: #fff; }}
        .t-body p {{ font-size: 12px; color: #777; }}
        .t-footer {{ display: flex; justify-content: space-between; align-items: center; margin-top: 20px; }}
        .t-btn {{ background: var(--purple); color: #fff; padding: 4px 12px; border-radius: 5px; font-size: 11px; }}
        .ad-area {{ text-align: center; margin: 30px 0; }}
        footer {{ text-align: center; padding: 40px; color: #333; font-size: 12px; }}
    </style>
</head>
<body>
    <header>
        <a href="#" class="logo">VORTEX TRENDS</a>
        <div style="font-size: 11px; color: var(--neon);">Live: {update_time}</div>
    </header>
    <div class="container">
        <div class="ad-area">
            <script type="text/javascript" src="{smart_ad_link}"></script>
        </div>
        <div class="trends-grid">{trends_html}</div>
        <div class="ad-area">
            <script type="text/javascript" src="{smart_ad_link}"></script>
        </div>
    </div>
    <footer>VORTEX TRENDS © 2026</footer>
</body>
</html>'''

        with open("index.html", "w", encoding="utf-8") as f:
            f.write(full_html)
    except Exception as e: print(f"Error: {e}")

if __name__ == "__main__":
    run_trends_scraper()
