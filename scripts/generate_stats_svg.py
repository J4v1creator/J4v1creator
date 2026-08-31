import os
import json
import re
import urllib.request
from datetime import datetime

def fetch_user_data(username):
    """Gets public user data from the GitHub API"""
    url = f"https://api.github.com/users/{username}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"⚠️ Warning: Could not fetch user API data ({e})")
        return None

def fetch_top_language(username):
    """Automatically calculates the most used programming language in your public repositories"""
    url = f"https://api.github.com/users/{username}/repos?per_page=100"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            repos = json.loads(response.read().decode())
            languages = {}
            for repo in repos:
                if not repo.get('fork', False):
                    lang = repo.get('language')
                    if lang:
                        languages[lang] = languages.get(lang, 0) + 1
            if languages:
                # Return the language with the most repositories
                return max(languages, key=languages.get)
    except Exception as e:
        print(f"⚠️ Warning: Could not fetch top language ({e})")
    return "Python" # Default fallback

def fetch_contributions(username):
    """Gets the total number of contributions for the last year from the public profile"""
    url = f"https://github.com/users/{username}/contributions"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            # Search for the numerical pattern in the contributions header
            match = re.search(r'([0-9,]+)\s+contributions\s+in\s+the\s+last\s+year', html)
            if match:
                raw_count = int(match.group(1).replace(',', ''))
                if raw_count >= 1000:
                    return f"{raw_count / 1000:.1f}k"
                return str(raw_count)
    except Exception as e:
        print(f"⚠️ Warning: Could not fetch contributions count ({e})")
    return "100+" # Fallback if it cannot be obtained locally

def generate_svg():
    username = os.environ.get('GITHUB_USERNAME', 'J4v1creator')
    
    # 1. Get data from the GitHub API
    user_data = fetch_user_data(username)
    
    # 2. Total public repositories (automatic)
    public_repos = user_data.get('public_repos', 2) if user_data else 2
    
    # 3. Most used language (automatic)
    top_language = fetch_top_language(username)
    
    # 4. Total contributions (automatic)
    contributions = fetch_contributions(username)
    
    # 5. Exact calculation of years on GitHub
    if user_data and 'created_at' in user_data:
        created_date = datetime.strptime(user_data['created_at'], "%Y-%m-%dT%H:%M:%SZ")
    else:
        created_date = datetime(2023, 8, 31)

    current_date = datetime.now()
    account_age_days = (current_date - created_date).total_seconds() / 86400
    years_on_github = round(account_age_days / 365.2425, 1)

    # SVG dimensions and equal column layout
    svg_width = 1000
    svg_height = 142
    column_width = svg_width / 4
    centers = [column_width * (i + 0.5) for i in range(4)]
    dividers = [column_width * (i + 1) for i in range(3)]
    
    # Generate SVG design with minimalist style in blue/cyan and fade animations
    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{svg_width}" height="{svg_height}" viewBox="0 0 {svg_width} {svg_height}" role="img" aria-label="GitHub Activity &amp; Metrics" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono','DejaVu Sans Mono',monospace">
  <title>GitHub Activity &amp; Metrics</title>
  <style>
    :root {{ color-scheme: dark; }}
    .fade {{ animation: fade .9s ease-out; }}
    @keyframes fade {{ from {{ opacity: 0; }} }}
    .val {{ font-size: 34px; fill: #38bdf8; font-weight: bold; text-anchor: middle; }}
    .lbl {{ font-size: 11px; fill: #e6edf3; text-anchor: middle; letter-spacing: 0.5px; }}
    .sub {{ font-size: 9.5px; fill: #8b949e; text-anchor: middle; letter-spacing: 0.3px; }}
    @media (prefers-reduced-motion: reduce) {{ * {{ animation: none!important; }} }}
  </style>

  <!-- Card background matching terminal/header -->
  <rect x="0.5" y="0.5" width="{svg_width - 1}" height="{svg_height - 1}" rx="10" fill="#161b22" stroke="#30363d"/>

  <!-- Column 1: Total Contributions -->
  <g class="fade" style="animation-delay: 0s;">
    <text x="{centers[0]}" y="62" class="val">{contributions}</text>
    <text x="{centers[0]}" y="84" class="lbl">contributions</text>
    <text x="{centers[0]}" y="100" class="sub">past 12 months</text>
  </g>

  <!-- Dividing line 1 -->
  <line x1="{dividers[0]}" y1="30" x2="{dividers[0]}" y2="112" stroke="#30363d" stroke-dasharray="3 3"/>

  <!-- Column 2: Public Repositories -->
  <g class="fade" style="animation-delay: 0.08s;">
    <text x="{centers[1]}" y="62" class="val">{public_repos}</text>
    <text x="{centers[1]}" y="84" class="lbl">public repositories</text>
    <text x="{centers[1]}" y="100" class="sub">excluding forks</text>
  </g>

  <!-- Dividing line 2 -->
  <line x1="{dividers[1]}" y1="30" x2="{dividers[1]}" y2="112" stroke="#30363d" stroke-dasharray="3 3"/>

  <!-- Column 3: Main Language -->
  <g class="fade" style="animation-delay: 0.16s;">
    <text x="{centers[2]}" y="62" class="val">{top_language}</text>
    <text x="{centers[2]}" y="84" class="lbl">top language</text>
    <text x="{centers[2]}" y="100" class="sub">most used in public repos</text>
  </g>

  <!-- Dividing line 3 -->
  <line x1="{dividers[2]}" y1="30" x2="{dividers[2]}" y2="112" stroke="#30363d" stroke-dasharray="3 3"/>

  <!-- Column 4: Years on GitHub -->
  <g class="fade" style="animation-delay: 0.24s;">
    <text x="{centers[3]}" y="62" class="val">{years_on_github}</text>
    <text x="{centers[3]}" y="84" class="lbl">years</text>
    <text x="{centers[3]}" y="100" class="sub">on GitHub platform</text>
  </g>
</svg>'''

    output_path = os.path.join('assets', 'stats.svg')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(svg_content)
    
    print("✅ Successfully generated assets/stats.svg")

if __name__ == '__main__':
    generate_svg()