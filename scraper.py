import requests
from bs4 import BeautifulSoup
from datetime import datetime

def run_vortex_ultra_prime():
    # مصدر أخبار RT العربية الرئيسي
    rt_url = "https://arabic.rt.com/rss/news/"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    try:
        # إعلاناتك الذكية المعتمدة
        smart_ad_url = "https://data527.click/21330bf1d025d41336e6/57154ac610/?placementName=default"
        responsive_ad = '<ins style="width: 300px;height:250px" data-width="300" data-height="250" class="g2fb0b4c321" data-domain="//data527.click" data-affquery="/e3435b2a507722939b6f/2fb0b4c321/?placementName=default"><script src="//data527.click/js/responsive.js" async></script></ins>'
        script_ad = '<script type="text/javascript" src="//data527.click/129ba2282fccd3392338/b1a648bd38/?placementName=default"></script>'

        response = requests.get(rt_url, headers=headers, timeout=20)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.content, 'xml')
        items = soup.find_all('item')
        
        content_html = ""
        for i, item in enumerate(items[:12]):
            title = item.title.text
            img_tag = item.find('enclosure')
            img_url = img_tag.get('url') if img_tag else "https://arabic.rt.com/static/img/logo.png"
            
            content_html += f'''
            <div class="glass-card">
                <a href="{smart_ad_url}" target="_blank">
                    <div class="card-img">
                        <img src="{img_url}" loading="lazy" onerror="this.src='https://picsum.photos/400/220'">
                    </div>
                    <div class="card-body">
                        <span class="live-tag">ULTRA LIVE</span>
                        <h3>{title}</h3>
                        <div class="card-footer">
                            <span>RT SOURCE</span>
                            <span class="prime-btn">دخول</span>
                        </div>
                    </div>
                </a>
            </div>'''
            
            # إعلانات بينية شفافة
            if (i + 1) % 4 == 0:
                content_html += f'<div class="ad-break">{responsive_ad}</div>'

        update_time = datetime.now().strftime('%H:%M')
        full_html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NEON RT | ULTRA PRIME</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        :root {{ --neon-blue: #00f2ff; --glass: rgba(255, 255, 255, 0.05); --border: rgba(255, 255, 255, 0.1); }}
        body {{ 
            background: radial-gradient(circle at center, #1a1a2e 0%, #0a0a0c 100%); 
            color: #fff; font-family: 'Cairo', sans-serif; margin: 0; min-height: 100vh;
        }}
        
        /* تأثير الخلفية الشفافة المتحركة */
        body::before {{
            content: ""; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: url('https://www.transparenttextures.com/patterns/carbon-fibre.png');
            opacity: 0.2; z-index: -1;
        }}

        header {{ 
            background: rgba(0, 0, 0, 0.5); backdrop-filter: blur(15px); padding: 20px 5%;
            border-bottom: 1px solid var(--border); position: sticky; top: 0; z-index: 1000;
            display: flex; justify-content: space-between; align-items: center;
        }}
        .logo {{ font-weight: 900; font-size: 26px; color: var(--neon-blue); text-shadow: 0 0 15px var(--neon-blue); text-decoration: none; }}
        
        .container {{ max-width: 1200px; margin: 20px auto; padding: 0 15px; }}

        /* الإعلانات الشفافة */
        .prime-ad {{ background: var(--glass); border: 1px solid var(--border); border-radius: 20px; padding: 20px; text-align: center; margin-bottom: 30px; backdrop-filter: blur(10px); }}

        .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 25px; }}
        
        /* كارت البرايم الشفاف */
        .glass-card {{ 
            background: var(--glass); backdrop-filter: blur(12px); border: 1px solid var(--border);
            border-radius: 24px; overflow: hidden; transition: 0.5s cubic-bezier(0.2, 0.8, 0.2, 1);
        }}
        .glass-card:hover {{ 
            transform: scale(1.03) translateY(-10px); background: rgba(255,255,255,0.08); 
            border-color: var(--neon-blue); box-shadow: 0 20px 40px rgba(0,0,0,0.4);
        }}
        .glass-card a {{ text-decoration: none; color: inherit; }}
        
        .card-img {{ height: 200px; overflow: hidden; }}
        .card-img img {{ width: 100%; height: 100%; object-fit: cover; transition: 0.5s; }}
        .glass-card:hover .card-img img {{ transform: scale(1.1); }}

        .card-body {{ padding: 20px; }}
        .live-tag {{ font-size: 10px; background: var(--neon-blue); color: #000; padding: 2px 10px; border-radius: 50px; font-weight: 900; }}
        h3 {{ margin: 15px 0; font-size: 17px; line-height: 1.5; color: #fff; height: 50px; overflow: hidden; }}
        
        .card-footer {{ display: flex; justify-content: space-between; align-items: center; margin-top: 20px; font-size: 12px; color: #777; }}
        .prime-btn {{ color: var(--neon-blue); border: 1px solid var(--neon-blue); padding: 4px 15px; border-radius: 8px; font-weight: bold; }}

        footer {{ text-align: center; padding: 60px; color: #444; font-size: 12px; }}
    </style>
</head>
<body>
    <header>
        <a href="#" class="logo">NEON<span>RT</span></a>
        <div style="font-size: 11px;">ULTRA PRIME v.1.0</div>
    </header>

    <div class="container">
        <div class="prime-ad">
            {script_ad}
        </div>

        <div class="grid">{content_html}</div>

        <div class="prime-ad" style="margin-top: 40px;">
            {responsive_ad}
        </div>
    </div>

    <footer>NEON RT DIGITAL EXPERIENCE © 2026</footer>
</body>
</html>'''

        with open("index.html", "w", encoding="utf-8") as f:
            f.write(full_html)
        print("Done! Ultra Prime Transparent Edition is Live.")
    except Exception as e: print(f"Error: {e}")

if __name__ == "__main__":
    run_vortex_ultra_prime()
