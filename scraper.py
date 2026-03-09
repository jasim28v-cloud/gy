import requests
from bs4 import BeautifulSoup
from datetime import datetime

def run_lumina_prime_scraper():
    rss_url = "https://arabic.rt.com/rss/sport/"
    matches_url = "https://www.yallakora.com/match-center"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    try:
        # رابط توجيه الأخبار
        my_link = "https://data527.click/21330bf1d025d41336e6/57154ac610/?placementName=default"
        
        # الأكواد الإعلانية المطلوبة
        ad_unit_1 = '<ins style="width: 300px;height:250px" data-width="300" data-height="250" class="g2fb0b4c321" data-domain="//data527.click" data-affquery="/e3435b2a507722939b6f/2fb0b4c321/?placementName=default"><script src="//data527.click/js/responsive.js" async></script></ins>'
        ad_unit_2 = '<script type="text/javascript" src="//data527.click/129ba2282fccd3392338/b1a648bd38/?placementName=default"></script>'

        # 1. جلب المباريات
        match_res = requests.get(matches_url, headers=headers, timeout=15)
        match_res.encoding = 'utf-8'
        match_soup = BeautifulSoup(match_res.content, 'lxml')
        matches_html = ""
        for league in match_soup.find_all('div', class_='matchCard')[:6]:
            for m in league.find_all('div', class_='allMatchesList')[:1]:
                t1 = m.find('div', class_='teamA').text.strip()
                t2 = m.find('div', class_='teamB').text.strip()
                res = m.find('div', class_='MResult').find_all('span')
                score = f"{res[0].text}-{res[1].text}" if len(res) > 1 else "LIVE"
                matches_html += f'''
                <div class="m-card">
                    <div class="m-team">{t1}</div>
                    <div class="m-score">{score}</div>
                    <div class="m-team">{t2}</div>
                </div>'''

        # 2. جلب الأخبار
        response = requests.get(rss_url, headers=headers, timeout=20)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.content, 'xml')
        items = soup.find_all('item')
        
        news_grid_html = ""
        for i, item in enumerate(items[:12]):
            title = item.title.text
            img = item.find('enclosure').get('url') if item.find('enclosure') else None
            if not img: continue 
            
            # إدراج إعلان وسط الأخبار عند الخبر رقم 4
            if i == 4:
                news_grid_html += f'<div class="ad-in-grid">{ad_unit_1}</div>'

            news_grid_html += f'''
            <div class="n-card">
                <a href="{my_link}" target="_blank">
                    <div class="n-img">
                        <img src="{img}" loading="lazy">
                        <div class="n-badge">ULTRA</div>
                    </div>
                    <div class="n-info">
                        <h3>{title}</h3>
                        <div class="n-footer">
                            <span><i class="far fa-clock"></i> {datetime.now().strftime('%H:%M')}</span>
                            <span class="n-more">إقرأ المزيد</span>
                        </div>
                    </div>
                </a>
            </div>'''

        # 3. بناء الواجهة
        full_html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LUMINA PRIME | 2026</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&family=Orbitron:wght@500;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        :root {{ --gold: #ffcf4b; --accent: #00f2ff; --bg: #030508; --card: rgba(255,255,255,0.05); }}
        body {{ background: var(--bg); color: #fff; font-family: 'Cairo', sans-serif; margin: 0; }}
        
        header {{ 
            background: rgba(0,0,0,0.8); backdrop-filter: blur(15px); 
            padding: 15px 8%; border-bottom: 1px solid rgba(255,255,255,0.1);
            display: flex; justify-content: space-between; align-items: center;
            position: sticky; top: 0; z-index: 1000;
        }}
        .logo {{ font-family: 'Orbitron'; font-size: 22px; font-weight: 900; color: #fff; text-decoration: none; }}
        .logo span {{ color: var(--gold); }}

        .container {{ max-width: 1250px; margin: 20px auto; padding: 0 15px; }}

        /* شريط المباريات */
        .match-scroller {{ display: flex; gap: 15px; overflow-x: auto; padding: 10px 0 25px; scrollbar-width: none; }}
        .m-card {{ 
            background: var(--card); min-width: 200px; padding: 15px; 
            border-radius: 15px; border: 1px solid rgba(255,255,255,0.1); text-align: center;
        }}
        .m-score {{ color: var(--accent); font-family: 'Orbitron'; font-weight: 900; }}

        /* شبكة الأخبار */
        .news-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 25px; }}
        .n-card {{ background: var(--card); border-radius: 20px; overflow: hidden; border: 1px solid rgba(255,255,255,0.1); }}
        .n-img {{ height: 180px; position: relative; }}
        .n-img img {{ width: 100%; height: 100%; object-fit: cover; }}
        .n-info {{ padding: 20px; }}
        .n-info h3 {{ font-size: 16px; margin: 0 0 15px; line-height: 1.6; height: 50px; overflow: hidden; }}
        .n-footer {{ display: flex; justify-content: space-between; font-size: 12px; opacity: 0.6; }}
        .n-more {{ color: var(--gold); font-weight: bold; }}

        /* تنسيق الإعلانات */
        .ad-container {{ display: flex; justify-content: center; align-items: center; margin: 30px 0; min-height: 250px; background: rgba(255,255,255,0.02); border-radius: 15px; }}
        .ad-in-grid {{ grid-column: 1 / -1; display: flex; justify-content: center; padding: 20px 0; }}

        @media (max-width: 768px) {{ .news-grid {{ grid-template-columns: 1fr; }} }}
    </style>
</head>
<body>
    <header>
        <a href="#" class="logo">LUMINA<span>PRIME</span></a>
        <div style="color: var(--accent); font-size: 12px;"><i class="fas fa-signal"></i> LIVE STREAM</div>
    </header>

    <div class="container">
        <div class="match-scroller">{matches_html}</div>

        <div class="ad-container">
            {ad_unit_1}
        </div>

        <h2 style="border-right: 4px solid var(--gold); padding-right: 15px; margin: 40px 0 25px;">الأخبار العاجلة</h2>
        
        <div class="news-grid">
            {news_grid_html}
        </div>

        <div class="ad-container">
            {ad_unit_2}
        </div>
    </div>

    <footer style="text-align: center; padding: 60px 20px; border-top: 1px solid rgba(255,255,255,0.1); margin-top: 50px;">
        <div class="logo">LUMINA<span>PRIME</span></div>
        <p style="opacity: 0.5;">حقوق النشر 2026 - تم التطوير لتقديم أفضل تجربة رياضية</p>
    </footer>
</body>
</html>'''

        with open("index.html", "w", encoding="utf-8") as f: f.write(full_html)
        print("✅ تم دمج الإعلانات بنجاح في ملف index.html")
    except Exception as e: print(f"❌ خطأ: {e}")

if __name__ == "__main__":
    run_lumina_prime_scraper()
