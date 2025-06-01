# Active Context: Astrologia API

## Current Work Focus

O foco atual é na finalização da integração das funcionalidades avançadas da API de Astrologia. Já consolidamos as três versões (original, V2 e V3) em uma implementação unificada com estrutura clara e modular. Implementamos novas funcionalidades como sinastria e progressões secundárias, melhoramos o sistema de traduções para suportar múltiplos idiomas, e criamos um sistema avançado de busca textual para substituir o RAG temporariamente. A API agora oferece uma solução completa para cálculos astrológicos, visualizações SVG e interpretações textuais.

## Recent Changes

- Corrigimos problemas de importação de dependências (fastapi, kerykeion, python-dotenv, pydantic) através da atualização do requirements.txt e instalação correta dos pacotes.
- Resolvemos problemas de indentação e estrutura no arquivo text_search.py, melhorando a legibilidade e manutenibilidade do código.
- Implementamos um sistema de busca textual avançado usando TF-IDF para substituir temporariamente o RAG, permitindo encontrar interpretações relevantes nos textos astrológicos.
- Expandimos e otimizamos o suporte a idiomas para incluir português, inglês, espanhol, francês, italiano e alemão, com melhor tratamento de traduções.
- Consolidamos a estrutura de traduções com funções translate_sign e translate_aspect para maior consistência.
- Corrigimos e padronizamos o uso de funções de tradução em toda a API.
- Desenvolvemos um novo endpoint para sinastria (comparação de mapas natais) com cálculo de aspectos entre os planetas de dois mapas.
- Implementamos um endpoint para progressões secundárias, uma técnica preditiva importante na astrologia.
- Atualizamos a documentação para refletir todas as novas funcionalidades e melhorias.
- Criamos testes automatizados para validar todas as funcionalidades principais da API.
- Organizamos os textos processados em uma estrutura padronizada para facilitar a busca.

## Next Steps

1. Expandir o conjunto de testes para cobrir mais casos de borda e cenários de erro.
2. Implementar funcionalidades adicionais como retornos solares e lunares.
3. Melhorar a documentação com exemplos mais detalhados e casos de uso.
4. Explorar otimizações de desempenho, especialmente para a geração de SVG e busca textual.
5. Adicionar mais textos processados para enriquecer as interpretações.
6. Implementar cache para cálculos astrológicos frequentes.
7. Refinar o sistema de busca textual com técnicas mais avançadas como busca semântica.
8. Adicionar mais opções de personalização para os gráficos SVG.
9. Desenvolver uma interface de usuário web simples para demonstrar as capacidades da API.
10. Preparar a documentação para deployment em produção.

## Active Decisions and Considerations

- Decidimos usar um sistema de busca TF-IDF para interpretações textuais, em vez do RAG completo, devido a limitações de recursos. Isso proporciona um bom equilíbrio entre relevância e desempenho.
- Implementamos sinastria e progressões como funcionalidades separadas com seus próprios endpoints, seguindo o padrão estabelecido para mapas natais e trânsitos.
- Ampliamos o suporte a idiomas além do português e inglês originais, garantindo que todas as funções de tradução sejam robustas e flexíveis.
- Mantivemos a compatibilidade com as versões anteriores da API, preservando o formato das respostas e parâmetros de requisição existentes.
- Adotamos uma abordagem modular para facilitar a adição de novas funcionalidades no futuro.
- Priorizamos a validação adequada de entradas e tratamento de erros para melhorar a robustez da API.
- Organizamos os textos interpretados em uma estrutura que facilita a busca e tradução.
- Projetamos o sistema de cache para ser transparente para o usuário, melhorando o desempenho sem alterar a interface da API.
## Important Patterns and Preferences

- Manter uma clara separação de preocupações com módulos distintos para endpoints de API, cálculos astrológicos, traduções e interpretações.
- Usar modelos Pydantic para validação de requisições e respostas.
- Fornecer tanto dados astrológicos brutos quanto resultados interpretados para acomodar diferentes necessidades de cliente.
- Preservar termos em inglês originais ao lado de traduções para compatibilidade.
- Usar FastAPI como framework principal devido à sua velocidade, tipagem e documentação automática.
- Utilizar a biblioteca Kerykeion para cálculos astrológicos e geração de SVG.
- Seguir princípios RESTful para o design da API.
- Implementar validação de entrada robusta para garantir cálculos precisos.
- Adotar uma abordagem modular para permitir expansão fácil com novos recursos.


## Learnings and Project Insights

- A Astrologia API é um sistema robusto para cálculos astrológicos, oferecendo uma ampla gama de funcionalidades.
- A implementação V2 introduz várias melhorias e extensões, como personalização do sistema de casas, traduções, interpretações e geração de gráficos SVG.
- A arquitetura em camadas e os princípios de design RESTful são bem mantidos.
- Kerykeion fornece uma base sólida para cálculos astrológicos, mas requer alguma adaptação para um contexto de API RESTful.
- O tratamento cuidadoso de data, hora, localização e fusos horários é crucial para resultados astrológicos precisos.
- A implementação do sistema RAG requer recursos significativos e pode precisar ser abordada em estágios.
- A V3 fez progresso na criação de um índice vetorial FAISS para busca semântica, mas foi pausada devido a limitações de recursos.
- A estrutura do projeto é bem organizada, com separação clara de responsabilidades.
- O projeto inclui uma extensa coleção de livros de astrologia que foram parcialmente processados para uso com o sistema RAG.
- O projeto utiliza FastAPI e Kerykeion como principais tecnologias, com Pydantic para validação de dados.
