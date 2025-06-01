# Implementação de Interpretações Textuais Básicas

Vamos implementar interpretações textuais básicas para signos, planetas e aspectos na API, conforme a estratégia definida anteriormente.

## 1. Criação do Banco de Interpretações

Primeiro, vamos criar um arquivo JSON com interpretações básicas para diferentes elementos astrológicos:

```python
# Em app/data/interpretations.json
{
  "planets_in_signs": {
    "sun": {
      "Áries": "O Sol em Áries confere uma personalidade dinâmica, corajosa e pioneira. Há uma forte necessidade de autoafirmação e independência. Pessoas com Sol em Áries tendem a ser diretas, entusiasmadas e possuem iniciativa para começar novos projetos.",
      "Touro": "O Sol em Touro indica uma personalidade estável, prática e determinada. Há uma forte conexão com o mundo material e valorização da segurança. Pessoas com Sol em Touro tendem a ser pacientes, confiáveis e apreciam conforto e beleza.",
      "Gêmeos": "O Sol em Gêmeos revela uma personalidade versátil, curiosa e comunicativa. Há uma necessidade constante de estímulo mental e troca de informações. Pessoas com Sol em Gêmeos tendem a ser adaptáveis, sociáveis e possuem facilidade para aprender.",
      "Câncer": "O Sol em Câncer indica uma personalidade sensível, protetora e emocional. Há uma forte conexão com a família e o lar. Pessoas com Sol em Câncer tendem a ser intuitivas, cuidadosas e valorizam a segurança emocional.",
      "Leão": "O Sol em Leão confere uma personalidade carismática, criativa e orgulhosa. Há uma necessidade de reconhecimento e expressão pessoal. Pessoas com Sol em Leão tendem a ser generosas, leais e possuem uma presença marcante.",
      "Virgem": "O Sol em Virgem revela uma personalidade analítica, prática e meticulosa. Há uma necessidade de ordem e aperfeiçoamento. Pessoas com Sol em Virgem tendem a ser trabalhadoras, detalhistas e possuem um forte senso de dever.",
      "Libra": "O Sol em Libra indica uma personalidade diplomática, harmoniosa e sociável. Há uma necessidade de equilíbrio e relacionamentos. Pessoas com Sol em Libra tendem a ser justas, elegantes e valorizam a cooperação.",
      "Escorpião": "O Sol em Escorpião confere uma personalidade intensa, reservada e determinada. Há uma necessidade de profundidade emocional e transformação. Pessoas com Sol em Escorpião tendem a ser perspicazes, resilientes e possuem grande força interior.",
      "Sagitário": "O Sol em Sagitário revela uma personalidade otimista, aventureira e filosófica. Há uma necessidade de expansão e liberdade. Pessoas com Sol em Sagitário tendem a ser honestas, entusiasmadas e possuem uma visão ampla da vida.",
      "Capricórnio": "O Sol em Capricórnio indica uma personalidade ambiciosa, responsável e disciplinada. Há uma necessidade de realização e reconhecimento social. Pessoas com Sol em Capricórnio tendem a ser perseverantes, práticas e possuem grande capacidade de organização.",
      "Aquário": "O Sol em Aquário confere uma personalidade original, independente e humanitária. Há uma necessidade de inovação e liberdade de pensamento. Pessoas com Sol em Aquário tendem a ser progressistas, amigáveis e possuem uma visão única do mundo.",
      "Peixes": "O Sol em Peixes revela uma personalidade sensível, compassiva e intuitiva. Há uma necessidade de conexão espiritual e transcendência. Pessoas com Sol em Peixes tendem a ser imaginativas, empáticas e possuem uma rica vida interior."
    },
    "moon": {
      "Áries": "A Lua em Áries indica emoções intensas, diretas e impulsivas. Há uma necessidade emocional de ação e independência. Pessoas com Lua em Áries tendem a reagir rapidamente às situações e buscam liberdade emocional.",
      "Touro": "A Lua em Touro revela emoções estáveis, sensuais e práticas. Há uma necessidade emocional de segurança material e conforto. Pessoas com Lua em Touro tendem a buscar estabilidade e valorizam prazeres sensoriais.",
      "Gêmeos": "A Lua em Gêmeos indica emoções variáveis, curiosas e comunicativas. Há uma necessidade emocional de estímulo mental e interação social. Pessoas com Lua em Gêmeos tendem a processar sentimentos através da comunicação.",
      "Câncer": "A Lua em Câncer revela emoções profundas, protetoras e nostálgicas. Há uma forte necessidade emocional de segurança familiar e pertencimento. Pessoas com Lua em Câncer tendem a ser muito sensíveis e intuitivas.",
      "Leão": "A Lua em Leão indica emoções calorosas, dramáticas e expressivas. Há uma necessidade emocional de reconhecimento e admiração. Pessoas com Lua em Leão tendem a buscar atenção e expressam seus sentimentos de forma teatral.",
      "Virgem": "A Lua em Virgem revela emoções contidas, analíticas e preocupadas. Há uma necessidade emocional de ordem e utilidade. Pessoas com Lua em Virgem tendem a processar sentimentos através da análise e do serviço aos outros.",
      "Libra": "A Lua em Libra indica emoções harmoniosas, diplomáticas e dependentes de relacionamentos. Há uma necessidade emocional de equilíbrio e parceria. Pessoas com Lua em Libra tendem a buscar paz e evitar conflitos.",
      "Escorpião": "A Lua em Escorpião revela emoções intensas, profundas e transformadoras. Há uma necessidade emocional de intimidade e controle. Pessoas com Lua em Escorpião tendem a sentir tudo com grande intensidade e raramente esquecem.",
      "Sagitário": "A Lua em Sagitário indica emoções expansivas, otimistas e aventureiras. Há uma necessidade emocional de liberdade e significado. Pessoas com Lua em Sagitário tendem a buscar experiências emocionais estimulantes.",
      "Capricórnio": "A Lua em Capricórnio revela emoções controladas, responsáveis e ambiciosas. Há uma necessidade emocional de realização e estrutura. Pessoas com Lua em Capricórnio tendem a reprimir sentimentos em favor do dever.",
      "Aquário": "A Lua em Aquário indica emoções desapegadas, originais e humanitárias. Há uma necessidade emocional de liberdade e amizade. Pessoas com Lua em Aquário tendem a processar sentimentos de forma intelectual.",
      "Peixes": "A Lua em Peixes revela emoções fluidas, compassivas e impressionáveis. Há uma necessidade emocional de transcendência e união. Pessoas com Lua em Peixes tendem a absorver os sentimentos dos outros e buscar escape."
    },
    "ascendant": {
      "Áries": "O Ascendente em Áries confere uma aparência energética, direta e corajosa. A primeira impressão é de uma pessoa dinâmica, independente e assertiva. Há uma abordagem pioneira e impulsiva da vida, com iniciativa para começar novos projetos.",
      "Touro": "O Ascendente em Touro confere uma aparência estável, sensual e determinada. A primeira impressão é de uma pessoa confiável, prática e persistente. Há uma abordagem paciente e sensorial da vida, com valorização da segurança e do conforto.",
      "Gêmeos": "O Ascendente em Gêmeos confere uma aparência ágil, expressiva e jovial. A primeira impressão é de uma pessoa comunicativa, curiosa e versátil. Há uma abordagem adaptável e intelectual da vida, com interesse em diversas áreas.",
      "Câncer": "O Ascendente em Câncer confere uma aparência receptiva, sensível e protetora. A primeira impressão é de uma pessoa cuidadosa, emocional e reservada. Há uma abordagem intuitiva e defensiva da vida, com forte conexão com o lar e a família.",
      "Leão": "O Ascendente em Leão confere uma aparência marcante, confiante e calorosa. A primeira impressão é de uma pessoa carismática, orgulhosa e generosa. Há uma abordagem dramática e criativa da vida, com desejo de reconhecimento e expressão pessoal.",
      "Virgem": "O Ascendente em Virgem confere uma aparência discreta, precisa e observadora. A primeira impressão é de uma pessoa analítica, organizada e prestativa. Há uma abordagem meticulosa e prática da vida, com atenção aos detalhes e busca de aperfeiçoamento.",
      "Libra": "O Ascendente em Libra confere uma aparência harmoniosa, elegante e diplomática. A primeira impressão é de uma pessoa sociável, justa e refinada. Há uma abordagem equilibrada e cooperativa da vida, com valorização dos relacionamentos e da beleza.",
      "Escorpião": "O Ascendente em Escorpião confere uma aparência magnética, intensa e misteriosa. A primeira impressão é de uma pessoa reservada, perspicaz e determinada. Há uma abordagem profunda e estratégica da vida, com capacidade de transformação e regeneração.",
      "Sagitário": "O Ascendente em Sagitário confere uma aparência expansiva, otimista e aventureira. A primeira impressão é de uma pessoa sincera, entusiasta e filosófica. Há uma abordagem ampla e inspiradora da vida, com busca de significado e liberdade.",
      "Capricórnio": "O Ascendente em Capricórnio confere uma aparência séria, reservada e digna. A primeira impressão é de uma pessoa responsável, ambiciosa e disciplinada. Há uma abordagem estruturada e persistente da vida, com foco em metas de longo prazo.",
      "Aquário": "O Ascendente em Aquário confere uma aparência única, independente e intelectual. A primeira impressão é de uma pessoa original, amigável e progressista. Há uma abordagem inovadora e humanitária da vida, com valorização da liberdade e da individualidade.",
      "Peixes": "O Ascendente em Peixes confere uma aparência suave, etérea e receptiva. A primeira impressão é de uma pessoa sensível, compassiva e adaptável. Há uma abordagem intuitiva e fluida da vida, com capacidade de transcendência e empatia."
    }
  },
  "planets_in_houses": {
    "sun": {
      "1": "O Sol na primeira casa confere forte vitalidade e autoexpressão. A personalidade tende a ser marcante, com necessidade de se destacar e ser reconhecido. Há uma forte identificação com a aparência física e a maneira como se apresenta ao mundo.",
      "2": "O Sol na segunda casa indica que a identidade está fortemente ligada aos recursos materiais e valores pessoais. Há uma necessidade de segurança financeira e talentos para acumular bens. A autoestima está conectada à capacidade de gerar recursos.",
      "3": "O Sol na terceira casa revela uma personalidade comunicativa e intelectualmente curiosa. Há uma forte identificação com as habilidades mentais e de comunicação. A pessoa tende a se expressar através da fala, escrita e busca constante de conhecimento.",
      "4": "O Sol na quarta casa indica que a identidade está profundamente enraizada nas origens familiares e no lar. Há uma forte necessidade de segurança emocional e conexão com as raízes. A pessoa tende a brilhar no ambiente doméstico e familiar.",
      "5": "O Sol na quinta casa confere uma personalidade criativa, expressiva e dramática. Há uma forte necessidade de reconhecimento através da autoexpressão criativa. A pessoa tende a se destacar em atividades artísticas, recreativas ou relacionadas a crianças.",
      "6": "O Sol na sexta casa indica que a identidade está ligada ao trabalho, serviço e saúde. Há uma necessidade de ser útil e eficiente. A pessoa tende a brilhar através do aperfeiçoamento de habilidades práticas e da dedicação às responsabilidades cotidianas.",
      "7": "O Sol na sétima casa revela uma personalidade orientada para os relacionamentos e parcerias. Há uma forte identificação com o papel de parceiro. A pessoa tende a se realizar através da cooperação e do equilíbrio nas relações interpessoais.",
      "8": "O Sol na oitava casa indica uma personalidade profunda e transformadora. Há uma forte necessidade de experiências intensas e regeneradoras. A pessoa tende a brilhar em situações de crise, através da gestão de recursos compartilhados ou da exploração do oculto.",
      "9": "O Sol na nona casa confere uma personalidade expansiva, filosófica e aventureira. Há uma forte identificação com crenças e princípios elevados. A pessoa tende a se destacar através de viagens, estudos superiores ou busca de significado na vida.",
      "10": "O Sol na décima casa indica que a identidade está fortemente ligada à carreira e ao papel social. Há uma necessidade de reconhecimento público e realização profissional. A pessoa tende a brilhar em posições de autoridade e responsabilidade.",
      "11": "O Sol na décima primeira casa revela uma personalidade orientada para grupos e causas coletivas. Há uma forte identificação com ideais humanitários e amizades. A pessoa tende a se destacar em atividades grupais e na busca por inovação social.",
      "12": "O Sol na décima segunda casa indica uma personalidade reservada e espiritualizada. Há uma necessidade de transcendência e conexão com dimensões mais sutis. A pessoa tende a brilhar em atividades que envolvem compaixão, sacrifício ou trabalho nos bastidores."
    },
    "moon": {
      "1": "A Lua na primeira casa indica uma natureza emocional sensível e reativa. As emoções são expressas abertamente e a pessoa é fortemente influenciada pelo ambiente. Há uma necessidade emocional de ser reconhecido e aceito pelos outros.",
      "2": "A Lua na segunda casa revela uma conexão emocional com a segurança material. Há uma tendência a buscar conforto emocional através de posses e recursos. A pessoa pode experimentar flutuações nos recursos financeiros ligadas ao estado emocional.",
      "3": "A Lua na terceira casa indica uma mente intuitiva e emocional. Há uma necessidade de comunicar sentimentos e conectar-se com o ambiente imediato. A pessoa tende a processar emoções através da comunicação e da interação com irmãos ou vizinhos.",
      "4": "A Lua na quarta casa revela uma profunda conexão emocional com o lar e a família. Há uma forte necessidade de raízes e segurança emocional. A pessoa é fortemente influenciada pelas memórias da infância e pelo ambiente doméstico.",
      "5": "A Lua na quinta casa indica uma expressão emocional criativa e dramática. Há uma necessidade de dar e receber amor de forma demonstrativa. A pessoa tende a canalizar emoções através de atividades criativas, romances ou interações com crianças.",
      "6": "A Lua na sexta casa revela uma conexão emocional com o trabalho e a saúde. Há uma tendência a processar emoções através do serviço aos outros. A pessoa pode experimentar flutuações na saúde relacionadas ao estado emocional.",
      "7": "A Lua na sétima casa indica uma forte necessidade emocional de relacionamentos. Há uma tendência a buscar segurança emocional através de parcerias. A pessoa é sensível às necessidades dos outros e pode adaptar seu comportamento para agradar.",
      "8": "A Lua na oitava casa revela emoções intensas e profundas. Há uma necessidade de intimidade emocional e transformação. A pessoa tende a experimentar ciclos emocionais de morte e renascimento, com forte intuição para o oculto.",
      "9": "A Lua na nona casa indica uma conexão emocional com crenças e filosofias. Há uma necessidade de expandir horizontes emocionais através de viagens ou estudos. A pessoa tende a buscar significado emocional em experiências culturais diversas.",
      "10": "A Lua na décima casa revela uma conexão emocional com a carreira e o status social. Há uma necessidade de reconhecimento público e realização profissional. A pessoa pode ter uma figura materna influente ou assumir um papel maternal na sociedade.",
      "11": "A Lua na décima primeira casa indica uma conexão emocional com grupos e amizades. Há uma necessidade de pertencer a uma comunidade que compartilha ideais. A pessoa tende a processar emoções através de interações sociais e causas coletivas.",
      "12": "A Lua na décima segunda casa revela uma natureza emocional profunda e intuitiva. Há uma conexão com o inconsciente coletivo e dimensões espirituais. A pessoa pode experimentar períodos de isolamento emocional e necessidade de recolhimento."
    }
  },
  "aspects": {
    "sun_conjunct_moon": "A conjunção entre Sol e Lua indica uma forte integração entre a consciência e as emoções. Há harmonia entre os princípios masculino e feminino internos, resultando em uma personalidade coesa e autoconfiante.",
    "sun_square_moon": "A quadratura entre Sol e Lua indica tensão entre a vontade consciente e as necessidades emocionais. Pode haver conflito interno entre o que se deseja fazer e o que se sente, resultando em períodos de indecisão ou mudanças de humor.",
    "sun_trine_moon": "O trígono entre Sol e Lua indica fluidez entre a vontade consciente e as emoções. Há facilidade em integrar razão e sentimento, resultando em uma personalidade equilibrada e criativa.",
    "sun_opposition_moon": "A oposição entre Sol e Lua indica polarização entre a consciência e as emoções. Pode haver projeção de aspectos da personalidade nos outros, especialmente em relacionamentos próximos, resultando em dinâmicas de dependência.",
    "sun_conjunct_mercury": "A conjunção entre Sol e Mercúrio indica uma forte identificação com o intelecto e a comunicação. O pensamento tende a ser claro e focado, com habilidade para expressar a individualidade através das palavras.",
    "sun_square_mercury": "A quadratura entre Sol e Mercúrio indica tensão entre a vontade e o intelecto. Pode haver dificuldade em comunicar claramente as intenções ou tendência a mudar frequentemente de opinião.",
    "sun_trine_mercury": "O trígono entre Sol e Mercúrio indica fluidez entre a vontade e o intelecto. Há facilidade em expressar ideias e opiniões, com clareza mental e capacidade de liderança intelectual.",
    "sun_opposition_mercury": "A oposição entre Sol e Mercúrio indica polarização entre a vontade e o intelecto. Pode haver tendência a intelectualizar demais as emoções ou dificuldade em integrar diferentes perspectivas.",
    "moon_conjunct_mercury": "A conjunção entre Lua e Mercúrio indica uma forte conexão entre emoções e intelecto. O pensamento é influenciado pelas emoções, resultando em comunicação expressiva e intuitiva.",
    "moon_square_mercury": "A quadratura entre Lua e Mercúrio indica tensão entre emoções e pensamento. Pode haver dificuldade em expressar sentimentos verbalmente ou tendência a racionalizar demais as emoções.",
    "moon_trine_mercury": "O trígono entre Lua e Mercúrio indica fluidez entre emoções e intelecto. Há facilidade em comunicar sentimentos e intuições, com sensibilidade para captar nuances emocionais nas palavras.",
    "moon_opposition_mercury": "A oposição entre Lua e Mercúrio indica polarização entre emoções e pensamento. Pode haver oscilação entre responder emocionalmente ou intelectualmente às situações, com desafios na comunicação emocional."
  },
  "transits": {
    "sun_conjunct_natal_sun": "Trânsito do Sol em conjunção com o Sol natal marca o 'aniversário solar', um período de renovação da vitalidade e propósito. É um momento favorável para novos começos e para reafirmar objetivos pessoais.",
    "sun_square_natal_sun": "Trânsito do Sol em quadratura com o Sol natal representa um ponto de tensão no ciclo anual. É um momento para revisar objetivos e fazer ajustes necessários, enfrentando obstáculos que impedem o progresso.",
    "sun_trine_natal_sun": "Trânsito do Sol em trígono com o Sol natal traz um fluxo harmonioso de energia e oportunidades. É um período favorável para avançar em projetos pessoais e receber reconhecimento por esforços anteriores.",
    "sun_opposition_natal_sun": "Trânsito do Sol em oposição ao Sol natal marca um ponto de culminação no ciclo anual. É um momento para avaliar o progresso feito nos últimos seis meses e ajustar o curso para os próximos seis.",
    "jupiter_conjunct_natal_sun": "Trânsito de Júpiter em conjunção com o Sol natal traz expansão, otimismo e oportunidades de crescimento. É um período favorável para novos empreendimentos, viagens e estudos superiores.",
    "jupiter_square_natal_sun": "Trânsito de Júpiter em quadratura com o Sol natal traz excessos e tendência à superestimação das capacidades. É importante manter o equilíbrio e não assumir mais compromissos do que pode cumprir.",
    "jupiter_trine_natal_sun": "Trânsito de Júpiter em trígono com o Sol natal traz fluxo harmonioso de oportunidades e crescimento. É um período favorável para expandir horizontes, com sorte e apoio de figuras de autoridade.",
    "jupiter_opposition_natal_sun": "Trânsito de Júpiter em oposição ao Sol natal traz culminação de projetos iniciados anteriormente. Pode haver tensão entre aspirações pessoais e expectativas sociais, exigindo equilíbrio.",
    "saturn_conjunct_natal_sun": "Trânsito de Saturno em conjunção com o Sol natal marca um período de responsabilidade aumentada e possíveis limitações. É um momento para consolidar a identidade através de trabalho árduo e disciplina.",
    "saturn_square_natal_sun": "Trânsito de Saturno em quadratura com o Sol natal traz obstáculos e testes à vontade pessoal. É um período para enfrentar limitações e desenvolver perseverança diante de desafios estruturais.",
    "saturn_trine_natal_sun": "Trânsito de Saturno em trígono com o Sol natal traz estabilidade e reconhecimento por esforços consistentes. É um período favorável para estabelecer fundações sólidas e assumir responsabilidades de longo prazo.",
    "saturn_opposition_natal_sun": "Trânsito de Saturno em oposição ao Sol natal marca um ponto de avaliação das estruturas de vida. Pode haver confronto com autoridades ou necessidade de equilibrar responsabilidades pessoais e profissionais."
  }
}
```

