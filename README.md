# Comparando Mapas de Cores para Visualização Científica

Este repositório contém um projeto de visualização de dados que compara o tradicional mapa de cores "rainbow" com três mapas de cores cientificamente derivados: **batlow**, **lapaz** e **bamako**.

## 📋 Objetivo

O objetivo deste projeto é demonstrar como diferentes escolhas de mapas de cores podem impactar significativamente a interpretação e compreensão dos dados em visualizações científicas. A comparação destaca os problemas do amplamente utilizado mapa rainbow e apresenta alternativas cientificamente fundamentadas que oferecem melhor uniformidade perceptual e acessibilidade.

## 🧪 Fundamentação Teórica

Este trabalho se baseia em conceitos apresentados nos artigos:

- "Using Colour to Communicate" de Ed Hawkins
- "The misuse of colour in science communication" (Crameri, F., Shephard, G.E. & Heron, P.J. Nature Communications 11, 5444, 2020)

## 📊 Dados Utilizados

O projeto utiliza três conjuntos de dados relacionados ao desenvolvimento humano global:

- `human-development-index.csv`: Índice de Desenvolvimento Humano (IDH) global
- `happiness-cantril-ladder.csv`: Índice de felicidade (Cantril ladder score)
- `life-expectancy.csv`: Expectativa de vida global

Todos os dados foram obtidos do repositório [Our World in Data](https://ourworldindata.org/).

## 📁 Estrutura do Repositório

- `color_map_extended.py`: Script Python principal que gera as visualizações
- `human-development-index.csv`: Dados do IDH global
- `happiness-cantril-ladder.csv`: Dados de felicidade global
- `life-expectancy.csv`: Dados de expectativa de vida global
- `outputs/`: Diretório contendo as visualizações geradas
  - `all_gradients_comparison.png`: Comparação dos gradientes de cores
  - `all_barplots_comparison.png`: Comparação de gráficos de barras
  - `all_scatter_comparison.png`: Comparação de gráficos de dispersão
  - `all_heatmap_comparison.png`: Comparação de mapas de calor
  - `all_grayscale_comparison.png`: Simulação de conversão para escala de cinza
  - `expanded_color_map_analysis.txt`: Análise textual detalhada dos mapas de cores

## 🔍 Visualizações Geradas

O script gera cinco tipos diferentes de visualizações para comparar os mapas de cores:

1. **Comparação de Gradientes**: Demonstra como cada mapa de cores representa um gradiente contínuo de valores.
2. **Gráficos de Barras**: Mostra o IDH dos 20 países com maior desenvolvimento usando cada mapa de cores.
3. **Gráficos de Dispersão**: Relaciona IDH e expectativa de vida com cada mapa de cores.
4. **Mapas de Calor**: Visualiza correlações usando cada mapa de cores.
5. **Simulação em Escala de Cinza**: Demonstra como cada mapa de cores é percebido quando convertido para escala de cinza, simulando a percepção de pessoas com deficiência na percepção de cores.

## 💻 Como Executar o Código

### Pré-requisitos

- Python 3.6 ou superior
- Bibliotecas Python: pandas, matplotlib, numpy, seaborn, cmocean, colorcet, cmcrameri

### Instalação das Dependências

```bash
pip install pandas matplotlib numpy seaborn cmocean colorcet cmcrameri
```

### Execução

```bash
python color_map_extended.py
```

Este comando irá:

1. Carregar os conjuntos de dados
2. Gerar as cinco visualizações comparativas
3. Salvar as visualizações no diretório `outputs/`
4. Criar um arquivo de análise textual `expanded_color_map_analysis.txt`

## 📝 Conclusões Principais

As visualizações demonstram claramente que:

1. O mapa de cores rainbow apresenta problemas significativos:

   - Distorções na percepção de variações de dados
   - Criação de fronteiras artificiais em dados contínuos
   - Ordenação não intuitiva
   - Problemas graves de acessibilidade
2. Os mapas de cores cientificamente derivados (batlow, lapaz e bamako) oferecem vantagens consideráveis:

   - Uniformidade perceptual
   - Melhor acessibilidade para pessoas com deficiência na percepção de cores
   - Ordem intuitiva através de gradientes de luminosidade consistentes
   - Representação mais fiel dos dados sem criar padrões artificiais

## 🔗 Referências

1. Crameri, F., Shephard, G.E. & Heron, P.J. The misuse of colour in science communication. Nat Commun 11, 5444 (2020). https://doi.org/10.1038/s41467-020-19160-7
2. Hawkins, E. "Using Colour to Communicate" https://www.climate-lab-book.ac.uk/2016/why-rainbow-colour-scales-can-be-misleading/
3. Our World in Data. Human Development Index (https://ourworldindata.org/grapher/human-development-index)
4. Our World in Data. Life expectancy at birth (https://ourworldindata.org/grapher/life-expectancy)
5. Our World in Data. Self-reported life satisfaction (https://ourworldindata.org/grapher/happiness-cantril-ladder)

## 📄 Licença

Este projeto é disponibilizado sob a licença [MIT](LICENSE). 
