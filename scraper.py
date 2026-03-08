import requests
from bs4 import BeautifulSoup
from datetime import datetime

def run_lumina_ultra_prime_v2():
    rss_url = "https://arabic.rt.com/rss/sport/"
    matches_url = "https://www.yallakora.com/match-center"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    # رابط الإعلان الخاص بك
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

        # 2. جلب الأخبار
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
                            <span class="n-more">المزيد</span>
                        </div>
                    </div>
                </a>
            </div>'''

        # 3. واجهة LUMINA PRIME V2 مع المنبثق الذكي
        full_html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LUMINA PRIME | Ultra Edition</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&family=Orbitron:wght@600;900&display=swap" rel="stylesheet">
    <style>
        :root {{ 
            --gold: #ffcf4b; 
            --accent: #00f2ff;
            --glass: rgba(255, 255, 255, 0.05);
            --bg: #020406;
        }}
        
        body {{ 
            background: var(--bg); color: #fff; font-family: 'Cairo', sans-serif; margin: 0; 
            overflow-x: hidden;
        }}

        header {{ 
            background: rgba(0, 0, 0, 0.7); backdrop-filter: blur(30px); 
            padding: 20px 8%; display: flex; justify-content: space-between; align-items: center;
            border-bottom: 1px solid var(--glass); position: sticky; top: 0; z-index: 1000; 
        }}
        .logo {{ font-family: 'Orbitron', sans-serif; font-size: 26px; font-weight: 900; color: #fff; text-decoration: none; }}
        .logo span {{ color: var(--gold); }}

        .container {{ max-width: 1300px; margin: 30px auto; padding: 0 20px; }}

        /* شريط المباريات */
        .match-scroller {{ display: flex; gap: 20px; overflow-x: auto; padding-bottom: 30px; scrollbar-width: none; }}
        .m-card {{ 
            background: var(--glass); min-width: 200px; padding: 25px; border-radius: 25px; 
            border: 1px solid rgba(255,255,255,0.1); text-align: center; backdrop-filter: blur(15px);
            transition: 0.4s;
        }}
        .m-score {{ color: var(--accent); font-family: 'Orbitron'; font-weight: 900; font-size: 22px; margin: 10px 0; display: block; }}

        /* شبكة الأخبار */
        .news-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 30px; }}
        .n-card {{ 
            background: var(--glass); border-radius: 30px; overflow: hidden; 
            border: 1px solid rgba(255,255,255,0.06); transition: 0.6s cubic-bezier(0.165, 0.84, 0.44, 1);
            backdrop-filter: blur(10px);
        }}
        .n-card:hover {{ border-color: var(--gold); transform: translateY(-10px); }}
        .n-img {{ position: relative; height: 220px; overflow: hidden; }}
        .n-img img {{ width: 100%; height: 100%; object-fit: cover; }}
        .n-badge {{ position: absolute; top: 20px; right: 20px; background: var(--gold); color: #000; font-size: 10px; font-weight: 900; padding: 6px 15px; border-radius: 12px; }}
        .n-info {{ padding: 25px; }}
        .n-info h3 {{ font-size: 19px; margin: 0 0 15px 0; line-height: 1.6; height: 60px; overflow: hidden; }}
        .n-more {{ color: var(--gold); font-weight: 900; }}

        /* تصميم النافذة المنبثقة (Popup) */
        .popup-overlay {{
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.85); backdrop-filter: blur(10px);
            display: flex; justify-content: center; align-items: center;
            z-index: 9999; opacity: 0; visibility: hidden; transition: 0.5s;
        }}
        .popup-content {{
            background: linear-gradient(135deg, #111, #000);
            width: 90%; max-width: 450px; padding: 40px; border-radius: 35px;
            text-align: center; border: 1px solid var(--gold);
            transform: scale(0.8); transition: 0.5s;
        }}
        .popup-overlay.active {{ opacity: 1; visibility: visible; }}
        .popup-overlay.active .popup-content {{ transform: scale(1); }}
        
        .popup-title {{ font-family: 'Orbitron'; font-size: 24px; color: var(--gold); margin-bottom: 15px; }}
        .popup-btn {{
            display: inline-block; padding: 15px 40px; background: var(--gold); color: #000;
            text-decoration: none; border-radius: 50px; font-weight: 900; margin-top: 25px;
            box-shadow: 0 10px 20px rgba(255, 207, 75, 0.3); transition: 0.3s;
        }}
        .popup-btn:hover {{ transform: scale(1.05); box-shadow: 0 15px 30px rgba(255, 207, 75, 0.5); }}
        .close-popup {{ color: #555; cursor: pointer; margin-top: 15px; display: block; font-size: 12px; text-decoration: underline; }}

        /* حركات التمرير */
        .animate-on-scroll {{ opacity: 0; transform: translateY(30px); transition: 0.8s; }}
        .animate-on-scroll.visible {{ opacity: 1; transform: translateY(0); }}

        footer {{ padding: 60px 20px; text-align: center; background: #000; border-top: 1px solid var(--glass); margin-top: 100px; }}
    </style>
</head>
<body>

    <div class="popup-overlay" id="adPopup">
        <div class="popup-content">
            <div class="popup-title">LUMINA PRIME <span>V2</span></div>
            <p style="opacity: 0.8; line-height: 1.8;">استمتع بأحدث التغطيات الرياضية الحصرية والأخبار العاجلة عبر منصتنا المطورة.</p>
            <a href="{my_ad_link}" target="_blank" class="popup-btn" onclick="closePopup()">دخول المنصة الآن</a>
            <span class="close-popup" onclick="closePopup()">إغلاق ومتابعة القراءة</span>
        </div>
    </div>

    <header>
        <a href="{my_ad_link}" class="logo">LUMINA<span>PRIME</span></a>
        <div style="color: var(--accent); font-family: 'Orbitron'; font-size: 11px; border: 1px solid var(--accent); padding: 4px 12px; border-radius: 5px;">ULTRA V2</div>
    </header>

    <div class="container">
        <div class="match-scroller">
            {matches_html}
        </div>

        <h2 style="font-size: 28px; font-weight: 900; margin-bottom: 40px; border-right: 6px solid var(--gold); padding-right: 15px;">آخر التحديثات</h2>
        
        <div class="news-grid">
            {news_grid_html}
        </div>
    </div>

    <footer>
        <div style="font-family: 'Orbitron'; font-size: 22px; font-weight: 900;">LUMINA <span>2026</span></div>
    </footer>

    <script>
        // إظهار النافذة المنبثقة بعد ثانيتين من الدخول
        window.onload = function() {{
            setTimeout(() => {{
                document.getElementById('adPopup').classList.add('active');
            }}, 2000);
        }};

        function closePopup() {{
            document.getElementById('adPopup').classList.remove('active');
        }}

        // حركات التمرير
        const observer = new IntersectionObserver((entries) => {{
            entries.forEach(entry => {{
                if (entry.isIntersecting) entry.target.classList.add('visible');
            }});
        }}, {{ threshold: 0.1 }});

        document.querySelectorAll('.animate-on-scroll').forEach(el => observer.observe(el));
    </script>
</body>
</html>'''

        with open("index.html", "w", encoding="utf-8") as f: f.write(full_html)
        print("Success: Lumina Prime V2 with Popup and New Ad Link is ready!")
    except Exception as e: print(f"Error: {e}")

if __name__ == "__main__":
    run_lumina_ultra_prime_v2()
