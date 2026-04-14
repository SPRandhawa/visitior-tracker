from pathlib import Path
from PIL import Image, ImageDraw


def generate_image(data, output_path):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    img = Image.new('RGB', (520, 320), color=(10, 10, 20))
    draw = ImageDraw.Draw(img)

    y = 20
    draw.text((20, y), "🌍 Visitor Intelligence", fill=(0, 255, 255))
    y += 40

    if data:
        total = sum(data.values())
        draw.text((20, y), f"Total Views: {total}", fill=(255, 255, 255))
        y += 30

        sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)
        for country, count in sorted_data[:10]:
            draw.text((20, y), f"{country}: {count}", fill=(200, 200, 200))
            y += 25
    else:
        draw.text((20, y), "No visitor data yet.", fill=(255, 255, 255))

    img.save(output_path)
    return str(output_path)
