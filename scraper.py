import requests
from bs4 import BeautifulSoup
from datetime import datetime

def run_trends_scraper():
    # مصدر التريندات (Google Trends RSS)
    trends_url = "https://trends.google.com/trending/rss?geo=US"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    try:
        # الرابط الذكي المعتمد (الوحيد الآن)
        smart_ad_link = "https://data527.click/21330bf1d025d41336e6/57154ac610/?placementName=default"
        
        # 1. جلب بيانات التريند
        response = requests.get(trends_url, headers=headers, timeout=20)
        soup = BeautifulSoup(response.content, 'xml')
        items = soup.find_all('item')
        
        trends_html = ""
        for i, item in enumerate(items[:15]):
            title = item.title.text
            traffic = item.find('ht:approx_traffic').text if item.find('ht:approx_traffic') else "+10K"
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
                        <p>{description[:100]}...</p>
                    </div>
                    <div class="t-footer">
                        <span class="t-tag">رائج الآن</span>
                        <span class="t-btn">تحليل التريند</span>
                    </div>
                </a>
            </div>'''

        # 2. بناء الواجهة
        update_time = datetime.now().strftime('%H:%M')
        full_html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VORTEX | رادار التريند العالمي</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&family=Cairo:wght@400;700&display=swap" rel="stylesheet">
    <style>
        :root {{ --bg: #050505; --card: #0f0f0f; --neon: #00f2ff; --purple: #7000ff; --text: #ffffff; }}
        body {{ background: var(--bg); color: var(--text); font-family: 'Cairo', sans-serif; margin: 0; overflow-x: hidden; }}
        header {{ padding: 20px 5%; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(0,242,255,0.2); background: rgba(0,0,0,0.8); backdrop-filter: blur(10px); position: sticky; top: 0; z-index: 1000; }}
        .logo {{ font-family: 'Orbitron', sans-serif; font-size: 22px; font-weight: 900; color: var(--neon); text-shadow: 0 0 10px var(--neon); text-decoration: none; }}
        .container {{ max-width: 1200px; margin: 30px auto; padding: 0 20px; }}
        .hero {{ text-align: center; margin-bottom: 50px; }}
        .hero h1 {{ font-size: 35px; margin-bottom: 10px; background: linear-gradient(90deg, var(--neon), var(--purple)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
        .trends-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }}
        .t-card {{ background: var(--card); border-radius: 20px; border: 1px solid rgba(255,255,255,0.05); transition: 0.4s; overflow: hidden; }}
        .t-card:hover {{ transform: translateY(-10px); border-color: var(--neon); box-shadow: 0 0 20px rgba(0,242,255,0.2); }}
        .t-card a {{ text-decoration: none; color: inherit; display: block; padding: 25px; }}
        .t-header {{ display: flex; justify-content: space-between; margin-bottom: 20px; }}
        .t-number {{ font-family: 'Orbitron', sans-serif; font-size: 24px; color: rgba(255,255,255,0.1); font-weight: 900; }}
        .t-traffic {{ background: rgba(0,242,255,0.1); color: var(--neon); padding: 4px 12px; border-radius: 50px; font-size: 12px; font-weight: bold; border: 1px solid var(--neon); }}
        .t-body h3 {{ font-size: 18px; margin: 0 0 10px 0; color: #fff; line-height: 1.4; }}
        .t-body p {{ font-size: 13px; color: #888; }}
        .t-footer {{ display: flex; justify-content: space-between; align-items: center; margin-top: 25px; }}
        .t-btn {{ font-size: 12px; color: #fff; background: var(--purple); padding: 5px 15px; border-radius: 8px; box-shadow: 0 0 10px var(--purple); }}
        .ad-box {{ text-align: center; margin: 40px 0; }}
        footer {{ padding: 50px; text-align: center; background: #000; margin-top: 100px; border-top: 1px solid rgba(112,0,255,0.3); }}
    </style>
</head>
<body>
    <header>
        <a href="#" class="logo">VORTEX TRENDS</a>
        <div style="font-size: 12px; color: #555;">آخر تحديث: {update_time}</div>
    </header>

    <div class="container">
        <div class="hero">
            <h1>رادار التريند العالمي</h1>
        </div>

        <div class="ad-box">
             <script type="text/javascript" src="{smart_ad_link}"></script>
        </div>

        <div class="trends-grid">
            {trends_html}
        </div>

        <div class="ad-box">
            <script type="text/javascript" src="{smart_ad_link}"></script>
        </div>
    </div>

    <footer>
        <p style="font-family: 'Orbitron', sans-serif; color: var(--neon);">VORTEX TRENDS © 2026</p>
    </footer>
</body>
</html>'''

        with open("index.html", "w", encoding="utf-8") as f:
            f.write(full_html)
        print("تم التحديث بنجاح باستخدام الرابط الذكي فقط.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_trends_scraper()
