import requests
from bs4 import BeautifulSoup
from datetime import datetime

def run_neon_rt_exclusive():
    # مصدر RT Arabic الحصري
    rt_url = "https://arabic.rt.com/rss/news/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        # إعلاناتك المعتمدة
        smart_ad_url = "https://data527.click/21330bf1d025d41336e6/57154ac610/?placementName=default"
        responsive_ad = '<ins style="width: 300px;height:250px" data-width="300" data-height="250" class="g2fb0b4c321" data-domain="//data527.click" data-affquery="/e3435b2a507722939b6f/2fb0b4c321/?placementName=default"><script src="//data527.click/js/responsive.js" async></script></ins>'
        script_ad = '<script type="text/javascript" src="//data527.click/129ba2282fccd3392338/b1a648bd38/?placementName=default"></script>'

        response = requests.get(rt_url, headers=headers, timeout=30)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.content, 'xml')
        items = soup.find_all('item')
        
        content_html = ""
        for i, item in enumerate(items[:15]): # جلب 15 خبر
            title = item.title.text
            # استخراج صورة RT الأصلية
            img_tag = item.find('enclosure')
            real_img = img_tag.get('url') if img_tag else "https://arabic.rt.com/static/img/logo.png"
            
            # معالج الصور لضمان الظهور
            proxied_img = f"https://images.weserv.nl/?url={real_img}&w=600&h=350&fit=cover"

            content_html += f'''
            <div class="glass-card">
                <a href="{smart_ad_url}" target="_blank">
                    <div class="img-box">
                        <img src="{proxied_img}" alt="RT NEWS" loading="lazy">
                        <div class="rt-label">RT EXCLUSIVE</div>
                    </div>
                    <div class="info-box">
                        <h3>{title}</h3>
                        <div class="card-footer">
                            <span class="date">🕒 {datetime.now().strftime('%H:%M')}</span>
                            <span class="neon-btn">قراءة المزيد</span>
                        </div>
                    </div>
                </a>
            </div>'''
            
            # إعلانات بينية كل 5 أخبار
            if (i + 1) % 5 == 0:
                content_html += f'<div class="mid-ad">{responsive_ad}</div>'

        update_time = datetime.now().strftime('%H:%M')
        full_html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NEON RT | الأخبار الحصرية</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        :root {{ --neon: #00f2ff; --bg: #020205; --card: rgba(255,255,255,0.03); --border: rgba(255,255,255,0.08); }}
        body {{ background: var(--bg); color: #fff; font-family: 'Cairo', sans-serif; margin: 0; }}
        header {{ background: rgba(0,0,0,0.9); padding: 15px 5%; border-bottom: 2px solid var(--neon); display: flex; justify-content: space-between; align-items: center; position: sticky; top: 0; z-index: 1000; backdrop-filter: blur(15px); }}
        .logo {{ font-size: 24px; font-weight: 900; color: var(--neon); text-decoration: none; text-shadow: 0 0 10px var(--neon); }}
        .container {{ max-width: 1200px; margin: 25px auto; padding: 0 15px; }}
        
        .top-ad-zone {{ text-align: center; margin-bottom: 30px; padding: 15px; background: var(--card); border: 1px solid var(--border); border-radius: 15px; min-height: 100px; }}
        .mid-ad {{ grid-column: 1 / -1; display: flex; justify-content: center; padding: 20px; }}

        .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 25px; }}
        .glass-card {{ background: var(--card); border: 1px solid var(--border); border-radius: 20px; overflow: hidden; transition: 0.4s; backdrop-filter: blur(10px); }}
        .glass-card:hover {{ border-color: var(--neon); transform: translateY(-8px); background: rgba(255,255,255,0.06); }}
        .glass-card a {{ text-decoration: none; color: inherit; }}
        
        .img-box {{ height: 210px; position: relative; overflow: hidden; }}
        .img-box img {{ width: 100%; height: 100%; object-fit: cover; opacity: 0.9; }}
        .rt-label {{ position: absolute; top: 12px; right: 12px; background: #ff004c; font-size: 10px; padding: 3px 10px; font-weight: 900; border-radius: 5px; }}

        .info-box {{ padding: 20px; }}
        h3 {{ font-size: 16px; margin: 0; line-height: 1.6; height: 52px; overflow: hidden; }}
        .card-footer {{ display: flex; justify-content: space-between; align-items: center; margin-top: 20px; }}
        .date {{ color: #555; font-size: 11px; }}
        .neon-btn {{ color: var(--neon); font-size: 12px; font-weight: bold; border: 1px solid var(--neon); padding: 4px 12px; border-radius: 6px; }}

        footer {{ text-align: center; padding: 50px; color: #333; font-size: 11px; }}
    </style>
</head>
<body>
    <header>
        <a href="#" class="logo">NEON<span>RT</span></a>
        <div style="font-size: 11px;">تحديث مباشر: {update_time}</div>
    </header>

    <div class="container">
        <div class="top-ad-zone">{script_ad}</div>
        <div class="grid">{content_html}</div>
        <div class="top-ad-zone" style="margin-top: 30px;">{responsive_ad}</div>
    </div>
    <footer>NEON RT EXCLUSIVE © 2026</footer>
</body>
</html>'''

        with open("index.html", "w", encoding="utf-8") as f:
            f.write(full_html)
        print("Success: Exclusive RT Content Deployed.")
    except Exception as e: print(f"Error: {e}")

if __name__ == "__main__":
    run_neon_rt_exclusive()
