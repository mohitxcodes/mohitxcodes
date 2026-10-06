import os

def create_info_card(output_path="info-card.svg"):
    username = "mohitxcodes"
    role = "Software Engineer"
    stack = "Python, TypeScript, React, Go"
    now_doing = "Building cool things"
    
    # We will build lines out of tspans
    lines = [
        # Command line
        f'<tspan class="prompt-user">mohit@github</tspan><tspan class="prompt-colon">:</tspan><tspan class="prompt-path">~</tspan><tspan class="prompt-dollar">$</tspan> <tspan class="cmd">neofetch</tspan>',
        '',
        # Info
        f'<tspan class="key">Username</tspan><tspan class="colon">: </tspan><tspan class="value">{username}</tspan>',
        f'<tspan class="key">Role</tspan><tspan class="colon">:     </tspan><tspan class="value">{role}</tspan>',
        f'<tspan class="key">Stack</tspan><tspan class="colon">:    </tspan><tspan class="value">{stack}</tspan>',
        f'<tspan class="key">Now</tspan><tspan class="colon">:      </tspan><tspan class="value">{now_doing}</tspan>',
    ]
    
    is_static = os.environ.get("STATIC", "0") == "1"
    
    width = 490
    height = 200
    line_height = 22
    
    svg_content = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">',
        '''<style>
            .terminal { font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace; font-size: 14px; font-weight: 500; }
            .prompt-user { fill: #3fb950; font-weight: bold; }
            .prompt-colon { fill: #c9d1d9; }
            .prompt-path { fill: #58a6ff; font-weight: bold; }
            .prompt-dollar { fill: #c9d1d9; }
            .cmd { fill: #c9d1d9; }
            
            .key { fill: #58a6ff; font-weight: bold; }
            .colon { fill: #c9d1d9; }
            .value { fill: #c9d1d9; }
            
            .anim-line {
                opacity: 0;
                animation: fadeSlideIn 0.3s forwards;
            }
            @keyframes fadeSlideIn {
                from { opacity: 0; transform: translateX(-10px); }
                to { opacity: 1; transform: translateX(0); }
            }
        </style>'''
    ]
    
    # Background (optional, or transparent)
    svg_content.append(f'<rect width="{width}" height="{height}" fill="#0d1117" rx="8" />')
    
    # macOS style dots
    svg_content.append('''
        <circle cx="20" cy="20" r="6" fill="#ff5f56" />
        <circle cx="40" cy="20" r="6" fill="#ffbd2e" />
        <circle cx="60" cy="20" r="6" fill="#27c93f" />
    ''')
    
    svg_content.append('<g class="terminal">')
    for i, line in enumerate(lines):
        y = 60 + i * line_height
        delay = i * 0.15
        
        if is_static or line == '':
            # Ensure empty lines don't get animated or if static is true
            svg_content.append(f'<text x="20" y="{y}">{line}</text>')
        else:
            # We animate the whole text block for that line
            svg_content.append(f'<text x="20" y="{y}" class="anim-line" style="animation-delay: {delay}s">{line}</text>')
            
    svg_content.append('</g>')
    svg_content.append('</svg>')
    
    with open(output_path, 'w') as f:
        f.write('\n'.join(svg_content))
    
    print(f"Saved {output_path}")

if __name__ == "__main__":
    create_info_card()
