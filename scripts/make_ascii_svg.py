import sys
from PIL import Image

RAMP = " .`:-=+*cs#%@"

def create_ascii_svg(image_path="source-prepped.png", output_path="avi-ascii.svg"):
    try:
        img = Image.open(image_path).convert('L')
    except Exception as e:
        print(f"Could not open {image_path}: {e}")
        return

    # Resize to character grid
    # A typical terminal character is about 2x taller than it is wide.
    # To get ~100x53, let's target width=100. 
    target_width = 100
    w, h = img.size
    aspect_ratio = h / w
    target_height = int(target_width * aspect_ratio * 0.5)
    
    img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
    
    ascii_rows = []
    for y in range(target_height):
        row = ""
        for x in range(target_width):
            pixel = img.getpixel((x, y))
            # Invert so black is mapped to densest char, white to space
            # RAMP goes from sparse (bright) to dense (dark)
            idx = int(( (255 - pixel) / 255 ) * (len(RAMP) - 1))
            row += RAMP[idx]
        ascii_rows.append(row)
    
    # SVG construction
    char_width = 7
    line_height = 14
    width = target_width * char_width
    height = target_height * line_height
    
    svg_content = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">',
        '<style>',
        '  text { font-family: monospace; font-size: 12px; fill: #c9d1d9; white-space: pre; }',
        '</style>'
    ]
    
    for i, row in enumerate(ascii_rows):
        y_pos = (i + 1) * line_height
        delay = i * 0.05
        
        # Each line gets a clip path that animates its width to reveal the text
        clip_id = f"wipe-{i}"
        
        svg_content.append(f'''
        <clipPath id="{clip_id}">
            <rect x="0" y="{y_pos - line_height}" width="0" height="{line_height + 2}">
                <animate attributeName="width" from="0" to="{width}" dur="0.5s" begin="{delay}s" fill="freeze" />
            </rect>
        </clipPath>
        <text x="0" y="{y_pos}" clip-path="url(#{clip_id})">{row}</text>
        ''')
        
    svg_content.append('</svg>')
    
    with open(output_path, 'w') as f:
        f.write('\n'.join(svg_content))
    
    print(f"Saved {output_path}")

if __name__ == "__main__":
    create_ascii_svg()
