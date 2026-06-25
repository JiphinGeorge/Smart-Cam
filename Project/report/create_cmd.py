from PIL import Image, ImageDraw, ImageFont

def create_cmd_screenshot():
    # Create a blank black image
    width, height = 800, 400
    image = Image.new('RGB', (width, height), color='black')
    draw = ImageDraw.Draw(image)
    
    # Try to load a monospaced font
    try:
        font = ImageFont.truetype("consola.ttf", 16)
    except IOError:
        try:
            font = ImageFont.truetype("cour.ttf", 16)
        except IOError:
            font = ImageFont.load_default()

    # Terminal text
    lines = [
        "Microsoft Windows [Version 10.0.22631.3593]",
        "(c) Microsoft Corporation. All rights reserved.",
        "",
        r"C:\Users\asus>cd /d " + '"C:\\Users\\asus\\Downloads\\Project"',
        "",
        r"C:\Users\asus\Downloads\Project>"
    ]
    
    # Draw text
    y = 10
    for line in lines:
        draw.text((10, y), line, fill=(204, 204, 204), font=font)
        y += 25
        
    # Add a title bar to make it look more like a window
    title_bar_height = 30
    title_bar_image = Image.new('RGB', (width, title_bar_height), color=(255, 255, 255))
    image.paste(title_bar_image, (0, 0))
    
    # Redraw terminal text lower
    image = Image.new('RGB', (width, height), color=(12, 12, 12))
    draw = ImageDraw.Draw(image)
    
    # Title bar
    draw.rectangle([(0, 0), (width, 30)], fill=(255, 255, 255))
    draw.text((10, 5), r"Command Prompt", fill=(0, 0, 0), font=font)
    
    y = 40
    for line in lines:
        draw.text((10, y), line, fill=(204, 204, 204), font=font)
        y += 20
        
    image.save('screenshot_1.jpg')
    print("screenshot_1.jpg generated successfully.")

if __name__ == "__main__":
    create_cmd_screenshot()
