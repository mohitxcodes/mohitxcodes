import json
import os
from datetime import datetime

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]

def render_heatmap(input_path="data/contributions.json", output_path="contrib-heatmap-test.svg"):
    with open(input_path, "r") as f:
        data = json.load(f)
        
    days = data.get("days", [])
    stats = data.get("stats", {})
    
    # We might need total contributions. If not available, we use a placeholder or calculate active days.
    # We can fetch total contributions via bs4 if needed, but let's just use what we have or a placeholder.
    total_active = stats.get("total_active_days", 0)
    
    # Calculate grid layout
    box_size = 10
    gap = 4
    week_width = box_size + gap
    
    # SVG dimensions
    width = 860
    height = 240
    
    # Layout constants
    margin_left = 40
    margin_top = 80
    
    svg_content = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">',
        '''<style>
            .terminal { font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace; }
            .bg { fill: #0d1117; }
            .box { rx: 2; ry: 2; }
            .anim-box {
                opacity: 0;
                transform: scale(0.8);
                animation: popIn 0.3s forwards;
            }
            .text-muted { fill: #8b949e; font-size: 12px; }
            .text-bold { fill: #c9d1d9; font-weight: bold; font-size: 14px; }
            .prompt-bg { fill: #21262d; rx: 6; ry: 6; }
            .prompt-text { fill: #ffffff; font-weight: bold; font-size: 18px; }
            @keyframes popIn {
                to { opacity: 1; transform: scale(1); }
            }
        </style>''',
        # Background
        f'<rect class="bg" width="{width}" height="{height}" />'
    ]
    
    # Header: avi@github ~ $ ./contributions.sh
    # We will center it
    prompt_text = "avi@github ~ $ ./contributions.sh"
    # Estimate text width (approx 10px per char for 18px font) -> 33 chars * 11 = 363
    # Let's just use text-anchor="middle"
    prompt_width = 400
    prompt_height = 36
    prompt_x = (width - prompt_width) // 2
    prompt_y = 15
    
    svg_content.append(f'<rect class="prompt-bg" x="{prompt_x}" y="{prompt_y}" width="{prompt_width}" height="{prompt_height}" />')
    svg_content.append(f'<text x="{width//2}" y="{prompt_y + 24}" class="terminal prompt-text" text-anchor="middle">{prompt_text}</text>')
    
    # Draw Days (Mon, Wed, Fri)
    days_y_offsets = {1: "Mon", 3: "Wed", 5: "Fri"}
    for row, label in days_y_offsets.items():
        y = margin_top + row * week_width + 10
        svg_content.append(f'<text x="{margin_left - 8}" y="{y}" class="terminal text-muted" text-anchor="end">{label}</text>')
    
    # Determine Months layout
    # Group by columns (weeks). For each column, get the month of the first day.
    col = 0
    row = 0
    col_months = {} # col_index -> month_name
    
    last_month = None
    
    cells = []
    
    # Assuming data is chronologically ordered day by day, starting from some day.
    # Usually GitHub data starts on Sunday.
    for i, day in enumerate(days):
        if row > 6:
            row = 0
            col += 1
            
        date_str = day.get("date")
        if date_str:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            month_name = dt.strftime("%b")
            
            # Label the month if it changed and we are in the first row (or just checking the column)
            if row == 0:
                if month_name != last_month:
                    # To prevent overlapping, only add if col > 0 or it's the first col
                    col_months[col] = month_name
                    last_month = month_name
                
        x = margin_left + col * week_width
        y = margin_top + row * week_width
        level = min(day.get("level", 0), len(PALETTE) - 1)
        color = PALETTE[level]
        
        delay = (row + col) * 0.02
        cells.append(
            f'<rect class="box anim-box" x="{x}" y="{y}" width="{box_size}" height="{box_size}" fill="{color}" '
            f'style="animation-delay: {delay}s" />'
        )
        row += 1
        
    # Draw Months
    for c, m in col_months.items():
        x = margin_left + c * week_width
        y = margin_top - 8
        svg_content.append(f'<text x="{x}" y="{y}" class="terminal text-muted">{m}</text>')
        
    # Draw Cells
    svg_content.extend(cells)
    
    # Footer
    # "8,514 contributions in the last year"
    footer_text = f"8,514 contributions in the last year"
    footer_y = margin_top + 7 * week_width + 20
    svg_content.append(f'<text x="{margin_left}" y="{footer_y}" class="terminal text-bold">{footer_text}</text>')
    
    svg_content.append('</svg>')
    
    with open(output_path, "w") as f:
        f.write('\n'.join(svg_content))
        
    print(f"Saved {output_path}")

if __name__ == "__main__":
    render_heatmap()
