import json
import os
import html

def generate_svg():
    # Load projects from the JSON file
    json_path = os.path.join('data', 'projects.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        projects = json.load(f)

    svg_height = 30 + (len(projects) * 95)

    # Git history inspired project timeline
    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" width="800" height="{svg_height}" viewBox="0 0 800 {svg_height}" fill="none" role="img" aria-label="Featured Projects">
  <title>Featured Projects</title>

  <style>
    :root {{ color-scheme: dark; }}

    .timeline {{ stroke-dasharray: 8 8; animation: timeline 2s linear infinite; }}
    @keyframes timeline {{ to {{ stroke-dashoffset: -16; }} }}

    .project {{ opacity: 0; animation: appear .6s ease-out forwards; }}
    @keyframes appear {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}

    .status {{ animation: pulse 1.8s ease-in-out infinite; }}
    @keyframes pulse {{ 0%,100% {{ opacity: 1; }} 50% {{ opacity: .45; }} }}

    @media (prefers-reduced-motion: reduce) {{
      * {{ animation: none!important; }}
      .project {{ opacity: 1; }}
    }}
  </style>

  <!-- Main background -->
  <rect width="800" height="{svg_height}" rx="12" fill="#161b22"/>
  <rect x="0.5" y="0.5" width="799" height="{svg_height - 1}" rx="12" fill="none" stroke="#30363d"/>

  <!-- Git history timeline -->
  <line class="timeline" x1="48" y1="20" x2="48" y2="{svg_height - 25}" stroke="#38bdf8" stroke-width="1" opacity=".65"/>
'''

    y_offset = 15

    for index, proj in enumerate(projects, start=1):
        title = html.escape(str(proj.get('title', '')))
        desc = html.escape(str(proj.get('description', '')))
        status = html.escape(str(proj.get('status', 'Active')))
        techs = proj.get('technologies', [])

        # Stagger project appearance
        delay = 0.25 + ((index - 1) * 0.2)

        svg_content += f'''
  <!-- Git history entry {index} -->
  <g class="project" style="animation-delay:{delay:.2f}s">

    <!-- Commit node -->
    <circle cx="48" cy="{y_offset + 8}" r="5" fill="#161b22" stroke="#38bdf8" stroke-width="2"/>
    <circle cx="48" cy="{y_offset + 8}" r="2" fill="#38bdf8"/>

    <!-- Commit number -->
    <text x="70" y="{y_offset + 12}" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono','DejaVu Sans Mono',monospace" font-size="10" font-weight="600" fill="#38bdf8">#{index:02d}</text>

    <!-- Project title -->
    <text x="105" y="{y_offset + 12}" font-family="system-ui,-apple-system,sans-serif" font-size="15" font-weight="600" fill="#e6edf3">{title}</text>

    <!-- Status -->
    <circle class="status" cx="676" cy="{y_offset + 8}" r="3" fill="#3fb950"/>
    <text x="688" y="{y_offset + 12}" font-family="system-ui,-apple-system,sans-serif" font-size="11" font-weight="600" fill="#3fb950">{status}</text>

    <!-- Description -->
    <text x="105" y="{y_offset + 35}" font-family="system-ui,-apple-system,sans-serif" font-size="13" fill="#8b949e">{desc}</text>

    <!-- Technologies -->
    <g transform="translate(105,{y_offset + 48})">
'''

        x_tech = 0

        for tech in techs:
            tech_clean = html.escape(str(tech))
            tech_width = len(str(tech)) * 9 + 16

            svg_content += f'''
      <rect x="{x_tech}" y="0" width="{tech_width}" height="20" rx="6" fill="#161b22" stroke="#30363d"/>
      <text x="{x_tech + tech_width / 2}" y="14" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono','DejaVu Sans Mono',monospace" font-size="11" fill="#7dd3fc" text-anchor="middle">{tech_clean}</text>
'''

            x_tech += tech_width + 8

        svg_content += '''
    </g>
  </g>
'''

        y_offset += 95

    svg_content += '''
</svg>
'''

    # Save the result to assets/projects.svg
    output_path = os.path.join('assets', 'projects.svg')

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(svg_content)

    print("✅ Successfully generated assets/projects.svg")


if __name__ == '__main__':
    generate_svg()