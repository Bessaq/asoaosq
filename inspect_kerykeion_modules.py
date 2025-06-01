import importlib
import pkgutil
import sys

def explore_package(package_name):
    print(f"Exploring package: {package_name}")
    
    try:
        # Import the package
        package = importlib.import_module(package_name)
        
        # Get the package path
        package_path = getattr(package, '__path__', [None])[0]
        print(f"Package path: {package_path}")
        
        # List all modules in the package
        print(f"\nModules in {package_name}:")
        for _, name, is_pkg in pkgutil.iter_modules([package_path]):
            module_type = "Package" if is_pkg else "Module"
            print(f"  {module_type}: {name}")
            
            # If it's a package, explore it recursively
            if is_pkg:
                explore_package(f"{package_name}.{name}")
        
        # List all attributes in the package
        print(f"\nAttributes in {package_name}:")
        for attr in dir(package):
            if not attr.startswith('_'):  # Skip private attributes
                try:
                    value = getattr(package, attr)
                    attr_type = type(value).__name__
                    print(f"  {attr} ({attr_type})")
                except Exception as e:
                    print(f"  {attr} (Error: {str(e)})")
    
    except ImportError as e:
        print(f"Error importing {package_name}: {str(e)}")
    except Exception as e:
        print(f"Error exploring {package_name}: {str(e)}")

# Explore the kerykeion package
explore_package("kerykeion")

# Specifically check for chart-related modules
print("\n\nChecking for chart-related modules...")
try:
    from kerykeion import charts
    print("Successfully imported kerykeion.charts")
    
    print("\nAttributes in kerykeion.charts:")
    for attr in dir(charts):
        if not attr.startswith('_'):  # Skip private attributes
            try:
                value = getattr(charts, attr)
                attr_type = type(value).__name__
                print(f"  {attr} ({attr_type})")
            except Exception as e:
                print(f"  {attr} (Error: {str(e)})")
except ImportError as e:
    print(f"Error importing kerykeion.charts: {str(e)}")

# Check installed version
try:
    import kerykeion
    print(f"\nKerykeion version: {kerykeion.__version__ if hasattr(kerykeion, '__version__') else 'Unknown'}")
except Exception as e:
    print(f"Error getting Kerykeion version: {str(e)}")

# Check if SVG generation is available
print("\nChecking for SVG generation functionality...")
try:
    from kerykeion import AstrologicalSubject
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
    
    # Check if subject has any chart-related methods
    chart_methods = [attr for attr in dir(subject) if 'chart' in attr.lower() and callable(getattr(subject, attr))]
    if chart_methods:
        print(f"Found chart-related methods on AstrologicalSubject:")
        for method in chart_methods:
            print(f"  {method}")
    else:
        print("No chart-related methods found on AstrologicalSubject")
    
    # Try to find any SVG-related functionality
    import kerykeion
    svg_modules = []
    for module_name in sys.modules:
        if module_name.startswith('kerykeion') and 'svg' in module_name.lower():
            svg_modules.append(module_name)
    
    if svg_modules:
        print(f"\nFound SVG-related modules:")
        for module in svg_modules:
            print(f"  {module}")
    else:
        print("\nNo SVG-related modules found")
    
except Exception as e:
    print(f"Error checking for SVG generation: {str(e)}")
