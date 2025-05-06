import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.colors import ListedColormap
import os
import sys
import subprocess

# --- Configurações Globais ---
OUTPUT_DIR = 'outputs'
TARGET_YEAR_HDI = 2022
TARGET_YEAR_LIFE_EXPECTANCY = 2022
YEARS_FOR_CORRELATION = range(2016, 2023)
MIN_COUNTRIES_FOR_CORRELATION = 5
DEFAULT_DPI = 300
TITLE_FONTSIZE = 15
LABEL_FONTSIZE = 12
ANNOT_FONTSIZE = 9

# Nomes simplificados dos colormaps
COLORMAP_NAMES = {
    'rainbow': 'Rainbow',
    'batlow': 'Batlow',
    'lapaz': 'Lapaz',
    'bamako': 'Bamako'
}

# Aplicar estilo base do Seaborn
plt.style.use('seaborn-v0_8-whitegrid')

# --- Funções Auxiliares ---
def install_missing_packages():
    """Instala pacotes necessários se estiverem faltando."""
    missing_packages = []
    
    # Verificar pacotes necessários
    try:
        import cmocean
    except ImportError:
        missing_packages.append("cmocean")
    try:
        import colorcet
    except ImportError:
        missing_packages.append("colorcet")
    try:
        import cmcrameri.cm
    except ImportError:
        missing_packages.append("cmcrameri")

    if missing_packages:
        print(f"Instalando pacotes: {', '.join(missing_packages)}...")
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", *missing_packages],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            print("Pacotes instalados com sucesso.")
            # Importar os pacotes após instalação
            _import_visualization_packages()
        except subprocess.CalledProcessError as e:
            print(f"Erro ao instalar pacotes: {e}")
            print("Instale manualmente: 'pip install cmocean colorcet cmcrameri'")
            sys.exit(1)
    
    # Garantir que os módulos sejam importados
    _import_visualization_packages()

def _import_visualization_packages():
    """Importa pacotes de visualização para o escopo global."""
    global cmocean, cc, cmc
    import cmocean
    import colorcet as cc
    import cmcrameri.cm as cmc

def load_colormaps():
    """Carrega e retorna colormaps para visualizações."""
    print("Carregando colormaps científicos...")
    if 'cmc' not in globals() or cmc is None:
        _import_visualization_packages()

    return {
        'rainbow': plt.cm.rainbow,
        'batlow': cmc.batlow,
        'lapaz': cmc.lapaz,
        'bamako': cmc.bamako
    }

def load_datasets():
    """Carrega datasets de IDH, felicidade e expectativa de vida."""
    print("Carregando datasets...")
    try:
        hdi_data = pd.read_csv('human-development-index.csv')
        happiness_data = pd.read_csv('happiness-cantril-ladder.csv')
        life_expectancy_data = pd.read_csv('life-expectancy.csv')
        return hdi_data, happiness_data, life_expectancy_data
    except FileNotFoundError as e:
        print(f"Erro: Arquivo não encontrado: {e.filename}")
        print("Verifique se os arquivos CSV estão no diretório do script.")
        sys.exit(1)

def prepare_hdi_data(hdi_df, year):
    """Prepara dados de IDH para o ano especificado."""
    print(f"Preparando dados de IDH para {year}...")
    hdi_year_df = hdi_df[hdi_df['Year'] == year].copy()
    hdi_countries_df = hdi_year_df[
        hdi_year_df['Code'].notna() & hdi_year_df['Human Development Index'].notna()
    ].copy()
    return hdi_countries_df

def plot_gradients_comparison(colormaps, output_filename="gradient_comparison.png"):
    """Cria imagem comparando gradientes de colormaps."""
    print("Criando comparação de gradientes...")
    gradient_data = np.linspace(0, 1, 256).reshape(1, -1)
    gradient_image = np.vstack((gradient_data, gradient_data))
    
    num_colormaps = len(colormaps)
    fig, axes = plt.subplots(num_colormaps, 1, figsize=(12, 2.5 * num_colormaps), constrained_layout=True)
    if num_colormaps == 1:
        axes = [axes]

    for i, (name, cmap_obj) in enumerate(colormaps.items()):
        axes[i].imshow(gradient_image, aspect='auto', cmap=cmap_obj)
        axes[i].set_title(f"Gradiente de Cor - {COLORMAP_NAMES.get(name, name.capitalize())}", fontsize=TITLE_FONTSIZE)
        axes[i].set_yticks([])
        axes[i].set_xticks([0, 63, 127, 191, 255])
        axes[i].set_xticklabels(['0.0', '0.25', '0.5', '0.75', '1.0'], fontsize=LABEL_FONTSIZE)
    
    plt.savefig(os.path.join(OUTPUT_DIR, output_filename), dpi=DEFAULT_DPI)
    plt.close(fig)
    print(f"Comparação de gradientes salva em: {os.path.join(OUTPUT_DIR, output_filename)}")

