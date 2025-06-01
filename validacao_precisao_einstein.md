## Validação de Precisão Astrológica: Albert Einstein

Este documento registra a validação da precisão dos cálculos astrológicos da API, utilizando como referência os dados de Albert Einstein obtidos no Astro-Databank (astro.com).

**Dados de Referência (Astro-Databank):**

*   **Nome:** Albert Einstein
*   **Data de Nascimento:** 14 de Março de 1879
*   **Hora:** 11:30 AM (LMT - Local Mean Time)
*   **Local:** Ulm, Alemanha
*   **Coordenadas:** 48n24 (Latitude 48.40 N), 10e0 (Longitude 10.0 E - astro.com indica 10e0, que é 10.0. A página do Astro-Databank mostra 48n24, 10e0. O Kerykeion espera decimais, então usaremos 48.40 e 10.0)
*   **Fuso Horário (Timezone):** LMT m10e0. Isso significa que o LMT é GMT +0h 40m (10 graus Leste * 4 minutos/grau = 40 minutos). Para Kerykeion, precisamos de um timezone string válido como `Europe/Berlin` ou um offset UTC. Ulm está na Alemanha, que usa CET/CEST. Em 1879, a Alemanha ainda não tinha padronizado o fuso horário. O LMT é o mais preciso aqui. Kerykeion pode lidar com LMT se o `tz_str` for construído corretamente ou se pudermos calcular o offset UTC. O offset LMT para 10E é +00:40. Kerykeion pode precisar de `tz_str` como `+00:40` ou um nome de fuso que resolva para isso historicamente (o que pode ser complexo).
    *   **Sol:** Peixes 23°30'
    *   **Lua:** Sagitário 14°32'
    *   **Ascendente (Asc):** Câncer 11°39'
    *   **Meio do Céu (MC):** Peixes (grau não explicitamente listado na imagem inicial, mas geralmente calculado)

**Dados para a API (convertidos/preparados):**

*   **name:** "Albert Einstein"
*   **year:** 1879
*   **month:** 3
*   **day:** 14
*   **hour:** 11
*   **minute:** 30
*   **longitude:** 10.0
*   **latitude:** 48.40
*   **tz_str:** "+00:40" (Este é o desafio, Kerykeion pode não aceitar este formato diretamente. Se não funcionar, tentaremos `Europe/Berlin` e ajustaremos a hora para UTC se necessário, ou buscaremos como Kerykeion lida com LMT. A documentação do Kerykeion sugere que ele usa a biblioteca `pytz`, que pode lidar com `Europe/Berlin`. A hora LMT 11:30 para 10E significa que o tempo solar local era 11:30. O tempo padrão da Alemanha (CET, GMT+1) só foi introduzido em 1893. Antes disso, LMT era comum. Se usarmos `Europe/Berlin`, teremos que verificar se Kerykeion/pytz lida corretamente com a data histórica ou se precisamos ajustar a hora de entrada para UTC. Para LMT 11:30 a 10E (GMT+0:40), o UTC seria 11:30 - 0:40 = 10:50 UTC.)
    *   Vamos tentar primeiro com `tz_str="Europe/Berlin"` e hora 11:30, e depois com hora UTC 10:50 e `tz_str="UTC"` se os resultados divergirem muito.
*   **house_system:** "Placidus"

**Resultados Esperados (Astro-Databank - posições principais):**

*   Sol: 23° Peixes 30'
*   Lua: 14° Sagitário 32'
*   Ascendente: 11° Câncer 39'

**Requisição à API (Exemplo com cURL):**

```bash
# (Será preenchido após a execução)
```

**Resultados da API:**

*   **(Será preenchido após a execução)**

**Comparação e Análise:**

*   **(Será preenchido após a execução)**

