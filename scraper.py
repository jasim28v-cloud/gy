import requests
from bs4 import BeautifulSoup
from datetime import datetime

def run_lumina_ultra_prime():
    rss_url = "https://arabic.rt.com/rss/sport/"
    matches_url = "https://www.yallakora.com/match-center"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    # الرابط الإعلاني الخاص بك
    my_ad_link = "https://data527.click/21330bf1d025d41336e6/57154ac610/?placementName=default"
    
    try:
        # 1. جلب بيانات المباريات
        match_res = requests.get(matches_url, headers=headers, timeout=15)
        match_res.encoding = 'utf-8'
        match_soup = BeautifulSoup(match_res.content, 'lxml')
        matches_html = ""
        for league in match_soup.find_all('div', class_='matchCard')[:4]:
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

        # 2. جلب الأخبار بتنسيق الشبكة الشفافة
        response = requests.get(rss_url, headers=headers, timeout=20)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.content, 'xml')
        items = soup.find_all('item')
        
        news_grid_html = ""
        for i, item in enumerate(items[:15]):
            title = item.title.text
            img = item.find('enclosure').get('url') if item.find('enclosure') else None
            if not img: continue 
            
            news_grid_html += f'''
            <div class="n-card animate-on-scroll">
                <a href="{my_ad_link}" target="_blank">
                    <div class="n-img">
                        <img src="{img}" loading="lazy">
                        <div class="n-badge">ULTRA PRIME</div>
                    </div>
                    <div class="n-info">
                        <h3>{title}</h3>
                        <div class="n-footer">
                            <span>🕒 {datetime.now().strftime('%H:%M')}</span>
                            <span class="n-more">تفاصيل الخبر</span>
                        </div>
                    </div>
                </a>
            </div>'''

        # 3. تصميم واجهة LUMINA PRIME الشفافة والمتحركة
        full_html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LUMINA PRIME | التغطية الشاملة</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&family=Orbitron:wght@600;900&display=swap" rel="stylesheet">
    <style>
        :root {{ 
            --gold: #ffcf4b; 
            --accent: #00f2ff;
            --glass: rgba(255, 255, 255, 0.04);
            --bg: #020406;
        }}
        
        body {{ 
            background: var(--bg); 
            background-attachment: fixed;
            background-image: 
                radial-gradient(circle at 20% 30%, rgba(0, 242, 255, 0.03) 0%, transparent 40%),
                radial-gradient(circle at 80% 70%, rgba(255, 207, 75, 0.03) 0%, transparent 40%);
            color: #fff; font-family: 'Cairo', sans-serif; margin: 0; 
        }}

        header {{ 
            background: rgba(0, 0, 0, 0.6); backdrop-filter: blur(25px); 
            padding: 20px 8%; display: flex; justify-content: space-between; align-items: center;
            border-bottom: 1px solid var(--glass); position: sticky; top: 0; z-index: 1000; 
        }}
        .logo {{ font-family: 'Orbitron', sans-serif; font-size: 26px; font-weight: 900; color: #fff; text-decoration: none; letter-spacing: 2px; }}
        .logo span {{ color: var(--gold); }}

        .container {{ max-width: 1300px; margin: 30px auto; padding: 0 20px; }}

        /* شريط المباريات */
        .match-scroller {{ display: flex; gap: 20px; overflow-x: auto; padding-bottom: 30px; scrollbar-width: none; }}
        .m-card {{ 
            background: var(--glass); min-width: 200px; padding: 25px; border-radius: 25px; 
            border: 1px solid rgba(255,255,255,0.08); text-align: center; backdrop-filter: blur(15px);
            transition: 0.4s; position: relative; overflow: hidden;
        }}
        .m-card:hover {{ border-color: var(--accent); transform: translateY(-8px); background: rgba(0, 242, 255, 0.05); }}
        .m-score {{ color: var(--accent); font-family: 'Orbitron'; font-weight: 900; font-size: 20px; margin: 10px 0; display: block; }}

        /* شبكة الأخبار ايلترا */
        .news-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 30px; }}
        .n-card {{ 
            background: var(--glass); border-radius: 30px; overflow: hidden; 
            border: 1px solid rgba(255,255,255,0.06); transition: 0.5s; backdrop-filter: blur(10px);
        }}
        .n-card:hover {{ border-color: var(--gold); transform: translateY(-10px); box-shadow: 0 20px 40px rgba(0,0,0,0.5); }}
        .n-card a {{ text-decoration: none; color: inherit; }}
        
        .n-img {{ position: relative; height: 220px; overflow: hidden; }}
        .n-img img {{ width: 100%; height: 100%; object-fit: cover; transition: 1.5s ease; }}
        .n-card:hover .n-img img {{ transform: scale(1.1); }}
        .n-badge {{ position: absolute; top: 20px; right: 20px; background: var(--gold); color: #000; font-size: 10px; font-weight: 900; padding: 6px 15px; border-radius: 12px; }}
        
        .n-info {{ padding: 25px; }}
        .n-info h3 {{ font-size: 19px; margin: 0 0 15px 0; line-height: 1.6; height: 60px; overflow: hidden; }}
        .n-footer {{ display: flex; justify-content: space-between; font-size: 13px; color: rgba(255,255,255,0.4); }}
        .n-more {{ color: var(--gold); font-weight: 900; }}

        /* تأثيرات الظهور */
        .animate-on-scroll {{ opacity: 0; transform: translateY(30px); transition: all 0.8s ease-out; }}
        .animate-on-scroll.visible {{ opacity: 1; transform: translateY(0); }}

        footer {{ 
            padding: 80px 20px; text-align: center; border-top: 1px solid var(--glass); 
            background: #000; margin-top: 100px; 
        }}
        
        @media (max-width: 768px) {{
            .news-grid {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <header>
        <a href="{my_ad_link}" class="logo">LUMINA<span>PRIME</span></a>
        <div style="color: var(--accent); font-family: 'Orbitron'; font-size: 12px;">SYSTEM ACTIVE</div>
    </header>

    <div class="container">
        <div class="match-scroller">
            {matches_html}
        </div>

        <div style="text-align: center; margin-bottom: 40px;">
             <a href="{my_ad_link}" target="_blank">
                <img src="https://via.placeholder.com/728x90/111/ffd700?text=ADVERTISING+SPACE+PRIME" style="max-width:100%; border-radius: 15px; border: 1px solid var(--glass);">
             </a>
        </div>

        <h2 style="font-size: 28px; font-weight: 900; margin-bottom: 40px; display: flex; align-items: center; gap: 15px;">
            <span style="width: 10px; height: 10px; background: var(--accent); border-radius: 50%; box-shadow: 0 0 15px var(--accent);"></span>
            أهم الأنباء العالمية
        </h2>
        
        <div class="news-grid">
            {news_grid_html}
        </div>
    </div>

    <footer>
        <div style="font-family: 'Orbitron'; font-size: 24px; font-weight: 900; margin-bottom: 15px;">LUMINA <span style="color:var(--gold)">2026</span></div>
        <p style="opacity: 0.5;">تم تطوير هذا النظام بواسطة تقنيات الذكاء الاصطناعي الفائقة.</p>
    </footer>

    <script>
        // كود بسيط لتشغيل الحركات عند التمرير
        const observerOptions = {{ threshold: 0.1 }};
        const observer = new IntersectionObserver((entries) => {{
            entries.forEach(entry => {{
                if (entry.isIntersecting) {{
                    entry.target.classList.add('visible');
                }}
            }});
        }}, observerOptions);

        document.querySelectorAll('.animate-on-scroll').forEach(el => observer.observe(el));
    </script>
</body>
</html>'''

        with open("index.html", "w", encoding="utf-8") as f: f.write(full_html)
        print("Success: Lumina Ultra Prime is ready with your new ad link!")
    except Exception as e: print(f"Error: {e}")

if __name__ == "__main__":
    run_lumina_ultra_prime()