def plot_bar_chart_comparison(data_df, value_col, label_col, title_prefix, colormaps, 
                             output_filename="barplots_comparison.png", xlim_range=None, top_n=20):
    """Cria gráficos de barras horizontais para os N maiores valores."""
    print(f"Criando comparação de gráficos de barras para '{title_prefix}'...")
    num_colormaps = len(colormaps)
    fig, axes = plt.subplots(num_colormaps, 1, figsize=(14, 5 * num_colormaps), constrained_layout=True)
    if num_colormaps == 1:
        axes = [axes]

    # Ordenar e selecionar os top N dados
    sorted_data_top_n = data_df.sort_values(value_col, ascending=False).head(top_n)

    for i, (name, cmap_obj) in enumerate(colormaps.items()):
        bar_colors = cmap_obj(np.linspace(0, 1, len(sorted_data_top_n)))
        axes[i].barh(sorted_data_top_n[label_col], sorted_data_top_n[value_col], 
                   color=bar_colors, edgecolor='grey', linewidth=0.5)
        axes[i].set_title(f"{title_prefix} - {COLORMAP_NAMES.get(name, name.capitalize())}", 
                        fontsize=TITLE_FONTSIZE)
        axes[i].set_xlabel(value_col, fontsize=LABEL_FONTSIZE)
        axes[i].tick_params(axis='y', labelsize=LABEL_FONTSIZE-1)
        axes[i].tick_params(axis='x', labelsize=LABEL_FONTSIZE)

        if xlim_range:
            axes[i].set_xlim(xlim_range)
        axes[i].grid(axis='x', linestyle=':', alpha=0.6)
        axes[i].invert_yaxis()

    plt.savefig(os.path.join(OUTPUT_DIR, output_filename), dpi=DEFAULT_DPI)
    plt.close(fig)
    print(f"Comparação de gráficos de barras salva em: {os.path.join(OUTPUT_DIR, output_filename)}")

def plot_scatter_comparison(data_df, x_col, y_col, color_val_col, title_prefix, colormaps, 
                           output_filename="scatter_comparison.png"):
    """Cria gráficos de dispersão, colorindo pontos por uma terceira variável."""
    print(f"Criando comparação de gráficos de dispersão para '{title_prefix}'...")
    num_colormaps = len(colormaps)
    rows = (num_colormaps + 1) // 2
    cols = 2 if num_colormaps > 1 else 1
    
    fig, axes = plt.subplots(rows, cols, figsize=(8 * cols, 6.5 * rows), squeeze=False, constrained_layout=True)
    axes_flat = axes.flatten()

    for i, (name, cmap_obj) in enumerate(colormaps.items()):
        ax = axes_flat[i]
        scatter_plot = ax.scatter(
            data_df[x_col], data_df[y_col], 
            c=data_df[color_val_col], cmap=cmap_obj, 
            s=60, alpha=0.8, edgecolor='k', linewidth=0.3
        )
        ax.set_title(f"{title_prefix} - {COLORMAP_NAMES.get(name, name.capitalize())}", fontsize=TITLE_FONTSIZE)
        ax.set_xlabel(x_col, fontsize=LABEL_FONTSIZE)
        ax.set_ylabel(y_col, fontsize=LABEL_FONTSIZE)
        ax.tick_params(axis='both', labelsize=LABEL_FONTSIZE-1)
        ax.grid(linestyle=':', alpha=0.6)
        
        # Barra de cores
        cbar = fig.colorbar(scatter_plot, ax=ax, label=color_val_col)
        cbar.ax.tick_params(labelsize=LABEL_FONTSIZE-1)
        cbar.set_label(color_val_col, size=LABEL_FONTSIZE)

    # Ocultar subplots não utilizados
    for j in range(i + 1, len(axes_flat)):
        fig.delaxes(axes_flat[j])

    plt.savefig(os.path.join(OUTPUT_DIR, output_filename), dpi=DEFAULT_DPI)
    plt.close(fig)
    print(f"Comparação de gráficos de dispersão salva em: {os.path.join(OUTPUT_DIR, output_filename)}")

