from kerykeion import AstrologicalSubject, KerykeionChartSVG
import os

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

# Set output directory to current directory
output_dir = os.getcwd()
print(f"Setting output directory to: {output_dir}")

# Create a chart for natal chart
print("Creating Natal KerykeionChartSVG...")
natal_chart = KerykeionChartSVG(subject, chart_type="Natal")
natal_chart.set_output_directory(output_dir)

# Generate SVG
print("\nGenerating Natal SVG...")
try:
    svg_path = natal_chart.makeSVG()
    print(f"Natal SVG generated at: {svg_path}")
except Exception as e:
    print(f"Error generating Natal SVG: {str(e)}")

# Create a transit subject
print("\nCreating Transit AstrologicalSubject...")
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

# Create a transit chart (using natal as first object and transit as second)
print("Creating Transit KerykeionChartSVG...")
try:
    # For transit charts, we need to use the natal chart as the first object
    # and the transit chart as the second object
    transit_chart = KerykeionChartSVG(subject, chart_type="Transit", second_obj=transit_subject)
    transit_chart.set_output_directory(output_dir)
    
    # Generate SVG
    print("Generating Transit SVG...")
    svg_path = transit_chart.makeSVG()
    print(f"Transit SVG generated at: {svg_path}")
except Exception as e:
    print(f"Error generating Transit SVG: {str(e)}")

# Create a combined/synastry chart
print("\nCreating Synastry KerykeionChartSVG...")
try:
    synastry_chart = KerykeionChartSVG(subject, chart_type="Synastry", second_obj=transit_subject)
    synastry_chart.set_output_directory(output_dir)
    
    # Generate SVG
    print("Generating Synastry SVG...")
    svg_path = synastry_chart.makeSVG()
    print(f"Synastry SVG generated at: {svg_path}")
except Exception as e:
    print(f"Error generating Synastry SVG: {str(e)}")

# Try to set theme and language
print("\nTesting theme and language settings...")
try:
    themed_chart = KerykeionChartSVG(subject, chart_type="Natal")
    themed_chart.set_output_directory(output_dir)
    
    # Try to set theme if method exists
    if hasattr(themed_chart, 'set_up_theme'):
        print("Setting theme to 'dark'...")
        themed_chart.set_up_theme("dark")
    
    # Generate SVG
    print("Generating themed SVG...")
    svg_path = themed_chart.makeSVG()
    print(f"Themed SVG generated at: {svg_path}")
except Exception as e:
    print(f"Error generating themed SVG: {str(e)}")

# Check if we can get the SVG content as a string instead of saving to file
print("\nTrying to get SVG content as string...")
try:
    string_chart = KerykeionChartSVG(subject, chart_type="Natal")
    
    # Try different methods to get SVG as string
    if hasattr(string_chart, 'makeTemplate'):
        print("Using makeTemplate() method...")
        svg_content = string_chart.makeTemplate()
        print(f"SVG content length: {len(svg_content)} characters")
        
        # Save to file manually
        with open("template_chart.svg", "w") as f:
            f.write(svg_content)
        print("SVG content saved to template_chart.svg")
except Exception as e:
    print(f"Error getting SVG as string: {str(e)}")
