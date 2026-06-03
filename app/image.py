from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

def generate_image(data):
    WIDTH, HEIGHT = 520, 360
    BG_COLOR = (10, 10, 20)
    CYAN = (0, 245, 255)
    WHITE = (255, 255, 255)
    GRAY = (160, 233, 255)
    ACCENT = (0, 180, 216)

    img = Image.new('RGB', (WIDTH, HEIGHT), color=BG_COLOR)
    draw = ImageDraw.Draw(img)

    # Try to load a font that supports emojis
    try:
        font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
        font_normal = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
    except:
        font_title = ImageFont.load_default()
        font_normal = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # Border
    draw.rectangle([(2, 2), (WIDTH - 2, HEIGHT - 2)], outline=ACCENT, width=2)

    # Title
    y = 20
    draw.text((20, y), "Visitor Intelligence", fill=CYAN, font=font_title)

    # Divider line
    y += 35
    draw.line([(20, y), (WIDTH - 20, y)], fill=ACCENT, width=1)
    y += 15

    if data:
        total = sum(data.values())

        # Total views
        draw.text((20, y), f"Total Views:  {total}", fill=WHITE, font=font_normal)
        y += 35

        # Country breakdown
        draw.text((20, y), "Visitors by Country:", fill=CYAN, font=font_small)
        y += 25

        sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)

        for country, count in sorted_data[:8]:
            # Strip emoji to avoid broken squares
            clean_country = ''.join(c for c in country if ord(c) < 0x10000)
            bar_width = int((count / total) * 300)

            # Progress bar
            draw.rectangle([(20, y), (20 + bar_width, y + 14)], fill=ACCENT)
            draw.text((330, y), f"{clean_country}: {count}", fill=GRAY, font=font_small)
            y += 22

    else:
        draw.text((20, y), "No visitors yet.", fill=WHITE, font=font_normal)

    # Footer
    draw.text((20, HEIGHT - 25), "Real-time tracking • Updates on every visit", fill=(80, 130, 150), font=font_small)

    img_bytes = BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    return img_bytes
