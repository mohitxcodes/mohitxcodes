import json
import os

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]

def render_heatmap(input_path="data/contributions.json", output_path="contrib-heatmap.svg"):
    if not os.path.exists(input_path):
        print(f"File {input_path} not found.")
        return
        
    with open(input_path, "r") as f:
        data = json.load(f)
        
    days = data.get("days", [])
    
    # Calculate grid layout
    box_size = 10
    gap = 4
    week_width = box_size + gap
    
    width = 860
    height = 200
    
    svg_content = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">',
        '''<style>
            .terminal { font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace; font-size: 14px; fill: #c9d1d9; }
            .box { rx: 2; ry: 2; }
            .anim-box {
                opacity: 0;
                transform: scale(0.8);
                animation: popIn 0.3s forwards;
            }
            @keyframes popIn {
                to { opacity: 1; transform: scale(1); }
            }
        </style>'''
    ]
    
    # Title
    svg_content.append('<text x="20" y="30" class="terminal" font-weight="bold" fill="#3fb950">Contributions Heatmap</text>')
    
    svg_content.append('<g transform="translate(20, 50)">')
    
    # GitHub layout: column by column (weeks), row by row (days)
    # The scraped data is usually linear (day by day).
    # We organize it into columns.
    
    col = 0
    row = 0
    for i, day in enumerate(days):
        # determine row (0-6) and col
        # GitHub's grid is 7 days tall
        # Usually it starts on Sunday, so let's just group by 7
        if row > 6:
            row = 0
            col += 1
            
        x = col * week_width
        y = row * week_width
        level = min(day.get("level", 0), 4)
        color = PALETTE[level]
        
        # Diagonal slide-down stagger:
        # delay based on (row + col)
        delay = (row + col) * 0.02
        
        svg_content.append(
            f'<rect class="box anim-box" x="{x}" y="{y}" width="{box_size}" height="{box_size}" fill="{color}" '
            f'style="animation-delay: {delay}s" />'
        )
        row += 1
        
    svg_content.append('</g>')
    svg_content.append('</svg>')
    
    with open(output_path, "w") as f:
        f.write('\n'.join(svg_content))
        
    print(f"Saved {output_path}")

if __name__ == "__main__":
    render_heatmap()