## 2. Criação do Serviço de Interpretação

Agora, vamos criar um serviço para acessar e fornecer as interpretações:

```python
# Em app/services/interpretation_service.py
import json
import os
from typing import Dict, Any, Optional

class InterpretationService:
    """Serviço para fornecer interpretações astrológicas textuais."""
    
    def __init__(self):
        """Inicializa o serviço carregando o arquivo de interpretações."""
        file_path = os.path.join(os.path.dirname(__file__), '../data/interpretations.json')
        with open(file_path, 'r', encoding='utf-8') as f:
            self.interpretations = json.load(f)
    
    def get_planet_in_sign_interpretation(self, planet: str, sign: str) -> str:
        """Retorna a interpretação para um planeta em um signo."""
        try:
            return self.interpretations["planets_in_signs"][planet.lower()][sign]
        except KeyError:
            return f"Interpretação não disponível para {planet} em {sign}."
    
    def get_planet_in_house_interpretation(self, planet: str, house: int) -> str:
        """Retorna a interpretação para um planeta em uma casa."""
        try:
            house_str = str(house)
            return self.interpretations["planets_in_houses"][planet.lower()][house_str]
        except KeyError:
            return f"Interpretação não disponível para {planet} na casa {house}."
    
    def get_aspect_interpretation(self, planet1: str, aspect: str, planet2: str) -> str:
        """Retorna a interpretação para um aspecto entre dois planetas."""
        try:
            aspect_key = f"{planet1.lower()}_{aspect.lower()}_{planet2.lower()}"
            return self.interpretations["aspects"][aspect_key]
        except KeyError:
            # Tentar com os planetas invertidos
            try:
                aspect_key = f"{planet2.lower()}_{aspect.lower()}_{planet1.lower()}"
                return self.interpretations["aspects"][aspect_key]
            except KeyError:
                return f"Interpretação não disponível para {planet1} {aspect} {planet2}."
    
    def get_transit_interpretation(self, transit_planet: str, aspect: str, natal_planet: str) -> str:
        """Retorna a interpretação para um trânsito."""
        try:
            transit_key = f"{transit_planet.lower()}_{aspect.lower()}_natal_{natal_planet.lower()}"
            return self.interpretations["transits"][transit_key]
        except KeyError:
            return f"Interpretação não disponível para {transit_planet} {aspect} {natal_planet} natal."
    
    def generate_natal_chart_interpretation(self, natal_chart_data: Dict[str, Any]) -> Dict[str, str]:
        """Gera interpretações para um mapa natal."""
        interpretations = {}
        
        # Interpretação do Sol no signo
        if "planets" in natal_chart_data and "sun" in natal_chart_data["planets"]:
            sun_data = natal_chart_data["planets"]["sun"]
            if sun_data and "sign" in sun_data:
                interpretations["sun_sign"] = self.get_planet_in_sign_interpretation("sun", sun_data["sign"])
        
        # Interpretação da Lua no signo
        if "planets" in natal_chart_data and "moon" in natal_chart_data["planets"]:
            moon_data = natal_chart_data["planets"]["moon"]
            if moon_data and "sign" in moon_data:
                interpretations["moon_sign"] = self.get_planet_in_sign_interpretation("moon", moon_data["sign"])
        
        # Interpretação do Ascendente
        if "ascendant" in natal_chart_data and "sign" in natal_chart_data["ascendant"]:
            interpretations["ascendant"] = self.get_planet_in_sign_interpretation("ascendant", natal_chart_data["ascendant"]["sign"])
        
        # Interpretações de planetas nas casas
        if "planets" in natal_chart_data:
            house_interpretations = {}
            for planet_key, planet_data in natal_chart_data["planets"].items():
                if planet_data and "house" in planet_data:
                    house_interpretations[planet_key] = self.get_planet_in_house_interpretation(
                        planet_key, planet_data["house"]
                    )
            interpretations["planets_in_houses"] = house_interpretations
        
        # Interpretações de aspectos
        if "aspects" in natal_chart_data:
            aspect_interpretations = {}
            for aspect in natal_chart_data["aspects"]:
                if "p1_name" in aspect and "aspect" in aspect and "p2_name" in aspect:
                    aspect_key = f"{aspect['p1_name']}_{aspect['aspect']}_{aspect['p2_name']}"
                    aspect_interpretations[aspect_key] = self.get_aspect_interpretation(
                        aspect["p1_name"], aspect["aspect"], aspect["p2_name"]
                    )
            interpretations["aspects"] = aspect_interpretations
        
        return interpretations
    
    def generate_transit_interpretation(self, transits_data: Dict[str, Any]) -> Dict[str, str]:
        """Gera interpretações para trânsitos."""
        interpretations = {}
        
        # Interpretações de aspectos de trânsito
        if "aspects" in transits_data:
            transit_interpretations = {}
            for aspect in transits_data["aspects"]:
                if "p1_name" in aspect and "aspect" in aspect and "p2_name" in aspect:
                    # Verificar se é um aspecto de trânsito para natal
                    if aspect["p1_owner"] == "Trânsito" and aspect["p2_owner"] == "Natal":
                        aspect_key = f"{aspect['p1_name']}_{aspect['aspect']}_{aspect['p2_name']}"
                        transit_interpretations[aspect_key] = self.get_transit_interpretation(
                            aspect["p1_name"], aspect["aspect"], aspect["p2_name"]
                        )
            interpretations["transit_aspects"] = transit_interpretations
        
        return interpretations
```

