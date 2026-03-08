import requests
from bs4 import BeautifulSoup
from datetime import datetime

def run_vortex_vogue():
    # مصادر الموضة والجمال العالمية
    fashion_url = "https://www.vogue.com/feed/rss"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    try:
        # استخدام رابطك الإعلاني الذكي المحفوظ
        smart_ad_url = "https://data527.click/21330bf1d025d41336e6/57154ac610/?placementName=default"
        
        response = requests.get(fashion_url, headers=headers, timeout=20)
        soup = BeautifulSoup(response.content, 'xml')
        items = soup.find_all('item')
        
        content_html = ""
        for i, item in enumerate(items[:16]):
            title = item.title.text
            # جلب وصف مختصر وصورة
            desc = item.description.text if item.description else "اكتشفي أحدث صيحات الموضة العالمية لهذا الموسم."
            img_tag = item.find('media:content') or item.find('enclosure')
            img_url = img_tag.get('url') if img_tag else f"https://picsum.photos/seed/{i}/500/300"
            
            content_html += f'''
            <div class="f-card">
                <a href="{smart_ad_url}" target="_blank">
                    <div class="f-img">
                        <img src="{img_url}" loading="lazy">
                        <div class="f-overlay"></div>
                    </div>
                    <div class="f-info">
                        <span class="f-tag">TRENDING</span>
                        <h3>{title}</h3>
                        <p>{desc[:80]}...</p>
                        <div class="f-footer">
                            <span>STYLE GUIDE 2026</span>
                            <span class="f-more">التفاصيل ←</span>
                        </div>
                    </div>
                </a>
            </div>'''

        # واجهة الموضة الراقية (Luxury Black & Gold)
        update_time = datetime.now().strftime('%H:%M')
        full_html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VORTEX VOGUE | عالم الأناقة</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&family=Playfair+Display:ital,wght@1,700&display=swap" rel="stylesheet">
    <style>
        :root {{ --gold: #c5a059; --bg: #0a0a0a; --card: #141414; --text: #ffffff; }}
        body {{ background: var(--bg); color: var(--text); font-family: 'Cairo', sans-serif; margin: 0; }}
        
        header {{ background: #000; padding: 25px 5%; text-align: center; border-bottom: 1px solid #222; position: sticky; top: 0; z-index: 1000; }}
        .logo {{ font-family: 'Playfair Display', serif; font-size: 32px; color: var(--gold); text-decoration: none; letter-spacing: 3px; }}
        
        .container {{ max-width: 1200px; margin: 30px auto; padding: 0 15px; }}
        
        /* مساحة الإعلان الذكي */
        .ad-zone {{ width: 100%; height: 250px; background: #000; margin-bottom: 40px; border: 1px solid #1a1a1a; overflow: hidden; }}
        .ad-zone iframe {{ width: 100%; height: 100%; border: none; }}

        .f-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 30px; }}
        .f-card {{ background: var(--card); border-radius: 0px; overflow: hidden; transition: 0.5s; border: 1px solid #1a1a1a; }}
        .f-card:hover {{ transform: translateY(-10px); border-color: var(--gold); }}
        .f-card a {{ text-decoration: none; color: inherit; }}
        
        .f-img {{ position: relative; height: 250px; overflow: hidden; }}
        .f-img img {{ width: 100%; height: 100%; object-fit: cover; transition: 0.8s; }}
        .f-card:hover .f-img img {{ transform: scale(1.1); }}
        .f-overlay {{ position: absolute; inset: 0; background: linear-gradient(to top, rgba(0,0,0,0.7), transparent); }}
        
        .f-info {{ padding: 20px; }}
        .f-tag {{ color: var(--gold); font-size: 10px; font-weight: 900; letter-spacing: 2px; }}
        h3 {{ font-family: 'Playfair Display', serif; font-size: 19px; margin: 10px 0; line-height: 1.4; color: #fff; height: 54px; overflow: hidden; }}
        p {{ color: #888; font-size: 13px; line-height: 1.6; }}
        
        .f-footer {{ display: flex; justify-content: space-between; margin-top: 20px; font-size: 11px; color: #444; border-top: 1px solid #222; padding-top: 15px; }}
        .f-more {{ color: var(--gold); font-weight: bold; }}

        footer {{ background: #000; padding: 60px; text-align: center; border-top: 1px solid #1a1a1a; margin-top: 50px; }}
    </style>
</head>
<body>
    <header>
        <a href="#" class="logo">VORTEX VOGUE</a>
        <div style="font-size: 10px; color: #444; margin-top: 5px;">LAST UPDATE: {update_time}</div>
    </header>

    <div class="container">
        <div class="ad-zone">
            <iframe src="{smart_ad_url}"></iframe>
        </div>

        <div class="f-grid">{content_html}</div>

        <div class="ad-zone" style="margin-top: 40px;">
            <iframe src="{smart_ad_url}"></iframe>
        </div>
    </div>

    <footer>
        <div style="font-family: 'Playfair Display', serif; color: var(--gold); font-size: 24px;">VV</div>
        <p style="color: #333; font-size: 11px;">© 2026 VORTEX VOGUE DIGITAL FASHION EXPERIENCE</p>
    </footer>
</body>
</html>'''

        with open("index.html", "w", encoding="utf-8") as f:
            f.write(full_html)
        print("Fashion Site Updated!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_vortex_vogue()
