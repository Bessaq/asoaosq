import requests
import json

# Load the natal chart data
with open('natal_chart_data.json', 'r') as f:
    natal_data = json.load(f)

# Test the natal chart endpoint
print("Testing /api/v1/natal_chart endpoint...")
response = requests.post('http://localhost:8000/api/v1/natal_chart', json=natal_data)
print(f"Status code: {response.status_code}")
if response.status_code == 200:
    result = response.json()
    print("Success! Natal chart calculated.")
    print(f"Sun in {result['planets']['sun']['sign']} at {result['planets']['sun']['longitude']}°")
    print(f"Moon in {result['planets']['moon']['sign']} at {result['planets']['moon']['longitude']}°")
    print(f"Ascendant in {result['ascendant']['sign']} at {result['ascendant']['longitude']}°")
else:
    print(f"Error: {response.text}")

# Test the current transits endpoint
print("\nTesting /api/v1/current_transits endpoint...")
transit_data = {
    "year": 2025,
    "month": 5,
    "day": 28,
    "hour": 12,
    "minute": 0,
    "longitude": -46.6333,
    "latitude": -23.5505,
    "tz_str": "America/Sao_Paulo",
    "house_system": "Placidus",
    "language": "pt"
}
response = requests.post('http://localhost:8000/api/v1/current_transits', json=transit_data)
print(f"Status code: {response.status_code}")
if response.status_code == 200:
    result = response.json()
    print("Success! Current transits calculated.")
    print(f"Sun in {result['planets']['sun']['sign']} at {result['planets']['sun']['longitude']}°")
    print(f"Moon in {result['planets']['moon']['sign']} at {result['planets']['moon']['longitude']}°")
else:
    print(f"Error: {response.text}")

# Test the transits to natal endpoint
print("\nTesting /api/v1/transits_to_natal endpoint...")
transits_to_natal_data = {
    "natal": natal_data,
    "transit": transit_data
}
response = requests.post('http://localhost:8000/api/v1/transits_to_natal', json=transits_to_natal_data)
print(f"Status code: {response.status_code}")
if response.status_code == 200:
    result = response.json()
    print("Success! Transits to natal calculated.")
    print(f"Found {len(result['aspects'])} aspects between transit and natal planets.")
    if len(result['aspects']) > 0:
        aspect = result['aspects'][0]
        print(f"Example: {aspect['p1_name']} ({aspect['p1_owner']}) {aspect['aspect']} {aspect['p2_name']} ({aspect['p2_owner']})")
else:
    print(f"Error: {response.text}")

# Test the SVG chart endpoint
print("\nTesting /api/v1/svg_chart_base64 endpoint...")
svg_data = {
    "natal_chart": natal_data,
    "chart_type": "natal",
    "show_aspects": True,
    "language": "pt",
    "theme": "light"
}
response = requests.post('http://localhost:8000/api/v1/svg_chart_base64', json=svg_data)
print(f"Status code: {response.status_code}")
if response.status_code == 200:
    result = response.json()
    print("Success! SVG chart generated.")
    print(f"SVG data URI length: {len(result['data_uri'])}")
    
    # Save the SVG to a file
    import base64
    svg_content = base64.b64decode(result['svg_base64'])
    with open('test_chart.svg', 'wb') as f:
        f.write(svg_content)
    print("SVG saved to test_chart.svg")
else:
    print(f"Error: {response.text}")