## 3. Criação do Router para Interpretações

Vamos criar um novo router para fornecer interpretações:

```python
# Em app/routers/interpretation_router.py
from fastapi import APIRouter, HTTPException
from app.models import NatalChartRequest, TransitsToNatalRequest
from app.services.interpretation_service import InterpretationService
from typing import Dict, Any

router = APIRouter(prefix="/api/v1", tags=["interpretations"])
interpretation_service = InterpretationService()

@router.post("/interpret_natal_chart", response_model=Dict[str, Any])
async def interpret_natal_chart(natal_chart_data: Dict[str, Any]):
    """Gera interpretações textuais para um mapa natal."""
    try:
        interpretations = interpretation_service.generate_natal_chart_interpretation(natal_chart_data)
        return {"interpretations": interpretations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar interpretações: {str(e)}")

@router.post("/interpret_transits", response_model=Dict[str, Any])
async def interpret_transits(transits_data: Dict[str, Any]):
    """Gera interpretações textuais para trânsitos."""
    try:
        interpretations = interpretation_service.generate_transit_interpretation(transits_data)
        return {"interpretations": interpretations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar interpretações: {str(e)}")

@router.get("/interpretation/{category}/{element}/{position}", response_model=Dict[str, str])
async def get_specific_interpretation(
    category: str,
    element: str,
    position: str
):
    """
    Retorna uma interpretação específica.
    
    - category: Categoria da interpretação (planet_sign, planet_house, aspect, transit)
    - element: Elemento astrológico (sun, moon, mercury, etc.)
    - position: Posição (signo, casa, aspecto)
    """
    try:
        if category == "planet_sign":
            interpretation = interpretation_service.get_planet_in_sign_interpretation(element, position)
        elif category == "planet_house":
            interpretation = interpretation_service.get_planet_in_house_interpretation(element, int(position))
        elif category == "aspect":
            # Formato esperado: planet1/aspect/planet2
            parts = position.split("/")
            if len(parts) != 3:
                raise ValueError("Formato inválido para aspecto. Use: planet1/aspect/planet2")
            interpretation = interpretation_service.get_aspect_interpretation(parts[0], parts[1], parts[2])
        elif category == "transit":
            # Formato esperado: transit_planet/aspect/natal_planet
            parts = position.split("/")
            if len(parts) != 3:
                raise ValueError("Formato inválido para trânsito. Use: transit_planet/aspect/natal_planet")
            interpretation = interpretation_service.get_transit_interpretation(parts[0], parts[1], parts[2])
        else:
            raise ValueError(f"Categoria desconhecida: {category}")
        
        return {"interpretation": interpretation}
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Interpretação não encontrada: {str(e)}")
```

