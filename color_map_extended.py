import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.colors import ListedColormap
from matplotlib import cm
import os
import sys

# Create output directory if it doesn't exist
os.makedirs('outputs', exist_ok=True)

# Install required packages if needed
try:
    import cmocean
    import colorcet as cc
    import cmcrameri.cm as cmc
except ImportError:
    print("Installing required packages...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "cmocean", "colorcet", "cmcrameri"])
    import cmocean
    import colorcet as cc
    import cmcrameri.cm as cmc

# Load datasets
print("Loading datasets...")
hdi_data = pd.read_csv('human-development-index.csv')
happiness_data = pd.read_csv('happiness-cantril-ladder.csv')
life_expectancy_data = pd.read_csv('life-expectancy.csv')

# Load scientific colormaps from libraries
print("Loading scientific colormaps...")
# Using perceptually uniform colormaps from cmcrameri
batlow_cmap = cmc.batlow    # Batlow: blue to yellow/orange
lapaz_cmap = cmc.lapaz      # Lapaz: blue to white/yellow
bamako_cmap = cmc.bamako    # Bamako: purple to green/yellow

# Prepare data
print("Preparing data...")
# Get the most recent HDI data (2022)
hdi_latest = hdi_data[hdi_data['Year'] == 2022].copy()
# Filter only entities that are countries (have codes)
hdi_countries = hdi_latest[hdi_latest['Code'].notna()].copy()

# 1. GRADIENT COMPARISON
print("Creating gradient comparison for all colormaps...")
# Create a gradient
gradient = np.linspace(0, 1, 256)
gradient = np.vstack((gradient, gradient))

# Create figure for comparison
fig, axes = plt.subplots(4, 1, figsize=(12, 8))

# Show gradients for all colormaps
axes[0].imshow(gradient, aspect='auto', cmap='rainbow')
axes[0].set_title('Rainbow Color Gradient', fontsize=14)
axes[0].set_yticks([])
axes[0].set_xticks([0, 64, 128, 192, 255])
axes[0].set_xticklabels(['0.0', '0.25', '0.5', '0.75', '1.0'])

axes[1].imshow(gradient, aspect='auto', cmap=batlow_cmap)
axes[1].set_title('Thermal Color Gradient (similar to Batlow)', fontsize=14)
axes[1].set_yticks([])
axes[1].set_xticks([0, 64, 128, 192, 255])
axes[1].set_xticklabels(['0.0', '0.25', '0.5', '0.75', '1.0'])

axes[2].imshow(gradient, aspect='auto', cmap=lapaz_cmap)
axes[2].set_title('Haline Color Gradient (similar to Lapaz)', fontsize=14)
axes[2].set_yticks([])
axes[2].set_xticks([0, 64, 128, 192, 255])
axes[2].set_xticklabels(['0.0', '0.25', '0.5', '0.75', '1.0'])

axes[3].imshow(gradient, aspect='auto', cmap=bamako_cmap)
axes[3].set_title('BMY Color Gradient (similar to Bamako)', fontsize=14)
axes[3].set_yticks([])
axes[3].set_xticks([0, 64, 128, 192, 255])
axes[3].set_xticklabels(['0.0', '0.25', '0.5', '0.75', '1.0'])

plt.tight_layout()
plt.savefig('outputs/all_gradients_comparison.png', dpi=300)
plt.close()

# 2. BAR CHART COMPARISON
print("Creating bar chart comparison for all colormaps...")
# Select top 20 countries by HDI
top_hdi = hdi_countries.sort_values('Human Development Index', ascending=False).head(20)

# Create figure for comparison
fig, axes = plt.subplots(4, 1, figsize=(14, 16))

# Using Rainbow colormap
rainbow_colors = cm.rainbow(np.linspace(0, 1, len(top_hdi)))
axes[0].barh(top_hdi['Entity'], top_hdi['Human Development Index'], color=rainbow_colors)
axes[0].set_title('Human Development Index (2022) - Rainbow Color Map', fontsize=14)
axes[0].set_xlabel('Human Development Index')
axes[0].set_xlim(0.8, 1.0)
axes[0].grid(axis='x', linestyle='--', alpha=0.7)

# Using Batlow colormap
batlow_colors_arr = batlow_cmap(np.linspace(0, 1, len(top_hdi)))
axes[1].barh(top_hdi['Entity'], top_hdi['Human Development Index'], color=batlow_colors_arr)
axes[1].set_title('Human Development Index (2022) - Thermal Color Map', fontsize=14)
axes[1].set_xlabel('Human Development Index')
axes[1].set_xlim(0.8, 1.0)
axes[1].grid(axis='x', linestyle='--', alpha=0.7)

# Using Lapaz colormap
lapaz_colors_arr = lapaz_cmap(np.linspace(0, 1, len(top_hdi)))
axes[2].barh(top_hdi['Entity'], top_hdi['Human Development Index'], color=lapaz_colors_arr)
axes[2].set_title('Human Development Index (2022) - Haline Color Map', fontsize=14)
axes[2].set_xlabel('Human Development Index')
axes[2].set_xlim(0.8, 1.0)
axes[2].grid(axis='x', linestyle='--', alpha=0.7)

# Using Bamako colormap
bamako_colors_arr = bamako_cmap(np.linspace(0, 1, len(top_hdi)))
axes[3].barh(top_hdi['Entity'], top_hdi['Human Development Index'], color=bamako_colors_arr)
axes[3].set_title('Human Development Index (2022) - BMY Color Map', fontsize=14)
axes[3].set_xlabel('Human Development Index')
axes[3].set_xlim(0.8, 1.0)
axes[3].grid(axis='x', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.savefig('outputs/all_barplots_comparison.png', dpi=300)
plt.close()

# 3. SCATTER PLOT COMPARISON
print("Creating scatter plot comparison for all colormaps...")
# Prepare data for scatter plot
life_exp_2022 = life_expectancy_data[life_expectancy_data['Year'] == 2022].copy()
merged_life_data = pd.merge(hdi_countries, life_exp_2022, on=['Entity', 'Code'], how='inner')

# Create figure for comparison
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Scatter plot using Rainbow
scatter1 = axes[0, 0].scatter(merged_life_data['Human Development Index'], 
                      merged_life_data['Period life expectancy at birth - Sex: total - Age: 0'],
                      c=merged_life_data['Human Development Index'], 
                      cmap='rainbow', 
                      s=50, alpha=0.8)
axes[0, 0].set_title('HDI vs. Life Expectancy - Rainbow Color Map', fontsize=14)
axes[0, 0].set_xlabel('Human Development Index')
axes[0, 0].set_ylabel('Life Expectancy at Birth (years)')
axes[0, 0].grid(linestyle='--', alpha=0.7)
plt.colorbar(scatter1, ax=axes[0, 0], label='HDI')

# Scatter plot using Batlow
scatter2 = axes[0, 1].scatter(merged_life_data['Human Development Index'], 
                      merged_life_data['Period life expectancy at birth - Sex: total - Age: 0'],
                      c=merged_life_data['Human Development Index'], 
                      cmap=batlow_cmap, 
                      s=50, alpha=0.8)
axes[0, 1].set_title('HDI vs. Life Expectancy - Thermal Color Map', fontsize=14)
axes[0, 1].set_xlabel('Human Development Index')
axes[0, 1].set_ylabel('Life Expectancy at Birth (years)')
axes[0, 1].grid(linestyle='--', alpha=0.7)
plt.colorbar(scatter2, ax=axes[0, 1], label='HDI')

# Scatter plot using Lapaz
scatter3 = axes[1, 0].scatter(merged_life_data['Human Development Index'], 
                      merged_life_data['Period life expectancy at birth - Sex: total - Age: 0'],
                      c=merged_life_data['Human Development Index'], 
                      cmap=lapaz_cmap, 
                      s=50, alpha=0.8)
axes[1, 0].set_title('HDI vs. Life Expectancy - Haline Color Map', fontsize=14)
axes[1, 0].set_xlabel('Human Development Index')
axes[1, 0].set_ylabel('Life Expectancy at Birth (years)')
axes[1, 0].grid(linestyle='--', alpha=0.7)
plt.colorbar(scatter3, ax=axes[1, 0], label='HDI')

# Scatter plot using Bamako
scatter4 = axes[1, 1].scatter(merged_life_data['Human Development Index'], 
                      merged_life_data['Period life expectancy at birth - Sex: total - Age: 0'],
                      c=merged_life_data['Human Development Index'], 
                      cmap=bamako_cmap, 
                      s=50, alpha=0.8)
axes[1, 1].set_title('HDI vs. Life Expectancy - BMY Color Map', fontsize=14)
axes[1, 1].set_xlabel('Human Development Index')
axes[1, 1].set_ylabel('Life Expectancy at Birth (years)')
axes[1, 1].grid(linestyle='--', alpha=0.7)
plt.colorbar(scatter4, ax=axes[1, 1], label='HDI')

plt.tight_layout()
plt.savefig('outputs/all_scatter_comparison.png', dpi=300)
plt.close()

# 4. HEATMAP COMPARISON
print("Creating heatmap comparison for all colormaps...")
# Prepare data for heatmap
happiness_2022 = happiness_data[happiness_data['Year'] == 2022].copy()
merged_data = pd.merge(hdi_countries, happiness_2022, on=['Entity', 'Code'], how='inner')

# Create correlation matrix
correlation_matrix = np.corrcoef([
    merged_data['Human Development Index'],
    merged_data['Cantril ladder score']
])

# Create figure for comparison
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Heatmap using Rainbow
sns.heatmap(correlation_matrix, annot=True, cmap='rainbow', ax=axes[0, 0], 
            xticklabels=['HDI', 'Happiness'], yticklabels=['HDI', 'Happiness'])
axes[0, 0].set_title('Correlation - Rainbow Color Map', fontsize=14)

# Heatmap using Batlow
sns.heatmap(correlation_matrix, annot=True, cmap=batlow_cmap, ax=axes[0, 1],
            xticklabels=['HDI', 'Happiness'], yticklabels=['HDI', 'Happiness'])
axes[0, 1].set_title('Correlation - Thermal Color Map', fontsize=14)

# Heatmap using Lapaz
sns.heatmap(correlation_matrix, annot=True, cmap=lapaz_cmap, ax=axes[1, 0],
            xticklabels=['HDI', 'Happiness'], yticklabels=['HDI', 'Happiness'])
axes[1, 0].set_title('Correlation - Haline Color Map', fontsize=14)

# Heatmap using Bamako
sns.heatmap(correlation_matrix, annot=True, cmap=bamako_cmap, ax=axes[1, 1],
            xticklabels=['HDI', 'Happiness'], yticklabels=['HDI', 'Happiness'])
axes[1, 1].set_title('Correlation - BMY Color Map', fontsize=14)

plt.tight_layout()
plt.savefig('outputs/all_heatmap_comparison.png', dpi=300)
plt.close()

# 5. GRAYSCALE CONVERSION COMPARISON
print("Creating grayscale comparison for all colormaps...")
# Function to convert to grayscale
def rgb_to_grayscale(rgb):
    # Using standard luminance calculation (0.299R + 0.587G + 0.114B)
    return np.dot(rgb[:, :3], [0.299, 0.587, 0.114])

# Get colors from all colormaps
rainbow_colors_array = cm.rainbow(np.linspace(0, 1, 256))
batlow_colors_array = batlow_cmap(np.linspace(0, 1, 256))
lapaz_colors_array = lapaz_cmap(np.linspace(0, 1, 256))
bamako_colors_array = bamako_cmap(np.linspace(0, 1, 256))

# Convert to grayscale
rainbow_gray = rgb_to_grayscale(rainbow_colors_array)
batlow_gray = rgb_to_grayscale(batlow_colors_array)
lapaz_gray = rgb_to_grayscale(lapaz_colors_array)
bamako_gray = rgb_to_grayscale(bamako_colors_array)

# Create custom grayscale colormaps
rainbow_gray_cmap = ListedColormap(np.column_stack((rainbow_gray, rainbow_gray, rainbow_gray)))
batlow_gray_cmap = ListedColormap(np.column_stack((batlow_gray, batlow_gray, batlow_gray)))
lapaz_gray_cmap = ListedColormap(np.column_stack((lapaz_gray, lapaz_gray, lapaz_gray)))
bamako_gray_cmap = ListedColormap(np.column_stack((bamako_gray, bamako_gray, bamako_gray)))

# Create the visualization
fig, axes = plt.subplots(4, 2, figsize=(14, 16))

# Original and grayscale versions
# Rainbow
axes[0, 0].imshow(gradient, aspect='auto', cmap='rainbow')
axes[0, 0].set_title('Rainbow - Original', fontsize=12)
axes[0, 0].set_yticks([])
axes[0, 0].set_xticks([])

axes[0, 1].imshow(gradient, aspect='auto', cmap=rainbow_gray_cmap)
axes[0, 1].set_title('Rainbow - Grayscale', fontsize=12)
axes[0, 1].set_yticks([])
axes[0, 1].set_xticks([])

# Batlow
axes[1, 0].imshow(gradient, aspect='auto', cmap=batlow_cmap)
axes[1, 0].set_title('Thermal - Original', fontsize=12)
axes[1, 0].set_yticks([])
axes[1, 0].set_xticks([])

axes[1, 1].imshow(gradient, aspect='auto', cmap=batlow_gray_cmap)
axes[1, 1].set_title('Thermal - Grayscale', fontsize=12)
axes[1, 1].set_yticks([])
axes[1, 1].set_xticks([])

# Lapaz
axes[2, 0].imshow(gradient, aspect='auto', cmap=lapaz_cmap)
axes[2, 0].set_title('Haline - Original', fontsize=12)
axes[2, 0].set_yticks([])
axes[2, 0].set_xticks([])

axes[2, 1].imshow(gradient, aspect='auto', cmap=lapaz_gray_cmap)
axes[2, 1].set_title('Haline - Grayscale', fontsize=12)
axes[2, 1].set_yticks([])
axes[2, 1].set_xticks([])

# Bamako
axes[3, 0].imshow(gradient, aspect='auto', cmap=bamako_cmap)
axes[3, 0].set_title('BMY - Original', fontsize=12)
axes[3, 0].set_yticks([])
axes[3, 0].set_xticks([])

axes[3, 1].imshow(gradient, aspect='auto', cmap=bamako_gray_cmap)
axes[3, 1].set_title('BMY - Grayscale', fontsize=12)
axes[3, 1].set_yticks([])
axes[3, 1].set_xticks([])

plt.tight_layout()
plt.savefig('outputs/all_grayscale_comparison.png', dpi=300)
plt.close()

print("All extended visualizations and analysis have been created and saved to the 'outputs' directory.") 