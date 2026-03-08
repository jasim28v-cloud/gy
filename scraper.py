import requests
from bs4 import BeautifulSoup
from datetime import datetime

def run_neon_rt_real_images():
    # الرابط المباشر لأخبار RT (الأكثر استقراراً للصور)
    rt_url = "https://arabic.rt.com/rss/news/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
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
        for i, item in enumerate(items[:12]):
            title = item.title.text
            # سحب رابط الصورة الحقيقي من وسم enclosure
            img_tag = item.find('enclosure')
            real_img = img_tag.get('url') if img_tag else ""
            
            # إذا لم تتوفر صورة حقيقية، نستخدم محرك بحث ذكي للصور المتعلقة بالعنوان
            if not real_img:
                real_img = f"https://source.unsplash.com/featured/?news,{i}"

            content_html += f'''
            <div class="prime-card">
                <a href="{smart_ad_url}" target="_blank">
                    <div class="img-box">
                        <img src="{real_img}" alt="RT News Image" onerror="this.src='https://arabic.rt.com/static/img/logo.png'">
                        <div class="status-tag">RT EXCLUSIVE</div>
                    </div>
                    <div class="text-box">
                        <h3>{title}</h3>
                        <div class="footer-box">
                            <span class="time-stamp">🕒 {datetime.now().strftime('%H:%M')}</span>
                            <span class="prime-btn">عرض التفاصيل</span>
                        </div>
                    </div>
                </a>
            </div>'''
            
            if (i + 1) % 3 == 0:
                content_html += f'<div class="ad-row">{responsive_ad}</div>'

        full_html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NEON RT | ULTRA PRIME</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        :root {{ --neon: #00f2ff; --dark: #050505; --glass: rgba(255, 255, 255, 0.03); }}
        body {{ background: var(--dark); color: #fff; font-family: 'Cairo', sans-serif; margin: 0; padding-bottom: 50px; }}
        header {{ 
            background: rgba(0,0,0,0.9); padding: 15px 5%; border-bottom: 1px solid var(--neon);
            display: flex; justify-content: space-between; align-items: center; position: sticky; top: 0; z-index: 1000; backdrop-filter: blur(10px);
        }}
        .logo {{ font-size: 24px; font-weight: 900; color: var(--neon); text-decoration: none; text-shadow: 0 0 10px var(--neon); }}
        .container {{ max-width: 1100px; margin: 20px auto; padding: 0 15px; }}
        
        .top-ad {{ background: var(--glass); border: 1px solid rgba(255,255,255,0.1); border-radius: 15px; margin-bottom: 30px; padding: 20px; text-align: center; }}
        .ad-row {{ grid-column: 1 / -1; display: flex; justify-content: center; margin: 20px 0; }}

        .news-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 25px; }}
        .prime-card {{ background: #111; border: 1px solid #222; border-radius: 20px; overflow: hidden; transition: 0.4s; }}
        .prime-card:hover {{ border-color: var(--neon); transform: translateY(-5px); box-shadow: 0 10px 30px rgba(0,242,255,0.1); }}
        .prime-card a {{ text-decoration: none; color: inherit; }}
        
        .img-box {{ height: 220px; position: relative; overflow: hidden; }}
        .img-box img {{ width: 100%; height: 100%; object-fit: cover; transition: 0.6s; }}
        .prime-card:hover .img-box img {{ transform: scale(1.1); }}
        .status-tag {{ position: absolute; top: 15px; right: 15px; background: #ff004c; color: #fff; font-size: 10px; padding: 3px 10px; font-weight: 900; border-radius: 5px; }}

        .text-box {{ padding: 20px; }}
        h3 {{ font-size: 16px; margin: 0; line-height: 1.6; height: 50px; overflow: hidden; color: #eee; }}
        .footer-box {{ display: flex; justify-content: space-between; align-items: center; margin-top: 20px; border-top: 1px solid #222; padding-top: 15px; }}
        .time-stamp {{ font-size: 11px; color: #555; }}
        .prime-btn {{ color: var(--neon); font-size: 12px; font-weight: bold; }}
        
        footer {{ text-align: center; padding: 40px; color: #333; font-size: 11px; }}
    </style>
</head>
<body>
    <header>
        <a href="#" class="logo">NEON<span>RT</span></a>
        <div style="font-size: 11px; color: var(--neon);">ULTRA PRIME EDITION</div>
    </header>

    <div class="container">
        <div class="top-ad">{script_ad}</div>
        <div class="news-grid">{content_html}</div>
        <div class="top-ad" style="margin-top: 30px;">{responsive_ad}</div>
    </div>

    <footer>VORTEX NEON RT SYSTEM © 2026</footer>
</body>
</html>'''

        with open("index.html", "w", encoding="utf-8") as f:
            f.write(full_html)
        print("Success: Real Images Integrated.")
    except Exception as e: print(f"Error: {e}")

if __name__ == "__main__":
    run_neon_rt_real_images()