## 4. Atualização dos Routers Existentes para Incluir Interpretações

Vamos modificar os routers existentes para opcionalmente incluir interpretações:

```python
# Em app/routers/natal_chart_router.py
from app.services.interpretation_service import InterpretationService

# Inicializar o serviço de interpretação
interpretation_service = InterpretationService()

@router.post("/natal_chart", response_model=NatalChartResponse)
async def calculate_natal_chart(data: NatalChartRequest):
    try:
        # Código existente para calcular o mapa natal...
        
        # Adicionar interpretações se solicitado
        if data.include_interpretations:
            response["interpretations"] = interpretation_service.generate_natal_chart_interpretation(response)
        
        return response
    except Exception as e:
        # Tratamento de erro existente...
```

```python
# Em app/routers/transit_router.py
from app.services.interpretation_service import InterpretationService

# Inicializar o serviço de interpretação
interpretation_service = InterpretationService()

@router.post("/transits_to_natal", response_model=TransitsToNatalResponse)
async def calculate_transits_to_natal(data: TransitsToNatalRequest):
    try:
        # Código existente para calcular os trânsitos...
        
        # Adicionar interpretações se solicitado
        if data.include_interpretations:
            response["interpretations"] = interpretation_service.generate_transit_interpretation(response)
        
        return response
    except Exception as e:
        # Tratamento de erro existente...
```

