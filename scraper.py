import requests
from bs4 import BeautifulSoup
from datetime import datetime

def run_lumina_prime_scraper():
    rss_url = "https://arabic.rt.com/rss/sport/"
    matches_url = "https://www.yallakora.com/match-center"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    try:
        my_link = "https://data527.click/21330bf1d025d41336e6/57154ac610/?placementName=default"
        ad_1 = '<ins style="width: 300px;height:250px" data-width="300" data-height="250" class="g2fb0b4c321" data-domain="//data527.click" data-affquery="/e3435b2a507722939b6f/2fb0b4c321/?placementName=default"><script src="//data527.click/js/responsive.js" async></script></ins>'
        ad_2 = '<script type="text/javascript" src="//data527.click/129ba2282fccd3392338/b1a648bd38/?placementName=default"></script>'

        # 1. جلب المباريات
        match_res = requests.get(matches_url, headers=headers, timeout=15)
        match_soup = BeautifulSoup(match_res.content, 'lxml')
        matches_html = ""
        for m in match_soup.find_all('div', class_='allMatchesList')[:8]:
            t1 = m.find('div', class_='teamA').text.strip()
            t2 = m.find('div', class_='teamB').text.strip()
            res = m.find('div', class_='MResult').find_all('span')
            score = f"{res[0].text} : {res[1].text}" if len(res) > 1 else "00:00"
            matches_html += f'''
            <div class="glass-match">
                <div class="team-name">{t1}</div>
                <div class="match-score">{score}</div>
                <div class="team-name">{t2}</div>
            </div>'''

        # 2. جلب الأخبار
        response = requests.get(rss_url, headers=headers, timeout=20)
        soup = BeautifulSoup(response.content, 'xml')
        news_grid_html = ""
        for i, item in enumerate(soup.find_all('item')[:10]):
            img = item.find('enclosure').get('url') if item.find('enclosure') else ""
            if not img: continue
            
            # إعلان في الشبكة
            if i == 3:
                news_grid_html += f'<div class="ad-box-grid">{ad_1}</div>'

            news_grid_html += f'''
            <div class="prime-card">
                <a href="{my_link}" target="_blank">
                    <div class="card-img" style="background-image: url('{img}')">
                        <div class="card-overlay"></div>
                        <div class="card-tag">عاجل</div>
                    </div>
                    <div class="card-body">
                        <h3>{item.title.text}</h3>
                        <div class="card-meta">
                            <span><i class="far fa-clock"></i> {datetime.now().strftime('%H:%M')}</span>
                            <span class="read-btn">تغطية خاصة</span>
                        </div>
                    </div>
                </a>
            </div>'''

        # 3. واجهة LUMINA PRIME - الإصدار السينمائي
        full_html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LUMINA PRIME | النخبة</title>
    <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@300;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {{ 
            --main-gold: #c5a059; --neon-blue: #00d4ff; --dark-depth: #020406;
            --glass-white: rgba(255, 255, 255, 0.03);
        }}
        
        body {{ 
            background: var(--dark-depth); color: #fff; font-family: 'IBM Plex Sans Arabic', sans-serif; margin: 0; 
            background-image: radial-gradient(circle at 50% -20%, #1a2a3a 0%, #020406 100%);
            min-height: 100vh; overflow-x: hidden;
        }}

        /* Navbar السينمائي */
        nav {{ 
            background: rgba(0,0,0,0.6); backdrop-filter: blur(25px); 
            padding: 20px 10%; border-bottom: 1px solid rgba(255,255,255,0.05);
            display: flex; justify-content: center; position: sticky; top: 0; z-index: 1000;
        }}
        .brand {{ font-size: 28px; font-weight: 700; letter-spacing: 4px; text-transform: uppercase; color: #fff; text-decoration: none; }}
        .brand span {{ color: var(--main-gold); text-shadow: 0 0 20px rgba(197, 160, 89, 0.4); }}

        .hero-container {{ max-width: 1400px; margin: 0 auto; padding: 40px 20px; }}

        /* شريط المباريات المتحرك */
        .match-wrap {{ display: flex; gap: 20px; overflow-x: auto; padding-bottom: 40px; scrollbar-width: none; }}
        .glass-match {{ 
            background: var(--glass-white); min-width: 250px; padding: 25px; border-radius: 30px;
            border: 1px solid rgba(255,255,255,0.07); text-align: center; backdrop-filter: blur(10px);
            transition: 0.4s;
        }}
        .glass-match:hover {{ transform: scale(1.05) translateY(-5px); border-color: var(--neon-blue); }}
        .match-score {{ font-size: 24px; font-weight: 700; color: var(--neon-blue); margin: 10px 0; }}
        .team-name {{ font-weight: 300; font-size: 14px; opacity: 0.8; }}

        /* شبكة الأخبار الاحترافية */
        .news-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 35px; }}
        .prime-card {{ 
            background: var(--glass-white); border-radius: 32px; overflow: hidden; 
            border: 1px solid rgba(255,255,255,0.05); position: relative;
        }}
        .prime-card:hover {{ border-color: var(--main-gold); transform: translateY(-10px); }}
        
        .card-img {{ height: 240px; background-size: cover; background-position: center; position: relative; }}
        .card-overlay {{ position: absolute; inset: 0; background: linear-gradient(to top, var(--dark-depth), transparent); }}
        .card-tag {{ position: absolute; top: 20px; right: 20px; background: var(--main-gold); color: #000; font-weight: 700; font-size: 10px; padding: 5px 15px; border-radius: 50px; }}
        
        .card-body {{ padding: 25px; }}
        .card-body h3 {{ font-size: 18px; line-height: 1.7; margin: 0 0 20px; font-weight: 500; height: 60px; overflow: hidden; }}
        .card-meta {{ display: flex; justify-content: space-between; align-items: center; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 15px; }}
        .read-btn {{ color: var(--main-gold); font-size: 13px; font-weight: 700; border: 1px solid var(--main-gold); padding: 5px 15px; border-radius: 10px; }}

        /* الإعلانات */
        .prime-ad-slot {{ display: flex; justify-content: center; margin: 50px 0; border: 1px dashed rgba(255,255,255,0.1); padding: 20px; border-radius: 20px; }}
        .ad-box-grid {{ grid-column: 1 / -1; display: flex; justify-content: center; padding: 20px; }}

        footer {{ text-align: center; padding: 100px 20px; background: rgba(0,0,0,0.4); margin-top: 100px; }}
        
        @media (max-width: 768px) {{ .news-grid {{ grid-template-columns: 1fr; }} }}
    </style>
</head>
<body>
    <nav>
        <a href="#" class="brand">LUMINA<span>PRIME</span></a>
    </nav>

    <div class="hero-container">
        <div class="match-wrap">{matches_html}</div>

        <div class="prime-ad-slot">{ad_1}</div>

        <h2 style="font-size: 32px; font-weight: 700; margin-bottom: 40px; display: flex; align-items: center; gap: 20px;">
            <span style="width: 50px; height: 2px; background: var(--main-gold);"></span> تـحقيقات حـصرية
        </h2>

        <div class="news-grid">
            {news_grid_html}
        </div>

        <div class="prime-ad-slot" style="border:none;">{ad_2}</div>
    </div>

    <footer>
        <div class="brand">LUMINA<span>PRIME</span></div>
        <p style="opacity: 0.4; margin-top: 20px;">النظام الأكثر تطوراً في رصد وتحليل البيانات الرياضية 2026</p>
    </footer>
</body>
</html>'''

        with open("index.html", "w", encoding="utf-8") as f: f.write(full_html)
        print("Done: The Cinematic Version is ready!")
    except Exception as e: print(f"Error: {e}")

if __name__ == "__main__":
    run_lumina_prime_scraper()
