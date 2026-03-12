from PIL import Image

def remove_fake_transparency(img_path, output_path):
    img = Image.open(img_path).convert("RGBA")
    datas = img.getdata()

    new_data = []
    # If a pixel matches the white/grey checkered pattern (R,G,B are very high / close), make it transparent
    # Otherwise keep it (the black silhouette)
    for item in datas:
        r, g, b, a = item
        # Many fake PNG gray squares are (204,204,204) or (192,192,192), white is (255,255,255)
        # We can just say: if it's very light, drop it. The silhouette should be dark.
        if r > 150 and g > 150 and b > 150:
            # Change to transparent
            new_data.append((255, 255, 255, 0))
        else:
            # Keep original silhouette color, but ensure alpha is 255
            new_data.append((r, g, b, 255))

    img.putdata(new_data)
    img.save(output_path, "PNG")

remove_fake_transparency("logo.png", "logo_fixed.png")
print("Saved transparent logo as logo_fixed.png")
