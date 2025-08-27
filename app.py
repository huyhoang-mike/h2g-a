import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px
import numpy as np
import pyaml
import plotly.graph_objects as go


st.set_page_config(page_title="H2Global meets Africa", layout="wide")

# Define vertical sidebar
with st.sidebar:
    title=st.title("Marginal Prices for Hydrogen export ports")
    topic= st.selectbox("", ["Marginal prices","africa hydrogen", "Plot summary"])
    
    year = st.selectbox(
        "SELECT YEAR",
        ["2035","2050"],)
    

#Plot for marginal prices figures
data = {"line_x": [], "line_y": [], "data_start": [], "data_end": [], "colors": [], "years": [], "countries": []}

if year=="2035":
    data_start="0.1MtH2export"
    data_end="0.7MtH2export"
    df=pd.read_csv("results/marginal_prices_35.csv")
    countries = df["country"].unique()
    
else:
    data_start="0.7MtH2export"
    data_end="4.0MtH2export"
    df=pd.read_csv( "results/marginal_prices_50.csv")
    countries = df["country"].unique()

for country in countries:
   
    row_start = df.loc[(df.scen == data_start) & (df.country == country), "value"]
    val_start = row_start.values[0] if not row_start.empty else None

    row_end = df.loc[(df.scen == data_end) & (df.country == country), "value"]
    val_end = row_end.values[0] if not row_end.empty else None

    data["data_start"].append(val_start)
    data["data_end"].append(val_end)
    data["line_x"].extend([val_start, val_end, None])
    data["line_y"].extend([country, country, None])

fig = go.Figure(
        data=[
            go.Scatter(
                x=data["line_x"],
                y=data["line_y"],
                mode="lines",
                showlegend=False,
                marker=dict(
                    color="grey"
                )
            ),
            go.Scatter(
                x=data["data_start"],
                y=countries,
                mode="markers+text",
                name=data_start,
                text=data["data_start"],            
                textposition="top center",
                texttemplate="%{text:.1f}",
                textfont=dict(size=15),
                marker=dict(
                    color="#A6BCC9",
                    size=20
                )

            ),
            go.Scatter(
                x=data["data_end"],
                y=countries,
                mode="markers+text",
                name=data_end,
                text=data["data_end"],
                textposition="top center",
                texttemplate="%{text:.1f}",
                textfont=dict(size= 15),
                marker=dict(
                    color="#179c7d",
                    size=20
                )
            ),
        ]
    )

fig.update_layout(
        title= f"Marginal price for H2 at export port in {year} <br><sub>Per country and H2 export volume in €/MWh_H2_LHV <sub>",
        title_font_size=30,
        width=400,
        height=750,
        legend_itemclick=False,
    )

if topic == "Marginal prices":
    st.plotly_chart(fig)
