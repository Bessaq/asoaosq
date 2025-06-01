from kerykeion import AstrologicalSubject, KerykeionChartSVG

# Create a test subject
print("Creating AstrologicalSubject...")
subject = AstrologicalSubject(
    name="Test Person",
    year=1990,
    month=7,
    day=15,
    hour=14,
    minute=30,
    lng=-46.6333,
    lat=-23.5505,
    tz_str="America/Sao_Paulo"
)

# Create a chart
print("Creating KerykeionChartSVG...")
chart = KerykeionChartSVG(subject)

# Check available methods
print("\nAvailable methods on KerykeionChartSVG:")
for attr in dir(chart):
    if not attr.startswith('_') and callable(getattr(chart, attr)):
        print(f"  {attr}")

# Try to get SVG
print("\nTrying to get SVG...")
try:
    # Try different methods to get SVG
    if hasattr(chart, 'makeSVG'):
        svg = chart.makeSVG()
        print(f"SVG generated using makeSVG(), length: {len(svg)} characters")
    elif hasattr(chart, 'get_svg'):
        svg = chart.get_svg()
        print(f"SVG generated using get_svg(), length: {len(svg)} characters")
    elif hasattr(chart, 'get_svg_string'):
        svg = chart.get_svg_string()
        print(f"SVG generated using get_svg_string(), length: {len(svg)} characters")
    else:
        print("Could not find method to generate SVG")
        
    # Save SVG to file
    with open("test_chart.svg", "w") as f:
        f.write(svg)
    print(f"SVG saved to test_chart.svg")
    
except Exception as e:
    print(f"Error generating SVG: {str(e)}")

# Try to create a transit chart
print("\nTrying to create a transit chart...")
try:
    transit_subject = AstrologicalSubject(
        name="Transit",
        year=2025,
        month=5,
        day=28,
        hour=12,
        minute=0,
        lng=-46.6333,
        lat=-23.5505,
        tz_str="America/Sao_Paulo"
    )
    
    # Try different chart types
    print("Creating transit chart...")
    transit_chart = KerykeionChartSVG(transit_subject, chart_type="Transit")
    
    # Try to get SVG
    if hasattr(transit_chart, 'makeSVG'):
        svg = transit_chart.makeSVG()
        print(f"Transit SVG generated using makeSVG(), length: {len(svg)} characters")
    elif hasattr(transit_chart, 'get_svg'):
        svg = transit_chart.get_svg()
        print(f"Transit SVG generated using get_svg(), length: {len(svg)} characters")
    elif hasattr(transit_chart, 'get_svg_string'):
        svg = transit_chart.get_svg_string()
        print(f"Transit SVG generated using get_svg_string(), length: {len(svg)} characters")
    else:
        print("Could not find method to generate transit SVG")
    
    # Save SVG to file
    with open("test_transit_chart.svg", "w") as f:
        f.write(svg)
    print(f"Transit SVG saved to test_transit_chart.svg")
    
    # Try combined chart
    print("\nCreating combined chart...")
    combined_chart = KerykeionChartSVG(subject, chart_type="Synastry", second_obj=transit_subject)
    
    # Try to get SVG
    if hasattr(combined_chart, 'makeSVG'):
        svg = combined_chart.makeSVG()
        print(f"Combined SVG generated using makeSVG(), length: {len(svg)} characters")
    elif hasattr(combined_chart, 'get_svg'):
        svg = combined_chart.get_svg()
        print(f"Combined SVG generated using get_svg(), length: {len(svg)} characters")
    elif hasattr(combined_chart, 'get_svg_string'):
        svg = combined_chart.get_svg_string()
        print(f"Combined SVG generated using get_svg_string(), length: {len(svg)} characters")
    else:
        print("Could not find method to generate combined SVG")
    
    # Save SVG to file
    with open("test_combined_chart.svg", "w") as f:
        f.write(svg)
    print(f"Combined SVG saved to test_combined_chart.svg")
    
except Exception as e:
    print(f"Error creating transit chart: {str(e)}")