def plot_grayscale_comparison(colormaps, output_filename="grayscale_comparison.png"):
    """Compara colormaps em sua forma original e em escala de cinza."""
    print("Criando comparação de versões em escala de cinza...")
    gradient_data = np.linspace(0, 1, 256).reshape(1, -1)
    gradient_image = np.vstack((gradient_data, gradient_data))

    num_colormaps = len(colormaps)
    fig, axes = plt.subplots(num_colormaps, 2, figsize=(10, 3.5 * num_colormaps), constrained_layout=True)
    if num_colormaps == 1:
         axes = np.array([axes]).reshape(1,2)

    def rgb_to_grayscale_values(rgb_colors_array):
        """Converte array RGB para valores em escala de cinza usando luminância."""
        return np.dot(rgb_colors_array[:, :3], [0.299, 0.587, 0.114])

    for i, (name, cmap_original_obj) in enumerate(colormaps.items()):
        # Colormap original
        current_ax_original = axes[i, 0] if num_colormaps > 1 else axes[0]
        current_ax_original.imshow(gradient_image, aspect='auto', cmap=cmap_original_obj)
        current_ax_original.set_title(f"{COLORMAP_NAMES.get(name, name.capitalize())}", fontsize=TITLE_FONTSIZE-1)
        current_ax_original.set_yticks([])
        current_ax_original.set_xticks([])

        # Escala de cinza
        original_colors_array = cmap_original_obj(np.linspace(0, 1, 256))
        grayscale_val_array = rgb_to_grayscale_values(original_colors_array)
        grayscale_cmap_obj = ListedColormap(np.column_stack([grayscale_val_array] * 3))
        
        current_ax_grayscale = axes[i, 1] if num_colormaps > 1 else axes[1]
        current_ax_grayscale.imshow(gradient_image, aspect='auto', cmap=grayscale_cmap_obj)
        current_ax_grayscale.set_title(f"{COLORMAP_NAMES.get(name, name.capitalize())} (Escala de Cinza)", 
                                     fontsize=TITLE_FONTSIZE-1)
        current_ax_grayscale.set_yticks([])
        current_ax_grayscale.set_xticks([])

    plt.savefig(os.path.join(OUTPUT_DIR, output_filename), dpi=DEFAULT_DPI)
    plt.close(fig)
    print(f"Comparação em escala de cinza salva em: {os.path.join(OUTPUT_DIR, output_filename)}")

def prepare_year_to_year_correlation_data(hdi_df, happiness_df, years_range):
    """Prepara dados para correlação ano a ano para IDH e Felicidade."""
    print("Preparando dados para correlação ano a ano...")
    countries_by_year_data_storage = {}

    for year_val in years_range:
        # Preparar dados de IDH para o ano atual
        hdi_year_df = hdi_df[hdi_df['Year'] == year_val].copy()
        hdi_year_df_filtered = hdi_year_df[hdi_year_df['Code'].notna()].copy()
        
        # Preparar dados de Felicidade para o ano atual
        happiness_year_df = happiness_df[happiness_df['Year'] == year_val].copy()
        
        # Mesclar os dados
        merged_year_df = pd.merge(
            hdi_year_df_filtered[['Entity', 'Code', 'Human Development Index']], 
            happiness_year_df[['Entity', 'Code', 'Cantril ladder score']], 
            on=['Entity', 'Code'], 
            how='inner'
        )
        
        if len(merged_year_df) >= MIN_COUNTRIES_FOR_CORRELATION:
            merged_year_df = merged_year_df.rename(columns={
                'Human Development Index': f'HDI_{year_val}',
                'Cantril ladder score': f'Happiness_{year_val}'
            })
            countries_by_year_data_storage[year_val] = merged_year_df[
                ['Entity', 'Code', f'HDI_{year_val}', f'Happiness_{year_val}']
            ]

    if not countries_by_year_data_storage:
        print("Aviso: Dados insuficientes para correlações ano a ano.")
        return pd.DataFrame(), pd.DataFrame()

    # Combinar dados de todos os anos
    all_years_data_list_dfs = list(countries_by_year_data_storage.values())
    if not all_years_data_list_dfs:
        return pd.DataFrame(), pd.DataFrame()

    # Encontrar interseção de países em todos os anos
    combined_all_years_df = all_years_data_list_dfs[0]
    for i in range(1, len(all_years_data_list_dfs)):
        combined_all_years_df = pd.merge(
            combined_all_years_df, all_years_data_list_dfs[i], on=['Entity', 'Code'], how='inner'
        )
    
    if combined_all_years_df.empty or len(combined_all_years_df) < MIN_COUNTRIES_FOR_CORRELATION:
        print(f"Aviso: Poucos países comuns ({len(combined_all_years_df)}) para análise robusta.")
        if combined_all_years_df.empty or len(combined_all_years_df) < 2:
            return pd.DataFrame(), pd.DataFrame()
    
    # Preparar matrizes de correlação
    hdi_cols = sorted([col for col in combined_all_years_df.columns if 'HDI_' in col])
    happiness_cols = sorted([col for col in combined_all_years_df.columns if 'Happiness_' in col])
    
    hdi_correlation_matrix = pd.DataFrame()
    if len(hdi_cols) > 1:
        hdi_correlation_matrix = combined_all_years_df[hdi_cols].corr()
        hdi_correlation_matrix.columns = [col.replace('HDI_', '') for col in hdi_correlation_matrix.columns]
        hdi_correlation_matrix.index = [idx.replace('HDI_', '') for idx in hdi_correlation_matrix.index]
    
    happiness_correlation_matrix = pd.DataFrame()
    if len(happiness_cols) > 1:
        happiness_correlation_matrix = combined_all_years_df[happiness_cols].corr()
        happiness_correlation_matrix.columns = [col.replace('Happiness_', '') for col in happiness_correlation_matrix.columns]
        happiness_correlation_matrix.index = [idx.replace('Happiness_', '') for idx in happiness_correlation_matrix.index]

    return hdi_correlation_matrix, happiness_correlation_matrix

