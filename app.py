import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px
import numpy as np
import pyaml
import plotly.graph_objects as go #für dynamische Afrika-Karte

st.set_page_config(page_title="H2Global meets Africa: Coupling", layout="wide")

st.title("Energy Partnership")
#HYDROGEN EXPORT QUANTITIES

@st.cache_data
def load_data():
    """
    Load data from a CSV file and rename specific values in the 'param' column.
    This function reads data from 'data/exportcountry.csv' into a pandas DataFrame,
    then renames the values 'eldemand' to 'dom_demand' and 'h2export' to 'h_export'
    in the 'param' column.
    Returns:
        pandas.DataFrame: The DataFrame containing the loaded and modified data.
    """

    # print(df.columns)

    df = pd.read_csv("data/exportcountry.csv")

    print(df.columns)

    # Rename eldemand to dom_demand and h2export to h_export (which are values in the column 'param')

    df["param"] = df["param"].replace(
        {"eldemand": "dom_demand", "h2export": "h_export"}
    )
    return df

def load_carriers():
    """
    Load available energy carriers from a CSV file.

    Returns:
        pandas.DataFrame: DataFrame with available carriers (column: 'carrier')
    """
    df = pd.read_csv("data/carriers.csv")
    df["carrier"] = df["carrier"].str.strip()  # Ensure that no spaces cause problems
    return df

def load_import_countries():
    """
    Load available import countries from a CSV file.

    Returns:
        pandas.DataFrame: DataFrame with available import countries (column: 'country')
    """
    df = pd.read_csv("data/importcountry.csv")
    df["country"] = df["country"].str.strip()
    return df

def load_impact_continent():
    """
    Load available continents from a CSV file.

    This function reads the 'impact_continent.csv' file located in the 'data' directory,
    and returns its contents as a pandas DataFrame.

    Returns:
        pandas.DataFrame: DataFrame containing available continents (column: 'continent')
    """
    df = pd.read_csv("data/impact_continent.csv")
    df["continent"] = df["continent"].str.strip()
    return df


def load_impact_factors():
    """
    Load available impact factors from a CSV file.

    This function reads the 'impact_factors.csv' file located in the 'data' directory,
    strips whitespace from column values, and returns the result as a pandas DataFrame.

    Returns:
        pandas.DataFrame: DataFrame containing available impact factors (column: 'factor')
    """
    df = pd.read_csv("data/impact_factors.csv")
    df["factor"] = df["factor"].str.strip()
    return df

def load_config():
    """
    Loads configuration from a YAML file.
    This function reads the 'config.yaml' file located in the current directory,
    parses its contents using the PyYAML library, and returns the configuration
    as a dictionary.
    Returns:
        dict: The configuration data loaded from the YAML file.
    Raises:
        FileNotFoundError: If the 'config.yaml' file does not exist.
        yaml.YAMLError: If there is an error parsing the YAML file.
    """
    with open("config.yaml", "r") as file:
        config = pyaml.yaml.load(file, Loader=pyaml.yaml.SafeLoader)
    return config

def get_line_style(carrier):    #Definition of line colours for drawing different transport options
    """
    Bestimmt den Stil der Verbindungslinie basierend auf dem ausgewählten Carrier.
    """
    if "pipeline" in carrier.lower():
        return {'color': 'green', 'dash': 'solid'}
    elif "ship" in carrier.lower():
        return {'color': 'blue', 'dash': 'dot'}
    elif "Electricity (hvdc)" in carrier:
        return {'color': 'red', 'dash': 'solid'}
    else:
        return {'color': 'black', 'dash': 'solid'}


data = load_data()

#st.write("Countrys in data set:", data["country"].unique())
    #To display directly in the dashboard which countries are taken into account  
    


config = load_config()
custom_colors = config.get("colors", {})

#Define horizontal sidebar
# Loading the new CSV files
impact_continent = load_impact_continent()
impact_factors = load_impact_factors()

# Two columns next to each other for the new drop-down menus
col1, col2 = st.columns(2)

# Dropdown for "Impact Continent"
with col1:
    continent = st.selectbox(
        "Select Continent (view)",
        impact_continent["continent"].unique()
    )

# Dropdown for "Impact Factors"
with col2:
    factor = st.selectbox(
        "Select Impact Factor",
        impact_factors["factor"].unique()
    )



