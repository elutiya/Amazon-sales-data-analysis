import os

# Folder where all your HTML files are (current folder)
visuals_folder = "."

# Path for the combined dashboard
combined_file = "dashboard.html"

# Automatically find all .html files except the dashboard itself
html_files = [f for f in os.listdir(visuals_folder) if f.endswith(".html") and f != combined_file]

if not html_files:
    print("⚠️ No HTML files found in the folder!")
    exit()

# Base HTML with dark theme and grid layout
base_html = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>My KPI Dashboard</title>
  <style>
    body { background-color: #1e1e1e; color: white; font-family: Arial, sans-serif; margin: 20px; }
    h1 { text-align: center; margin-bottom: 40px; }
    .grid-container { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
    .grid-item { background-color: #2b2b2b; padding: 10px; border-radius: 12px; box-shadow: 0 4px 8px rgba(0,0,0,0.3); }
    iframe { width: 100%; height: 400px; border: none; }
  </style>
</head>
<body>
<h1>My KPI Dashboard</h1>
<div class="grid-container">
"""

# Write the base HTML
with open(combined_file, "w", encoding="utf-8") as f:
    f.write(base_html)

# Add each figure as an iframe
for file in html_files:
    iframe_html = f'<div class="grid-item"><iframe src="{file}"></iframe></div>\n'
    with open(combined_file, "a", encoding="utf-8") as f:
        f.write(iframe_html)

# Close HTML tags
with open(combined_file, "a", encoding="utf-8") as f:
    f.write("</div>\n</body>\n</html>")

print(f"✅ Dashboard created: {combined_file}")