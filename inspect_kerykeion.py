from kerykeion import AstrologicalSubject
from kerykeion.aspects import SynastryAspects
import json

def print_attributes(obj, name):
    print(f"\n{name} attributes:")
    for attr in dir(obj):
        if not attr.startswith('_'):  # Skip private attributes
            try:
                value = getattr(obj, attr)
                if not callable(value):  # Skip methods
                    print(f"  {attr}: {value}")
            except Exception as e:
                print(f"  {attr}: Error accessing - {str(e)}")

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

# Print basic info
print(f"Subject: {subject.name}")
print(f"Birth Date: {subject.year}-{subject.month}-{subject.day} {subject.hour}:{subject.minute}")
print(f"Location: Lat {subject.lat}, Lng {subject.lng}, TZ: {subject.tz_str}")

# Inspect sun attributes
print_attributes(subject.sun, "Sun")

# Inspect moon attributes
print_attributes(subject.moon, "Moon")

# Inspect first house attributes
print_attributes(subject.first_house, "First House")

# Explore available methods
print("\nAvailable methods on AstrologicalSubject:")
for attr in dir(subject):
    if not attr.startswith('_') and callable(getattr(subject, attr)):
        print(f"  {attr}")

# Try to find aspects
print("\nLooking for aspects...")
if hasattr(subject, 'get_all_aspects'):
    print("Found get_all_aspects method")
    aspects = subject.get_all_aspects()
    print(f"Number of aspects: {len(aspects)}")
    for i, aspect in enumerate(aspects):
        if i < 5:  # Just show the first 5 aspects
            print(f"  Aspect {i+1}: {aspect.p1_name} {aspect.aspect} {aspect.p2_name} (orbit: {aspect.orbit}°)")
        else:
            print(f"  ... and {len(aspects) - 5} more aspects")
            break
elif hasattr(subject, 'all_aspects'):
    print("Found all_aspects attribute")
    aspects = subject.all_aspects
    print(f"Number of aspects: {len(aspects)}")
    for i, aspect in enumerate(aspects):
        if i < 5:  # Just show the first 5 aspects
            print(f"  Aspect {i+1}: {aspect.p1_name} {aspect.aspect} {aspect.p2_name} (orbit: {aspect.orbit}°)")
        else:
            print(f"  ... and {len(aspects) - 5} more aspects")
            break
else:
    print("Could not find aspects directly. Trying to create Aspects object...")
    try:
        from kerykeion.aspects import Aspects
        aspects_obj = Aspects(subject)
        if hasattr(aspects_obj, 'all_aspects'):
            aspects = aspects_obj.all_aspects
            print(f"Number of aspects: {len(aspects)}")
            for i, aspect in enumerate(aspects):
                if i < 5:  # Just show the first 5 aspects
                    print(f"  Aspect {i+1}: {aspect.p1_name} {aspect.aspect} {aspect.p2_name} (orbit: {aspect.orbit}°)")
                else:
                    print(f"  ... and {len(aspects) - 5} more aspects")
                    break
    except Exception as e:
        print(f"Error creating Aspects object: {str(e)}")

# Create a second subject for synastry
print("\nCreating second AstrologicalSubject for synastry...")
subject2 = AstrologicalSubject(
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

# Create synastry
print("Creating SynastryAspects...")
synastry = SynastryAspects(subject, subject2)

# Inspect synastry aspects
print("\nSynastry Aspects:")
for i, aspect in enumerate(synastry.all_aspects):
    if i < 5:  # Just show the first 5 aspects
        print(f"  Aspect {i+1}: {aspect.p1_name} ({aspect.p1_owner}) {aspect.aspect} {aspect.p2_name} ({aspect.p2_owner}) (orbit: {aspect.orbit}°)")
    else:
        print(f"  ... and {len(synastry.all_aspects) - 5} more aspects")
        break
