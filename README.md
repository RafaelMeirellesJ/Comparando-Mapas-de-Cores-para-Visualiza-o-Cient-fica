# Comparando Mapas de Cores para Visualização Científica

## 📋 Sobre o Projeto

Este trabalho foi desenvolvido como parte de uma atividade acadêmica sobre visualização de dados científicos, com o objetivo de analisar como diferentes escolhas de mapas de cores podem impactar significativamente a interpretação e compreensão dos dados.

## 🎯 Objetivos e Motivação

A escolha adequada de mapas de cores é um aspecto frequentemente negligenciado na visualização científica, apesar de seu impacto significativo na interpretação dos dados. Este projeto tem como objetivos:

- Demonstrar os problemas do tradicional mapa "rainbow" em contextos científicos
- Comparar sua eficácia com mapas cientificamente derivados: **batlow**, **lapaz** e **bamako**
- Avaliar aspectos de acessibilidade na escolha de mapas de cores
- Evidenciar como escolhas inadequadas podem levar a conclusões errôneas

## 🧪 Fundamentação Teórica

Este trabalho se baseia em conceitos apresentados nos artigos "Using Colour to Communicate" de Ed Hawkins e "The misuse of colour in science communication" (Crameri et al., Nature Communications, 2020), que discutem problemas do popular mapa rainbow e propõem alternativas cientificamente fundamentadas.

## 🎨 Mapas de Cores Analisados

A análise comparou quatro mapas de cores distintos:

1. **Rainbow**: Tradicionalmente usado em visualizações científicas, apresenta transições por todo o espectro de cores do arco-íris, do violeta ao vermelho.
2. **Batlow**: Mapa científico que vai do azul escuro ao amarelo/laranja, com transições suaves e perceptualmente uniformes.
3. **Lapaz**: Mapa científico com transição do azul para o branco/amarelo, projetado para ser perceptualmente uniforme.
4. **Bamako**: Mapa científico com transição do azul para o magenta e amarelo, oferecendo uma alternativa estética distinta.

<p align="center">
  <img src="outputs/all_gradients_comparison.png" width="80%" alt="Comparação de Gradientes entre Rainbow, Batlow, Lapaz e Bamako">
  <br>
  <em>Comparação visual dos quatro mapas de cores analisados neste estudo</em>
</p>

## 📊 Metodologia

### Conjuntos de Dados

Os dados utilizados nesta análise foram obtidos do repositório [Our World in Data](https://ourworldindata.org/) e incluem:

- Índice de Desenvolvimento Humano (IDH) global
- Índice de felicidade (Cantril ladder score)
- Expectativa de vida global

### Visualizações Desenvolvidas

Foram gerados cinco tipos de visualizações comparativas para analisar o desempenho dos diferentes mapas de cores:

1. **Comparação de Gradientes**: Demonstra como cada mapa de cores representa um gradiente contínuo de valores.
2. **Gráficos de Barras**: Mostra o IDH dos 20 países com maior desenvolvimento.
3. **Gráficos de Dispersão**: Relaciona IDH e expectativa de vida.
4. **Mapas de Calor**: Visualiza correlações entre variáveis.
5. **Simulação em Escala de Cinza**: Demonstra como cada mapa de cores é percebido quando convertido para escala de cinza.

## 📝 Principais Resultados

A análise comparativa demonstrou claramente que o mapa rainbow apresenta problemas significativos:

- **Distorções perceptuais**: Diferentes regiões do espectro são percebidas de forma não uniforme
- **Falsas estruturas**: Cria divisões artificiais em dados contínuos
- **Problemas de acessibilidade**: Perde informação significativa quando convertido para escala de cinza

Em contraste, os mapas cientificamente derivados demonstraram melhor:

- Uniformidade perceptual
- Representação fiel dos dados subjacentes
- Acessibilidade para pessoas com deficiência na percepção de cores

## 📚 Conteúdo do Repositório

Este repositório contém:

1. Scripts Python para geração das visualizações comparativas
2. Conjuntos de dados sobre desenvolvimento humano global
3. Visualizações geradas para demonstração
4. Um relatório completo em PDF com todas as análises e conclusões

## 📄 Conclusões e Referências

Para conclusões detalhadas, incluindo análises específicas de cada visualização, bem como as referências bibliográficas completas, consulte o [relatório em PDF](Comparando_Mapas_de_Cores_para_Visualização_Científica__ou_Não_.pdf) disponível neste repositório.

## 📜 Licença MIT

Este projeto é disponibilizado sob a licença MIT.