def plot_heatmap_comparison(correlation_matrix_df, title_prefix, colormaps, 
                           output_filename="heatmap_comparison.png", vmin_val=None, 
                           vmax_val=None, center_val=None):
    """Cria heatmaps para matriz de correlação usando diferentes colormaps."""
    print(f"Criando comparação de heatmaps para '{title_prefix}'...")
    num_colormaps = len(colormaps)
    rows = (num_colormaps + 1) // 2
    cols = 2 if num_colormaps > 1 else 1

    fig, axes = plt.subplots(rows, cols, figsize=(8.5 * cols, 7.5 * rows), 
                           squeeze=False, constrained_layout=True)
    axes_flat = axes.flatten()

    # Ajustar vmin e vmax
    if vmin_val is None and center_val is None and not correlation_matrix_df.empty:
        if len(correlation_matrix_df) > 1:
            actual_min = correlation_matrix_df.min().min()
            actual_max = correlation_matrix_df.max().max()
            _vmin_val = max(0, actual_min * 0.98 if actual_min > 0 else actual_min * 1.02)
            _vmax_val = min(1.0, actual_max * 1.02 if actual_max > 0 else actual_max * 0.98)
            
            if _vmin_val >= _vmax_val:
                _vmin_val = _vmax_val - 0.1
        else:
            _vmin_val = 0.8
            _vmax_val = 1.0
    else:
        _vmin_val = vmin_val
        _vmax_val = vmax_val

    for i, (name, cmap_obj) in enumerate(colormaps.items()):
        ax = axes_flat[i]
        sns.heatmap(
            correlation_matrix_df, annot=True, fmt=".2f", cmap=cmap_obj, ax=ax,
            vmin=_vmin_val, vmax=_vmax_val, center=center_val,
            annot_kws={"size": ANNOT_FONTSIZE}, linewidths=.5, linecolor='gray',
            cbar_kws={"shrink": 0.8, "aspect": 30}
        )
        ax.set_title(f"{title_prefix} - {COLORMAP_NAMES.get(name, name.capitalize())}", 
                   fontsize=TITLE_FONTSIZE, pad=15)
        rotation = 45 if correlation_matrix_df.shape[0] > 5 else 0
        ax.tick_params(axis='both', labelsize=LABEL_FONTSIZE-1, rotation=rotation)

    # Ocultar subplots não utilizados
    for j in range(i + 1, len(axes_flat)):
        fig.delaxes(axes_flat[j])

    plt.savefig(os.path.join(OUTPUT_DIR, output_filename), dpi=DEFAULT_DPI)
    plt.close(fig)
    print(f"Comparação de heatmaps salva em: {os.path.join(OUTPUT_DIR, output_filename)}")

