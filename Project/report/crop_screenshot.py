from PIL import Image, ImageChops

def crop_black_borders(img_path):
    img = Image.open(img_path)
    
    # Convert to grayscale for thresholding
    gray = img.convert('L')
    
    bg = Image.new('RGB', img.size, (0, 0, 0))
    diff = ImageChops.difference(img.convert('RGB'), bg)
    bbox = diff.getbbox()
    
    if bbox:
        padding = 20
        left, upper, right, lower = bbox
        
        # We mostly care about cropping the bottom
        lower = min(img.height, lower + padding)
        
        # Crop the image (only vertically, keep full width)
        cropped = img.crop((0, 0, img.width, lower))
        cropped.save(img_path)
        print(f"Cropped {img_path} to height {lower}")
    else:
        print("Could not find non-black pixels.")

if __name__ == "__main__":
    crop_black_borders('screenshot_2.jpg')
