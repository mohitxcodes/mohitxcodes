import sys
import cv2
import numpy as np
from PIL import Image
from rembg import remove

def prep_photo(input_path, output_path="source-prepped.png"):
    print(f"Processing {input_path}...")
    
    # 1. Remove background
    with open(input_path, 'rb') as i:
        input_data = i.read()
    subject_only = remove(input_data)
    
    # Convert rembg output to numpy array for OpenCV
    nparr = np.frombuffer(subject_only, np.uint8)
    img_rgba = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)
    
    # Extract alpha channel
    if img_rgba.shape[2] == 4:
        alpha = img_rgba[:, :, 3]
        img_bgr = img_rgba[:, :, :3]
    else:
        alpha = np.ones(img_rgba.shape[:2], dtype=np.uint8) * 255
        img_bgr = img_rgba
        
    # 2. Boost contrast with CLAHE on L channel of LAB color space
    lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    cl = clahe.apply(l)
    limg = cv2.merge((cl,a,b))
    img_contrasted = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
    
    # 3. Composite onto pure white background
    white_bg = np.ones_like(img_contrasted) * 255
    
    # Normalize alpha to 0-1
    alpha_norm = alpha / 255.0
    
    # Blend
    for c in range(3):
        white_bg[:,:,c] = (alpha_norm * img_contrasted[:,:,c] + (1 - alpha_norm) * white_bg[:,:,c])
        
    # Convert to grayscale for ASCII prep
    gray = cv2.cvtColor(white_bg, cv2.COLOR_BGR2GRAY)
    
    cv2.imwrite(output_path, gray)
    print(f"Saved {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python prep_photo.py <source-photo>")
        sys.exit(1)
    prep_photo(sys.argv[1])