## 5. Atualização dos Modelos de Requisição

Vamos atualizar os modelos de requisição para incluir a opção de interpretações:

```python
# Em models.py
class NatalChartRequest(BaseModel):
    # Campos existentes...
    include_interpretations: bool = Field(default=False, description="Se deve incluir interpretações textuais na resposta")

class TransitRequest(BaseModel):
    # Campos existentes...
    include_interpretations: bool = Field(default=False, description="Se deve incluir interpretações textuais na resposta")

class TransitsToNatalRequest(BaseModel):
    natal: NatalChartRequest
    transit: TransitRequest
    include_interpretations: bool = Field(default=False, description="Se deve incluir interpretações textuais na resposta")
```

## 6. Atualização do Arquivo Principal

Vamos atualizar o arquivo principal para incluir o novo router:

```python
# Em main.py
from fastapi import FastAPI
from app.routers import natal_chart_router, transit_router, svg_chart_router, interpretation_router
import uvicorn

app = FastAPI(
    title="API de Astrologia",
    description="""
    API para cálculos astrológicos, incluindo mapas natais, trânsitos, aspectos, geração de gráficos SVG e interpretações textuais.
    
    ## Sistemas de Casas Suportados
    
    A API suporta os seguintes sistemas de casas:
    
    - **Placidus** (padrão): Sistema mais comum, baseado na divisão do tempo que leva para um ponto da eclíptica passar do horizonte ao meio-céu.
    - **Koch**: Baseado na divisão do tempo que leva para um ponto da eclíptica passar do horizonte ao meridiano.
    - **Porphyrius**: Sistema antigo que divide o espaço entre os quatro ângulos.
    - **Regiomontanus**: Baseado na divisão do equador celeste.
    - **Campanus**: Baseado na divisão do primeiro vertical.
    - **Equal**: Casas de tamanho igual (30°) a partir do Ascendente.
    - **Whole Sign**: Cada casa corresponde a um signo inteiro.
    - **Alcabitus**: Sistema medieval baseado na divisão do equador celeste.
    - **Morinus**: Sistema que ignora a rotação da Terra.
    - **Horizontal**: Baseado no horizonte local.
    - **Topocentric**: Variação do sistema Placidus.
    - **Vehlow**: Variação do sistema Equal com deslocamento de 5°.
    
    ## Suporte a Idiomas
    
    A API suporta os seguintes idiomas:
    
    - **Inglês (en)**: Nomes de signos, planetas e aspectos em inglês.
    - **Português (pt)** (padrão): Nomes de signos, planetas e aspectos traduzidos para português.
    
    ## Interpretações Textuais
    
    A API fornece interpretações textuais básicas para:
    
    - Planetas em signos
    - Planetas em casas
    - Aspectos entre planetas
    - Trânsitos planetários
    
    Para incluir interpretações nas respostas, defina o parâmetro `include_interpretations` como `true`.
    """,
    version="1.0.0"
)

app.include_router(natal_chart_router.router)
app.include_router(transit_router.router)
app.include_router(svg_chart_router.router)
app.include_router(interpretation_router.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## 7. Testes e Validação

Para testar a implementação, vamos criar um script que faz requisições e verifica as interpretações:

```python
# Em tests/test_interpretations.py
import requests
import json