# Define vertical sidebar
with st.sidebar:

    # image = Image.open("bmbf-logo.png")
    # st.image(image, width=150)
    st.image("bmbf-logo-new.png", width=300)

    st.title("AFRICA & EUROPE")

    st.markdown("This dashboard shows various scenarios for a possible basis for an energy partnership between Africa and Europe")

    st.header("Scenario selection")

    export_country = st.selectbox(
        "Export-Country",
        data.country.unique(),
        # np.insert(data.country.unique(), 0, "All"),
    )

    carriers = load_carriers()
    selected_carriers = st.selectbox(
    "Energy Carrier",
    carriers["carrier"].unique()
    )

    import_countries = load_import_countries()
    import_country = st.selectbox(
    "Import Country",
    import_countries["country"].unique()
    )


    # rule = st.selectbox(
    #     "Rule",
    #     data.rule.unique(),
    # )

    st.header("Documentation")

    st.markdown("Find the code on [GitHub](https://github.com/energyLS/exportquan).")
    # Placeholder
    st.markdown(" ")
    st.markdown(" ")
    st.markdown(" ")
    st.markdown(" ")

# st.warning(":building_construction: Sorry, this page is still under construction")

# hover_data = {
#     "Name": False,
#     "Description": True,
#     "Trainstop": True,
#     "Distance in km": True,
#     "lat": False,
#     "lon": False,
#     "size": False,
# }

# Filter the data based on the selected country and rule
data_sel = data.query("country == @export_country")

#plotting the interactive graph
dat = pd.read_csv("input/energy_balance.csv", index_col=0)

fig = go.Figure()

with open("config.yaml", "r") as file:
        config = pyaml.yaml.load(file, Loader=pyaml.yaml.SafeLoader)

colours = config.get("tech_colors", {})

sorted_carriers1=dat.sum(axis=1).sort_values().index

for carrier in sorted_carriers1:
    fig.add_trace(go.Bar(
        x=dat.columns,
        y=dat.loc[carrier],
        name=carrier,
        marker_color=colours.get(carrier, None),
        width=0.4
    ))

fig.update_layout(
    barmode='relative',
    yaxis_title='Electricity Balance in TWh',
    legend_title='Technology',
    template='plotly_white',
    yaxis_dtick=50,
    yaxis_range=[-200,200]
)

capex=pd.read_csv("input/capex.csv",index_col=0)

fig2=go.Figure()

sorted_carriers = capex.sum(axis=1).sort_values().index

for carrier in sorted_carriers:
    fig2.add_trace(go.Bar(
        x=capex.columns,
        name=carrier,
        y=capex.loc[carrier]/1000,
        marker_color=colours.get(carrier,None),
        width=0.4
    ))

total_saving=capex.sum().sum()/1000

fig2.add_trace(go.Scatter(
    x=[None],  
    y=[None],
    name='Total savings',  
    showlegend=True,
    line=dict(color="green", width=2)
))


fig2.add_shape(
    type="line",
    xref="paper",     
    yref="y",
    x0=0,             
    x1=1,             
    y0=total_saving,  
    y1=total_saving,
    line=dict(
        color="green",
        width=2,
        dash=None
    )
)

fig2.update_layout(
    barmode="relative",
    yaxis_title="Capex in billion €",
    legend_title="Technology",
    template="plotly_white",
    yaxis_dtick=2,
    yaxis_range=[-6,7],
    width=400, 
    height=450
)

with col1:
    if factor=="Impact on energy quantities" and continent=="Relation between Africa and Europe":
        st.plotly_chart(fig, width= 50, height= 400)

with col1:
    if factor=="Effects on total costs" and continent=="Relation between Africa and Europe":
        st.plotly_chart(fig2, use_container_width=False)


electricity_balance_africa=pd.read_csv("input/africa_energy_balance.csv",index_col=0)
fig3=go.Figure()

sorted = electricity_balance_africa.sum(axis=1).sort_values().index

for carrier in sorted:
   fig3.add_trace(go.Bar(
        x=electricity_balance_africa.columns,
        y=electricity_balance_africa.loc[carrier],
        name=carrier,
        marker_color=colours.get(carrier, None),
        width=0.4
    ))


fig3.update_layout(
    barmode='relative',
    yaxis_title='Electricity Balance in TWh',
    legend_title='Technology',
    template='plotly_white',
    yaxis_dtick=100,
    yaxis_range=[-400,400]
)

with col1:
    if continent=="Africa" and factor=="Impact on energy quantities":
        st.plotly_chart(fig3, width=50, height=400)

