from kerykeion import AstrologicalSubject, KerykeionChartSVG
import os

# Create a test subject for natal chart
print("Creating Natal AstrologicalSubject...")
natal_subject = AstrologicalSubject(
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

# Create a test subject for transit
print("Creating Transit AstrologicalSubject...")
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

# Test Natal Chart SVG
print("\n--- Testing Natal Chart SVG ---")
try:
    natal_chart = KerykeionChartSVG(natal_subject, chart_type="Natal")
    svg_content = natal_chart.makeTemplate()
    print(f"Natal SVG content length: {len(svg_content)} characters")
    
    # Save to file
    with open("natal_chart.svg", "w") as f:
        f.write(svg_content)
    print("Natal SVG saved to natal_chart.svg")
except Exception as e:
    print(f"Error generating Natal SVG: {str(e)}")

# Test Transit Chart SVG
print("\n--- Testing Transit Chart SVG ---")
try:
    transit_chart = KerykeionChartSVG(natal_subject, chart_type="Transit", second_obj=transit_subject)
    svg_content = transit_chart.makeTemplate()
    print(f"Transit SVG content length: {len(svg_content)} characters")
    
    # Save to file
    with open("transit_chart.svg", "w") as f:
        f.write(svg_content)
    print("Transit SVG saved to transit_chart.svg")
except Exception as e:
    print(f"Error generating Transit SVG: {str(e)}")

# Test Synastry Chart SVG
print("\n--- Testing Synastry Chart SVG ---")
try:
    synastry_chart = KerykeionChartSVG(natal_subject, chart_type="Synastry", second_obj=transit_subject)
    svg_content = synastry_chart.makeTemplate()
    print(f"Synastry SVG content length: {len(svg_content)} characters")
    
    # Save to file
    with open("synastry_chart.svg", "w") as f:
        f.write(svg_content)
    print("Synastry SVG saved to synastry_chart.svg")
except Exception as e:
    print(f"Error generating Synastry SVG: {str(e)}")

# Test theme setting
print("\n--- Testing Theme Setting ---")
try:
    # Try to set theme
    themed_chart = KerykeionChartSVG(natal_subject, chart_type="Natal")
    
    if hasattr(themed_chart, 'set_up_theme'):
        print("Setting theme to 'dark'...")
        themed_chart.set_up_theme("dark")
        
        svg_content = themed_chart.makeTemplate()
        print(f"Themed SVG content length: {len(svg_content)} characters")
        
        # Save to file
        with open("dark_theme_chart.svg", "w") as f:
            f.write(svg_content)
        print("Dark theme SVG saved to dark_theme_chart.svg")
    else:
        print("set_up_theme method not found")
except Exception as e:
    print(f"Error with themed SVG: {str(e)}")

# Test wheel only and aspect grid only
print("\n--- Testing Wheel Only and Aspect Grid Only ---")
try:
    wheel_chart = KerykeionChartSVG(natal_subject, chart_type="Natal")
    
    if hasattr(wheel_chart, 'makeWheelOnlyTemplate'):
        print("Generating wheel only...")
        wheel_content = wheel_chart.makeWheelOnlyTemplate()
        print(f"Wheel only SVG content length: {len(wheel_content)} characters")
        
        # Save to file
        with open("wheel_only.svg", "w") as f:
            f.write(wheel_content)
        print("Wheel only SVG saved to wheel_only.svg")
    else:
        print("makeWheelOnlyTemplate method not found")
        
    if hasattr(wheel_chart, 'makeAspectGridOnlyTemplate'):
        print("Generating aspect grid only...")
        grid_content = wheel_chart.makeAspectGridOnlyTemplate()
        print(f"Aspect grid only SVG content length: {len(grid_content)} characters")
        
        # Save to file
        with open("aspect_grid_only.svg", "w") as f:
            f.write(grid_content)
        print("Aspect grid only SVG saved to aspect_grid_only.svg")
    else:
        print("makeAspectGridOnlyTemplate method not found")
except Exception as e:
    print(f"Error with wheel/grid only: {str(e)}")
