import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
data = pd.read_csv('dataviz24.csv')

# Define indicator lists
prevalence_indicators_list = [
    'Prevalence of HIV, female (% ages 15-24)',
    'Prevalence of HIV, male (% ages 15-24)',
    'Prevalence of HIV, total (% of population ages 15-49)'
]

incidence_indicators_list = [
    'Incidence of HIV, ages 15-24 (per 1,000 uninfected population ages 15-24)',
    'Incidence of HIV, ages 15-49 (per 1,000 uninfected population ages 15-49)',
    'Incidence of HIV, ages 50+ (per 1,000 uninfected population ages 50+)',
    'Incidence of HIV, all (per 1,000 uninfected population)'
]

# Filter and melt data
def filter_and_melt_data(data, indicators):
    filtered_data = data[data['Indicator.Name'].isin(indicators)]
    melted_data = pd.melt(filtered_data, id_vars=['Country.Name', 'Country.Code', 'Indicator.Name', 'Indicator.Code'], 
                          var_name='Year', value_name='Value')
    melted_data['Year'] = melted_data['Year'].str[1:].astype(int)
    melted_data.dropna(inplace=True)
    return melted_data

# Generate heatmap
def generate_heatmap(data, indicator, colormap):
    heatmap_data = data[data['Indicator.Name'] == indicator].pivot(index='Country.Name', columns='Year', values='Value')
    plt.figure(figsize=(20, 10))
    sns.heatmap(heatmap_data, cmap=colormap, cbar_kws={'label': '% of population' if 'Prevalence' in indicator else 'Per 1,000 uninfected population'})
    plt.title(f'Heatmap of {indicator} Over Time')
    plt.xlabel('Year')
    plt.ylabel('Country')
    st.pyplot(plt)

# Streamlit app
st.title('HIV Indicators Heatmap')

# Dropdown for prevalence indicators
prevalence_indicator = st.selectbox('Select Prevalence Indicator:', prevalence_indicators_list)
prevalence_melted_data = filter_and_melt_data(data, prevalence_indicators_list)

# Dropdown for incidence indicators
incidence_indicator = st.selectbox('Select Incidence Indicator:', incidence_indicators_list)
incidence_melted_data = filter_and_melt_data(data, incidence_indicators_list)

# Dropdown for colormap selection
colormap = st.selectbox('Select Heatmap Color Palette:', ['Blues', 'Greens', 'Reds', 'Oranges'])

# Generate heatmaps based on selection
st.subheader('Prevalence Heatmap')
generate_heatmap(prevalence_melted_data, prevalence_indicator, colormap)

st.subheader('Incidence Heatmap')
generate_heatmap(incidence_melted_data, incidence_indicator, colormap)