if not data_sel.empty:

    #st.image("firstresults.png", width=700)


    param = "h_export"

    df_melted = data_sel.melt(
        id_vars=["country", "name", "param", "lat", "lon"], var_name="year", value_name="value"
    )

    print(df_melted["year"].unique())

    # Convert 'year' to numeric
    df_melted["year"] = df_melted["year"].astype(int)

    # Filter data
    filtered_df = df_melted.query("param == 'h_export' or param == 'dom_demand'")

    # fig = px.line(
    #     filtered_df,
    #     x="year",
    #     y="value",
    #     color="param",  # Use 'param' to distinguish different lines
    #     line_group="param",
    #     title="Hydrogen export",
    #     color_discrete_map=custom_colors,  # Apply custom colors
    # )

    # # Update the x and y axis labels
    # fig.update_layout(
    #     xaxis_title="Year",
    #     yaxis_title="Change of electricity supply and\nhydrogen export in TWh",
    #     plot_bgcolor="black",  # Set background to white
    #     legend_title="",  # Remove the label of the legend
    # )

    # # Update the legend labels
    # labels = {
    #     "dom_demand": "Domestic electricity demand",
    #     "h_export": "Hydrogen export",
    # }
    # # fig.update_traces(name=None)  # Remove legend labels
    # fig.for_each_trace(lambda t: t.update(name=labels.get(t.name, t.name)))

    # st.plotly_chart(fig, use_container_width=True)

  # # export_country and import_country now come from the sidebar
    # countries = {
    #     "Algeria": {"lat": 28.0339, "lon": 1.6596},
    #     "South Africa": {"lat": -30.5595, "lon": 22.9375},
    #     "SELECT ALL": {"lat": 30.000, "lon": 2.200},
    #     "Germany": {"lat": 51.1657, "lon": 10.4515},
    # }

    # export_country = "Algeria"  # Example export country (is set by the UI)
    # import_country = ‘Germany’ # Example import country (set by the UI)


    # Get coordinates dynamically from the DataFrame
    export_lat = data.query("country == @export_country")["lat"].values[0]
    export_lon = data.query("country == @export_country")["lon"].values[0]
    import_lat = import_countries.query("country == @import_country")["lat"].values[0]
    import_lon = import_countries.query("country == @import_country")["lon"].values[0]

    print(export_country)
    print(data.query("country == @export_country"))

    export_name = data.query("country == @export_country")["name"].values[0]
    import_name = import_countries.query("country == @import_country")["name"].values[0]

    fig_map = go.Figure()

    # Point: Export-Country (Afrika)
    fig_map.add_trace(go.Scattergeo(
        lon=[export_lon],
        lat=[export_lat],
        mode='markers',
        marker=dict(size=10, color='blue'),
        name=export_name
    ))

    # Point: Import-Country (Europa)
    fig_map.add_trace(go.Scattergeo(
        lon=[import_lon],
        lat=[import_lat],
        mode='markers',
        marker=dict(size=10, color='red'),
        name=import_name
    ))

    # Determine the line style based on the carrier selection
    line_style = get_line_style(selected_carriers)

    # Line: Connection export-country -> import-country
    fig_map.add_trace(go.Scattergeo(
        lon=[export_lon, import_lon],
        lat=[export_lat, import_lat],
        mode='lines',
        line=dict(width=2, color=line_style['color'], dash=line_style['dash']),
        name=f"Route: {export_name} -> {import_name}"
    ))

    # Customise the layout of the map
    fig_map.update_layout(
        title_text="Export Routes from Africa to Europe",
        showlegend=True,
        geo=dict(
            scope='world',  # Represents the whole world
            projection_type='natural earth',  #Projection of the earth
            showland=True,  # Shows land masses
            landcolor='lightgray',  # Colour for country
            countrycolor='black',  # Country borders in black
            showcoastlines=True,  # Show coastlines
            coastlinecolor='black',  # coastlines colours
            showcountries=True,  # Shows countrylines
            countrywidth=0.5,  # Thickness of country borders
            coastlinewidth=0.7,  # Thickness of the coastlines
            center=dict(lat=20, lon=20),  # Centre the focus (between Africa and Europe)
            projection=dict(scale=2.5),  # Adjust the scale of the map to make both continents visible
        ),
        height=1000,  # Height of the card
        width=1500,  # Width of the map
    )

    # Streamlit shows the map
    st.plotly_chart(fig_map, use_container_width=True)

else:
    st.error("Sorry, no data to display. Please adjust your filters.")