# --- Função Principal ---
def main():
    """Função principal que orquestra o fluxo de trabalho."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    install_missing_packages()
    colormaps_dict = load_colormaps()
    hdi_data_df, happiness_data_df, life_expectancy_data_df = load_datasets()
    hdi_countries_latest_df = prepare_hdi_data(hdi_data_df, TARGET_YEAR_HDI)
    
    # 1. Comparação de gradientes
    plot_gradients_comparison(colormaps_dict)

    # 2. Gráficos de barras para IDH
    if not hdi_countries_latest_df.empty:
        min_hdi_val = hdi_countries_latest_df['Human Development Index'].min()
        max_hdi_val = hdi_countries_latest_df['Human Development Index'].max()
        xlim_hdi_bars = (min_hdi_val * 0.98, max_hdi_val * 1.02)

        plot_bar_chart_comparison(
            data_df=hdi_countries_latest_df, 
            value_col='Human Development Index', 
            label_col='Entity',
            title_prefix=f'Índice de Desenvolvimento Humano ({TARGET_YEAR_HDI})', 
            colormaps=colormaps_dict,
            output_filename="hdi_barplots_comparison.png", 
            xlim_range=xlim_hdi_bars
        )
    else:
        print(f"Pulando gráficos de barras: sem dados para {TARGET_YEAR_HDI}")

    # 3. Gráficos de dispersão (IDH vs. Expectativa de Vida)
    life_exp_df = life_expectancy_data_df[
        life_expectancy_data_df['Year'] == TARGET_YEAR_LIFE_EXPECTANCY
    ].copy()
    
    if not hdi_countries_latest_df.empty and not life_exp_df.empty:
        merged_df = pd.merge(
            hdi_countries_latest_df, 
            life_exp_df, 
            on=['Entity', 'Code'],
            suffixes=('_hdi', '_le'),
            how='inner'
        )
        
        original_life_col = 'Period life expectancy at birth - Sex: total - Age: 0'
        new_life_col = 'Expectativa de Vida (anos)'
        
        if original_life_col in merged_df.columns:
            merged_df = merged_df.rename(columns={original_life_col: new_life_col})
        
        if not merged_df.empty and new_life_col in merged_df.columns:
            plot_scatter_comparison(
                data_df=merged_df, 
                x_col='Human Development Index', 
                y_col=new_life_col,
                color_val_col='Human Development Index',
                title_prefix=f'IDH vs. Expectativa de Vida ({TARGET_YEAR_HDI}/{TARGET_YEAR_LIFE_EXPECTANCY})',
                colormaps=colormaps_dict, 
                output_filename="hdi_life_expectancy_scatter_comparison.png"
            )
        else:
            print("Pulando gráficos de dispersão: dados mesclados insuficientes")
    else:
        print("Pulando gráficos de dispersão: falta de dados para os anos alvo")

    # 4. Comparação em escala de cinza
    plot_grayscale_comparison(colormaps_dict)
    
    # 5. Heatmap de correlação ano a ano (Felicidade)
    hdi_corr_years_df, happiness_corr_years_df = prepare_year_to_year_correlation_data(
        hdi_data_df, happiness_data_df, YEARS_FOR_CORRELATION
    )
    
    year_correlation_vmax = 1.0
    
    if not happiness_corr_years_df.empty:
        if len(happiness_corr_years_df) > 1:
            happiness_min_corr = happiness_corr_years_df.values[
                np.triu_indices_from(happiness_corr_years_df.values, k=1)
            ].min()
        else:
            happiness_min_corr = 0.8
        
        happiness_year_corr_vmin = max(0, happiness_min_corr - 0.05)

        plot_heatmap_comparison(
            correlation_matrix_df=happiness_corr_years_df,
            title_prefix=f'Correlação Felicidade Ano a Ano ({min(YEARS_FOR_CORRELATION)}-{max(YEARS_FOR_CORRELATION)})',
            colormaps=colormaps_dict, 
            output_filename="happiness_year_to_year_correlation_heatmap.png",
            vmin_val=happiness_year_corr_vmin,
            vmax_val=year_correlation_vmax
        )
    else:
        print("Não foi possível gerar o heatmap de correlação (dados insuficientes)")

    print(f"\nTodas as visualizações foram salvas no diretório '{OUTPUT_DIR}'.")

if __name__ == '__main__':
    main()