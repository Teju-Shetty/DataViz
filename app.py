import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Set page configuration
st.set_page_config(layout="wide")

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
    plt.title(f'Heatmap of {indicator} Over Time', fontsize=16)
    plt.xlabel('Year', fontsize=14)
    plt.ylabel('Country', fontsize=14)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=12)
    st.pyplot(plt)

# Sidebar for navigation
st.sidebar.title("Navigation")
options = st.sidebar.radio("Select a view:", ["Objective 1", "Objective 3"])

if options == "Objective 1":
    st.header('Geographic disparities and temporal trends in the African nations')

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

elif options == "Objective 3":
    st.header('Country-specific Analysis of HIV Indicators')

    # Get unique country names
    countries = data["Country.Name"].unique()

    # Create a dropdown menu for selecting the country
    selected_country = st.selectbox("Select a country", countries)

    # Filter the data for the selected country
    country_data = data[data["Country.Name"] == selected_country]

    # Filter the data for the desired indicators
    indicator1 = "Adults (ages 15+) and children (0-14 years) living with HIV"
    indicator2 = "Adults (ages 15+) and children (ages 0-14) newly infected with HIV"
    indicator3 = "Antiretroviral therapy coverage (% of people living with HIV)"
    indicator4 = "AIDS estimated deaths (UNAIDS estimates)" 
    
    filtered_data1 = country_data[country_data["Indicator.Name"] == indicator1]
    filtered_data2 = country_data[country_data["Indicator.Name"] == indicator2]
    filtered_data3 = country_data[country_data["Indicator.Name"] == indicator3]
    filtered_data4 = country_data[country_data["Indicator.Name"] == indicator4]

    # Extract the relevant columns for x and y values
    years = data.columns[4:]  # Assuming the years start from the 5th column
    hiv_counts1 = filtered_data1.iloc[:, 4:].astype(float)  # Assuming the counts start from the 5th column
    hiv_counts2 = filtered_data2.iloc[:, 4:].astype(float)  # Assuming the counts start from the 5th column
    coverage_percentage = filtered_data3.iloc[:, 4:].astype(float)
    estimated_deaths = filtered_data4.iloc[:, 4:].astype(float)

    # Plot the bar chart
    fig, ax = plt.subplots(figsize=(20, 10))  # Increase the figure size here
    ax.bar(years, hiv_counts1.values.flatten(), label=indicator1, color="pink")

    # Add the bar chart for the multiplied percentage
    ax.bar(
        years,
        coverage_percentage.values.flatten() * hiv_counts1.values.flatten() / 100,
        alpha=0.3,
        color="red",
        label=f"{indicator3}",
    )

    # Plot the area chart
    ax.fill_between(years, hiv_counts2.values.flatten(), color="blue", alpha=0.3, label=indicator2)

    # Plot the dotted line for the new indicator
    ax.plot(years, estimated_deaths.values.flatten(), linestyle='--', color='black', label=indicator4, linewidth=2)

    # Add labels and title
    ax.set_xlabel("Year", fontsize=14)
    ax.set_ylabel("Population living with HIV", fontsize=14)
    ax.set_title("Accessibility and Effectiveness of HIV Treatment", fontsize=16)

    # Rotate x-axis labels for better readability
    ax.set_xticklabels([year.replace("X", "") for year in years], fontsize=12)
    ax.set_yticklabels(ax.get_yticks(), fontsize=12)

    # Add a legend below the plot
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), fontsize=12, ncol=1)  # Position legend below the plot

    # Adjust layout to make space for the legend
    plt.tight_layout(rect=[0, 0.05, 1, 1])

    # Show the plot
    st.pyplot(fig)

# Add custom CSS to control layout and styling
st.markdown("""
    <style>
    .reportview-container .main .block-container{
        max-width: 95%;
        padding: 2rem;
    }
    .reportview-container .sidebar .block-container{
        max-width: 30%;
        padding: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)