def test_interpretations():
    # Dados de teste
    data = {
        "name": "Albert Einstein",
        "year": 1879,
        "month": 3,
        "day": 14,
        "hour": 11,
        "minute": 30,
        "longitude": 10.0,
        "latitude": 48.4,
        "tz_str": "Europe/Berlin",
        "house_system": "Placidus",
        "include_interpretations": True
    }
    
    # Testar mapa natal com interpretações
    response = requests.post("http://localhost:8000/api/v1/natal_chart", json=data)
    
    assert response.status_code == 200
    result = response.json()
    
    # Verificar se há interpretações na resposta
    assert "interpretations" in result
    
    # Verificar interpretações específicas
    interpretations = result["interpretations"]
    assert "sun_sign" in interpretations
    assert "moon_sign" in interpretations
    assert "ascendant" in interpretations
    
    print("Interpretação do Sol no signo:")
    print(interpretations["sun_sign"])
    print("\nInterpretação da Lua no signo:")
    print(interpretations["moon_sign"])
    print("\nInterpretação do Ascendente:")
    print(interpretations["ascendant"])
    
    # Testar endpoint específico de interpretação
    sun_sign = result["planets"]["sun"]["sign"]
    response = requests.get(f"http://localhost:8000/api/v1/interpretation/planet_sign/sun/{sun_sign}")
    
    assert response.status_code == 200
    interpretation_result = response.json()
    
    assert "interpretation" in interpretation_result
    assert interpretation_result["interpretation"] == interpretations["sun_sign"]
    
    # Testar trânsitos com interpretações
    transit_data = {
        "natal": data,
        "transit": {
            "year": 2025,
            "month": 5,
            "day": 28,
            "hour": 12,
            "minute": 0,
            "longitude": 10.0,
            "latitude": 48.4,
            "tz_str": "Europe/Berlin",
            "house_system": "Placidus"
        },
        "include_interpretations": True
    }
    
    response = requests.post("http://localhost:8000/api/v1/transits_to_natal", json=transit_data)
    
    assert response.status_code == 200
    transit_result = response.json()
    
    # Verificar se há interpretações na resposta
    assert "interpretations" in transit_result
    
    # Imprimir algumas interpretações de trânsito
    if "transit_aspects" in transit_result["interpretations"]:
        print("\nInterpretações de trânsitos:")
        for aspect_key, interpretation in list(transit_result["interpretations"]["transit_aspects"].items())[:3]:
            print(f"\n{aspect_key}:")
            print(interpretation)
    
    print("\nTeste concluído com sucesso!")

if __name__ == "__main__":
    test_interpretations()
```

## 8. Considerações Adicionais

1. **Extensibilidade**: A estrutura proposta permite adicionar facilmente mais interpretações no futuro, expandindo o arquivo JSON ou conectando a uma base de dados mais robusta.

2. **Personalização**: Considerar permitir que os usuários forneçam suas próprias interpretações ou escolham entre diferentes estilos de interpretação.

3. **Profundidade**: As interpretações básicas podem ser expandidas para incluir análises mais detalhadas, como combinações de planetas em signos e casas, ou interpretações de padrões planetários (como T-quadrados, Grandes Trígonos, etc.).

4. **Caching**: Implementar cache para interpretações frequentemente solicitadas para melhorar o desempenho.

5. **Internacionalização**: Expandir o suporte para múltiplos idiomas nas interpretações.

Esta implementação fornece uma base sólida para a inclusão de interpretações textuais básicas na API, com uma estrutura flexível que pode ser facilmente expandida no futuro. As interpretações são opcionais, permitindo que os usuários escolham se desejam incluí-las nas respostas, e estão disponíveis tanto integradas nas respostas principais quanto através de endpoints específicos.
