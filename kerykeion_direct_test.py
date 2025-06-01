from kerykeion import AstrologicalSubject

try:
    print("Tentando criar AstrologicalSubject com dados modernos...")
    subject = AstrologicalSubject(
        name="Test Modern Date",
        year=2000,
        month=1,
        day=1,
        hour=12,
        minute=0,
        city="London",
        nation="UK",
        lng=0.0,
        lat=51.5,
        tz_str="UTC"
    )
    print("AstrologicalSubject criado com sucesso!")
    print(f"Sol: {subject.sun.name} em {subject.sun.sign} a {subject.sun.position}°")
    print(f"Ascendente: {subject.first_house.sign} a {subject.first_house.position}°")

except Exception as e:
    print(f"Erro ao usar Kerykeion diretamente: {type(e).__name__} - {str(e)}")
    import traceback
    traceback.print_exc()

