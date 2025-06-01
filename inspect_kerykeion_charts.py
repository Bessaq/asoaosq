from kerykeion import AstrologicalSubject
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

# Explore chart-related functionality
print("\nExploring chart functionality...")

# Check if KerykeionChartSVG exists
try:
    from kerykeion.charts import KerykeionChartSVG
    print("Found KerykeionChartSVG class")
    
    # Try to create a chart
    print("Creating chart...")
    chart = KerykeionChartSVG(subject)
    
    # Check available methods
    print("\nAvailable methods on KerykeionChartSVG:")
    for attr in dir(chart):
        if not attr.startswith('_') and callable(getattr(chart, attr)):
            print(f"  {attr}")
    
    # Try to get SVG
    print("\nTrying to get SVG...")
    if hasattr(chart, 'get_svg'):
        svg = chart.get_svg()
        print(f"SVG generated successfully, length: {len(svg)} characters")
        
        # Save SVG to file for inspection
        with open("test_chart.svg", "w") as f:
            f.write(svg)
        print(f"SVG saved to {os.path.abspath('test_chart.svg')}")
    elif hasattr(chart, 'makeSVG'):
        svg = chart.makeSVG()
        print(f"SVG generated successfully, length: {len(svg)} characters")
        
        # Save SVG to file for inspection
        with open("test_chart.svg", "w") as f:
            f.write(svg)
        print(f"SVG saved to {os.path.abspath('test_chart.svg')}")
    else:
        print("Could not find method to generate SVG")
    
    # Check if there's a method for language customization
    language_methods = [attr for attr in dir(chart) if 'language' in attr.lower() and callable(getattr(chart, attr))]
    if language_methods:
        print("\nFound language-related methods:")
        for method in language_methods:
            print(f"  {method}")
    else:
        print("\nNo language-related methods found")
    
except ImportError as e:
    print(f"Could not import KerykeionChartSVG: {str(e)}")
    
    # Try alternative chart classes
    try:
        print("\nTrying alternative chart classes...")
        from kerykeion.charts import MakeSvgChart
        print("Found MakeSvgChart class")
        
        # Try to create a chart
        print("Creating chart...")
        chart = MakeSvgChart(subject)
        
        # Check available methods
        print("\nAvailable methods on MakeSvgChart:")
        for attr in dir(chart):
            if not attr.startswith('_') and callable(getattr(chart, attr)):
                print(f"  {attr}")
        
        # Try to get SVG
        print("\nTrying to get SVG...")
        if hasattr(chart, 'get_svg'):
            svg = chart.get_svg()
            print(f"SVG generated successfully, length: {len(svg)} characters")
            
            # Save SVG to file for inspection
            with open("test_chart.svg", "w") as f:
                f.write(svg)
            print(f"SVG saved to {os.path.abspath('test_chart.svg')}")
        elif hasattr(chart, 'get_svg_string'):
            svg = chart.get_svg_string()
            print(f"SVG generated successfully, length: {len(svg)} characters")
            
            # Save SVG to file for inspection
            with open("test_chart.svg", "w") as f:
                f.write(svg)
            print(f"SVG saved to {os.path.abspath('test_chart.svg')}")
        else:
            print("Could not find method to generate SVG")
        
        # Check if there's a method for language customization
        language_methods = [attr for attr in dir(chart) if 'language' in attr.lower() and callable(getattr(chart, attr))]
        if language_methods:
            print("\nFound language-related methods:")
            for method in language_methods:
                print(f"  {method}")
        else:
            print("\nNo language-related methods found")
        
    except ImportError as e:
        print(f"Could not import MakeSvgChart: {str(e)}")
except Exception as e:
    print(f"Error exploring chart functionality: {str(e)}")
