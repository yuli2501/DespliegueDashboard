
# ---------------------- LIBRERÍAS ------------------------
import streamlit as st
import plotly.express as px
import pandas as pd

# ---------------- PALETA DE COLORES ------------------
custom_palette = [
    "#C25E4C",  # Rojo ladrillo
    "#F7C59F",  # Durazno pastel (suavecito y cálido)
    "#E5B25D",  # Mostaza tulipán
    "#F28C38",  # Naranja Holanda
    "#F0E5D8",  # Cremita (deja este al final)
]

# ---------------- CONFIGURACIÓN INICIAL ------------------
st.set_page_config(layout="wide", page_title="Dashboard - Amsterdam", page_icon="🏡")

# ----------------- ESTILO CSS -----------------
st.markdown("""
    <style>
    /* Fondo general */
    .stApp {
        background-color: #F4F0EB;
    }

    .stAppHeader {
        background-color: #F4F0EB;
    }

    /* Sidebar */
    .stSidebar {  
        background-color: #F0E5D8 !important;
        border-right: 3px solid #C25E4C;
    }

    .stTittle{
        text-align: center;
    }
        
    /* Cambiar el fondo del selectbox */
    div[data-baseweb="select"] > div {
        background-color: #F4F0EB !important;  /* Cremita */
        border: 2px solid #C25E4C !important;  /* Rojo ladrillo */
        border-radius: 10px;
    }

    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    ::-webkit-scrollbar-thumb {
        background-color: #C25E4C;
        border-radius: 10px;
    }
    section[data-testid="stSidebar"] button {
        background-color: #F4F0EB !important;    
        border: 2px solid #C25E4C !important;    
        border-radius: 10px !important;         
        font-weight: bold !important;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------- FUNCIÓN DE CARGA -----------------------
@st.cache_data
def load_data():
    df = pd.read_csv("Amsterdam.csv")
    df = df.drop(columns=["Unnamed: 0.1", "Unnamed: 0", "id", "scrape_id", "host_id"], errors="ignore")

    # ----------------- LIMPIEZA DE VARIABLES -----------------
    if 'host_acceptance_rate' in df.columns:
        df['host_acceptance_rate'] = df['host_acceptance_rate'].str.replace('%', '').astype(float) 

    if 'host_response_rate' in df.columns:
        df['host_response_rate'] = df['host_response_rate'].str.replace('%', '').astype(float) 

    numeric_df = df.select_dtypes(['float', 'int'])
    numeric_cols = numeric_df.columns
    text_df = df.select_dtypes(['object'])
    text_cols = text_df.columns
    unique_categories = df['host_is_superhost'].unique() if 'host_is_superhost' in df.columns else []

    return df, numeric_cols, text_cols, unique_categories, numeric_df

# ---------------- CARGA DE DATOS -------------------------
df, numeric_cols, text_cols, unique_categories, numeric_df = load_data()

# ----------------- SIDEBAR -------------------------------
st.sidebar.title("Dashboard")
View = st.sidebar.selectbox(label="Vistas", options=[
    "Análisis univariado",
    "Regresión lineal simple",
    "Regresión lineal múltiple",
    "Regresión logística"
])

st.markdown("""
    <h1 style='text-align: center; color: #303030;'>
        Amsterdam
    </h1>
""", unsafe_allow_html=True)

# ---------------- ÍCONOS SVG ----------------
icon_alojamientos = """<svg width="24" height="24" viewBox="0 0 24 24" fill="#C25E4C" xmlns="http://www.w3.org/2000/svg"><path d="M3 9L12 2L21 9V20C21 20.55 20.55 21 20 21H4C3.45 21 3 20.55 3 20V9Z"/><path d="M9 22H15V12H9V22Z" fill="white"/></svg>"""
icon_precio = """<svg width="24" height="24" viewBox="0 0 64 64" fill="#E5B25D" xmlns="http://www.w3.org/2000/svg"><path d="M32 2C25.925 2 20 7.925 20 14V18H14V22H50V18H44V14C44 7.925 38.075 2 32 2ZM32 4C36.418 4 40 7.582 40 12V18H24V12C24 7.582 27.582 4 32 4ZM12 26V58C12 60.209 13.791 62 16 62H48C50.209 62 52 60.209 52 58V26H12ZM30 34H34C36.209 34 38 35.791 38 38C38 39.656 36.656 41 35 41H29V45H35C36.105 45 37 45.895 37 47C37 48.105 36.105 49 35 49H30C28.895 49 28 48.105 28 47V43H27C25.895 43 25 42.105 25 41C25 39.895 25.895 39 27 39H33C34.105 39 35 38.105 35 37C35 35.895 34.105 35 33 35H29C27.895 35 27 34.105 27 33C27 31.895 27.895 31 29 31H35C37.209 31 39 32.791 39 35C39 36.305 38.403 37.446 37.469 38.179C38.58 38.803 39.312 39.986 39.312 41.312C39.312 43.329 37.642 45 35.625 45H29.375C27.358 45 25.688 43.329 25.688 41.312C25.688 39.986 26.42 38.803 27.531 38.179C26.597 37.446 26 36.305 26 35C26 32.791 27.791 31 30 31Z"/></svg>"""
icon_disponibilidad = """<svg width="24" height="24" viewBox="0 0 24 24" fill="#8DA47E" xmlns="http://www.w3.org/2000/svg"><path d="M19 3H18V1H16V3H8V1H6V3H5C3.9 3 3 3.9 3 5V20C3 21.11 3.9 22 5 22H19C20.1 22 21 21.11 21 20V5C21 3.9 20.1 3 19 3ZM19 20H5V10H19V20ZM7 12H9V14H7V12Z"/></svg>"""
icon_limpieza = """<svg width="24" height="24" viewBox="0 0 24 24" fill="#F28C38" xmlns="http://www.w3.org/2000/svg"><path d="M12 17.27L18.18 21L16.54 13.97L22 9.24L14.81 8.62L12 2L9.19 8.62L2 9.24L7.46 13.97L5.82 21L12 17.27Z"/></svg>"""

# ---------------- KPIs ----------------
col1, col2, col3, col4 = st.columns(4)

def kpi_card(icon_svg, title, value, delta, title_color):
    st.markdown(f"""
        <div style='
            background-color: #FFFFFF;
            border: 2px solid #E5B25D;
            border-radius: 15px;
            padding: 8px 12px;
            height: 120px;  /* Altura fija */
            box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
            text-align: center;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;  /* Centramos todo */
            gap: 6px;  /* Espacio entre título, número e icono */
            overflow: hidden;
        '>
            <h3 style='
                color: {title_color}; 
                font-size: 15px; 
                margin: 0;
                overflow: hidden;
                text-overflow: ellipsis;
                white-space: nowrap;
            '>{title}</h3>
            <div style='
                display: flex; 
                align-items: center; 
                justify-content: center;
                margin: 0;
                flex-wrap: nowrap;
                max-height: 40px;  /* Control del bloque del número + ícono */
            '>
                {icon_svg}
                <h1 style='
                    margin: 0 0 0 10px; 
                    color: #000000; 
                    font-size: 26px;
                    overflow: hidden;
                    text-overflow: ellipsis;
                    white-space: nowrap;
                '>{value}</h1>
            </div>
            <p style='
                margin: 0; 
                font-size: 13px;
                overflow: hidden;
                text-overflow: ellipsis;
                white-space: nowrap;
            '>{delta}</p>
        </div>
    """, unsafe_allow_html=True)

with col1:
    kpi_card(icon_alojamientos, "Total alojamientos", len(df), "↑ 5% más que el mes pasado", "#C25E4C")
with col2:
    kpi_card(icon_precio, "Precio promedio (€)", f"{df['price'].mean():.2f}", "↑ 3% aumento", "#D4A037")
with col3:
    kpi_card(icon_disponibilidad, "Disponibilidad 365 (días)", f"{df['availability_365'].mean():.0f}", "↔ Estable", "#8DA47E")
with col4:
    kpi_card(icon_limpieza, "Score limpieza promedio", f"{df['review_scores_cleanliness'].mean():.2f}", "↑ 2% mejora", "#F28C38")

# ------------------ VISTA 1 ------------------------------
if View == "Análisis univariado":
    st.header("Análisis univariado")
    
    # ----------------- GRÁFICAS -----------------
    st.sidebar.subheader("Variables")

    # Variables categóricas para las gráficas
    opciones_bar = [
        'room_type', 'property_type', 'neighbourhood', 
        'host_response_time', 'host_response_rate', 'host_acceptance_rate'
    ]

    opciones_pie = [
        'room_type', 'host_is_superhost', 'instant_bookable', 'host_identity_verified',
        'has_availability', 'license', 'host_response_time'
    ]

    opciones_area = [
        'price', 'number_of_reviews', 'availability_365',
        'host_total_listings_count', 'accommodates', 'minimum_nights',
        'maximum_nights', 'review_scores_rating', 'review_scores_cleanliness'
    ]

    variable_cat_bar = st.sidebar.selectbox("Gráfica de frecuencias", options=opciones_bar)
    variable_cat_pie = st.sidebar.selectbox("Gráfica de categorías", options=opciones_pie)
    variable_cat_area = st.sidebar.selectbox("Gráfica de distribución", options=opciones_area)

    # ----------- GRÁFICA DE BARRAS -----------------
    count_data_bar = df[variable_cat_bar].value_counts().reset_index()
    count_data_bar.columns = [variable_cat_bar, 'Frecuencia']
    st.subheader(f"Frecuencia de {variable_cat_bar}")
    fig_bar = px.bar(count_data_bar, x=variable_cat_bar, y='Frecuencia', color_discrete_sequence=["#D4A037"])
    #fig_bar.update_layout(paper_bgcolor="#F4F0EB", plot_bgcolor="#F4F0EB")
    st.plotly_chart(fig_bar, use_container_width=True)

    # ----------- GRÁFICA DE PASTEL -----------------
    count_data_pie = df[variable_cat_pie].value_counts().reset_index()
    count_data_pie.columns = [variable_cat_pie, 'Cantidad']
    st.subheader(f"Categorías de {variable_cat_pie}")
    fig_pie = px.pie(count_data_pie, names=variable_cat_pie, values='Cantidad', color_discrete_sequence=custom_palette)
    #fig_pie.update_layout(paper_bgcolor="#F4F0EB", plot_bgcolor="#F4F0EB")
    st.plotly_chart(fig_pie, use_container_width=True)

    # ----------- GRÁFICA DE ÁREA  -----------------
    # Definir bins y labels
    if variable_cat_area == 'price':
        bins = [0, 50, 100, 200, 300, df['price'].max()]
        labels = ['Económico', 'Accesible', 'Medio', 'Alto', 'Premium']
    elif variable_cat_area == 'number_of_reviews':
        bins = [0, 30, 60, df['number_of_reviews'].max()]
        labels = ['Muy pocas', 'Pocas', 'Muchas']
    elif variable_cat_area == 'availability_365':
        bins = [0, 90, 180, 270, 365]
        labels = ['Menos de 3 meses', '3-6 meses', '6-9 meses', 'Todo el año']
    elif variable_cat_area == 'host_total_listings_count':
        bins = [0, 1, 2, 3, df['host_total_listings_count'].max()]
        labels = ['Muy pocos', 'Pocos', 'Muchos', 'Demasiados']
    elif variable_cat_area == 'accommodates':
        bins = [1, 2, 4, 5, df['accommodates'].max()]
        labels = ['Muy pocos huépedes', 'Pocos huéspedes', 'Muchos huéspedes', 'Demasiados huéspedes']
    elif variable_cat_area == 'minimum_nights':
        bins = [1, 2, 4, 5, df['minimum_nights'].max()]
        labels = ['1-2  noches', '2-4 noches', '4-5 noches', '1 semana']
    elif variable_cat_area == 'maximum_nights':
        bins = [1, 30, 90, 180, 365, df['maximum_nights'].max()]
        labels = ['Menos de 1 mes', '1-3 meses', '3-6 meses', '6-10 meses', '1 año']
    elif variable_cat_area == 'review_scores_rating':
        bins = [0, 2, 3, 4, 4.5, 5]
        labels = ['Muy bajo', 'Bajo', 'Aceptable', 'Bueno', 'Excelente']
    elif variable_cat_area == 'review_scores_cleanliness':
        bins = [0, 2, 3, 4, 4.5, 5]
        labels = ['Muy bajo', 'Bajo', 'Aceptable', 'Bueno', 'Excelente']
    else:
        st.warning("Selecciona una variable válida para la gráfica de área.")
        bins = None
        labels = None

    # Gráfica de área corregida
    df['Categorías'] = pd.cut(df[variable_cat_area], bins=bins, labels=labels, include_lowest=True)
    count_data_area = df.groupby('Categorías').size().reset_index(name='Cantidad')

    st.subheader(f"Distribución de {variable_cat_area}")
    fig_area = px.area(count_data_area, x='Categorías', y='Cantidad', color_discrete_sequence=["#8DA47E"])
    #fig_area.update_layout(paper_bgcolor="#F4F0EB", plot_bgcolor="#F4F0EB")
    st.plotly_chart(fig_area, use_container_width=True)

    # ----------- MAPA -------------------------------
    st.subheader("Ubicación de alojamientos")
    fig_map = px.scatter_mapbox(
        df,
        lat="latitude",
        lon="longitude",
        hover_name="name",
        color="price",  # O la variable que prefieras
        color_continuous_scale="YlOrRd",
        mapbox_style="carto-positron",  # Cambia a otro si quieres
        zoom=11,
        height=500
    )

    fig_map.update_layout(
        paper_bgcolor="#F4F0EB",  # Fondo igual al de tu página
        margin={"r":0, "t":30, "l":0, "b":0}
    )

    fig_map.update_traces(marker=dict(size=6, opacity=0.9))
    st.plotly_chart(fig_map, use_container_width=True)

    # ----------- SIDEBAR OPCIONES -------------
    st.sidebar.subheader("Dataset")
    show_data = st.sidebar.checkbox(label="Mostrar dataset")

    if show_data:
        st.subheader("Dataset completo")
        st.write(df)

        # Lista de las columnas numéricas
        important_cols = [
            'price', 'availability_365', 'number_of_reviews',
            'review_scores_rating', 'review_scores_accuracy', 'review_scores_cleanliness',
            'review_scores_checkin', 'review_scores_communication',
            'review_scores_location', 'review_scores_value'
        ]

        stats = df[important_cols].describe()
        stats = stats.loc[['mean', 'std', 'min', 'max']]
        stats.index = ['Promedio', 'Desviación estándar', 'Mínimo', 'Máximo']

        # Mostrar la tabla
        st.subheader("Resumen estadístico")
        st.write(stats)

# ------------------ VISTA 2 ------------------------------
elif View == "Regresión lineal simple":
    st.header("Regresión lineal simple")

    # ----------------- VARIABLES -----------------

    # Dependientes 
    variables_dependientes = [
        'price',
        'number_of_reviews',
        'review_scores_rating',
        'availability_365',
        'review_scores_value'
    ]

    # Independientes 
    variables_independientes = [
        'accommodates',
        'bedrooms',
        'beds',
        'minimum_nights',
        'maximum_nights ',
        'host_response_rate',
        'host_acceptance_rate',
        'review_scores_cleanliness',
        'review_scores_checkin ',
        'review_scores_location'
    ]

    st.sidebar.subheader("Variables")
    variable_dependiente = st.sidebar.selectbox("Variable dependiente (Y)", options=variables_dependientes)
    variable_independiente = st.sidebar.selectbox("Variable independiente (X)", options=variables_independientes)

    st.subheader(f"Diagrama de dispersión")

    # Scatterplot con línea de regresión
    fig_scatter = px.scatter(
        df,
        x=variable_independiente,
        y=variable_dependiente,
        trendline="ols",
    )

    fig_scatter.update_traces(marker=dict(color="#D4A037", size=5), selector=dict(mode='markers'))  
    fig_scatter.update_traces(line=dict(color="#C25E4C", width=2), selector=dict(mode='lines'))  

    fig_scatter.update_layout(
        #paper_bgcolor="#F4F0EB",  # Fondo cremita como el de tu dashboard
        #plot_bgcolor="#F4F0EB",
        xaxis_title=variable_independiente,
        yaxis_title=variable_dependiente
    )

    st.plotly_chart(fig_scatter, use_container_width=True)

    # Modelo de regresión
    from statsmodels.formula.api import ols
    model = ols(f"{variable_dependiente} ~ {variable_independiente}", data=df).fit()
    r_squared = model.rsquared
    p_value = model.pvalues[1]  # el p-valor de la variable independiente
    coef = model.params[1]  # pendiente
    correlation = df[[variable_dependiente, variable_independiente]].corr().iloc[0,1]
    n_datos = df[[variable_dependiente, variable_independiente]].dropna().shape[0]

    direccion = "incrementa" if coef > 0 else "disminuye"
    st.markdown(f"""
    Por cada unidad que aumenta **{variable_independiente}**, 
    el valor de **{variable_dependiente}** {direccion} en **{abs(coef):.4f} unidades** en promedio.
    """)

    # Interpretación automática
    st.subheader("Indicadores del modelo")
            # ---------------- ÍCONOS SVG ----------------
    icon_r2 = """<svg width="24" height="24" viewBox="0 0 24 24" fill="#E5B25D" xmlns="http://www.w3.org/2000/svg"><path d="M12 2C6.49 2 2 4.69 2 8V16C2 19.31 6.49 22 12 22C17.51 22 22 19.31 22 16V8C22 4.69 17.51 2 12 2ZM12 4C16.97 4 21 6.13 21 8C21 9.87 16.97 12 12 12C7.03 12 3 9.87 3 8C3 6.13 7.03 4 12 4ZM12 20C7.03 20 3 17.87 3 16V14.15C5.03 15.82 8.36 17 12 17C15.64 17 18.97 15.82 21 14.15V16C21 17.87 16.97 20 12 20Z"/></svg>"""
    icon_r = """<svg width="24" height="24" viewBox="0 0 24 24" fill="#E5B25D" xmlns="http://www.w3.org/2000/svg"><path d="M12 2C6.49 2 2 4.69 2 8V16C2 19.31 6.49 22 12 22C17.51 22 22 19.31 22 16V8C22 4.69 17.51 2 12 2ZM12 4C16.97 4 21 6.13 21 8C21 9.87 16.97 12 12 12C7.03 12 3 9.87 3 8C3 6.13 7.03 4 12 4ZM12 20C7.03 20 3 17.87 3 16V14.15C5.03 15.82 8.36 17 12 17C15.64 17 18.97 15.82 21 14.15V16C21 17.87 16.97 20 12 20Z"/></svg>"""
    icon_significativa = """<svg width="24" height="24" viewBox="0 0 24 24" fill="#8DA47E" xmlns="http://www.w3.org/2000/svg"><path d="M9 16.2L4.8 12L3.4 13.4L9 19L21 7L19.6 5.6L9 16.2Z"/></svg>"""
    icon_datos = """<svg width="24" height="24" viewBox="0 0 24 24" fill="#E5B25D" xmlns="http://www.w3.org/2000/svg"><path d="M12 2C6.49 2 2 4.69 2 8V16C2 19.31 6.49 22 12 22C17.51 22 22 19.31 22 16V8C22 4.69 17.51 2 12 2ZM12 4C16.97 4 21 6.13 21 8C21 9.87 16.97 12 12 12C7.03 12 3 9.87 3 8C3 6.13 7.03 4 12 4ZM12 20C7.03 20 3 17.87 3 16V14.15C5.03 15.82 8.36 17 12 17C15.64 17 18.97 15.82 21 14.15V16C21 17.87 16.97 20 12 20Z"/></svg>"""

    # ---------------- FUNCIÓN KPI CARD ----------------
    def kpi_card(icon_svg, title, value, delta, title_color):
        st.markdown(f"""
            <div style='
                background-color: #FFFFFF;
                border: 2px solid #E5B25D;
                border-radius: 15px;
                padding: 8px 12px;
                height: 120px;  /* Altura fija */
                box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
                text-align: center;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;  /* Centramos todo */
                gap: 6px;  /* Espacio entre título, número e icono */
                overflow: hidden;
            '>
                <h3 style='
                    color: {title_color}; 
                    font-size: 15px; 
                    margin: 0;
                    overflow: hidden;
                    text-overflow: ellipsis;
                    white-space: nowrap;
                '>{title}</h3>
                <div style='
                    display: flex; 
                    align-items: center; 
                    justify-content: center;
                    margin: 0;
                    flex-wrap: nowrap;
                    max-height: 40px;  /* Control del bloque del número + ícono */
                '>
                    {icon_svg}
                    <h1 style='
                        margin: 0 0 0 10px; 
                        color: #000000; 
                        font-size: 26px;
                        overflow: hidden;
                        text-overflow: ellipsis;
                        white-space: nowrap;
                    '>{value}</h1>
                </div>
                <p style='
                    margin: 0; 
                    font-size: 13px;
                    overflow: hidden;
                    text-overflow: ellipsis;
                    white-space: nowrap;
                '>{delta}</p>
            </div>
        """, unsafe_allow_html=True)

    # ---------------- KPIs ----------------
    col1, col2, col3, col4 = st.columns(4)

    relacion_porcentaje = r_squared * 100  # % basado en R²

    with col1:
        kpi_card(icon_r2, "R² (Coef. Determinación)", f"{r_squared:.4f}", "Proporción de la variabilidad", "#C25E4C")
    with col2:
        kpi_card(icon_r, "r (Coef. Correlación)", f"{correlation:.4f}", "Grado de variación", "#F28C38")
    with col3:
        kpi_card(icon_significativa, "Relación (%)", f"{relacion_porcentaje:.2f}%", "Porcentaje de relación", "#8DA47E")
    with col4:
        kpi_card(icon_datos, "Datos analizados", n_datos, "Registros en el modelo", "#E5B25D")

    # ----------------- HEATMAP SOLO DE Y y X -----------------
    st.subheader("Mapa de calor")

    # Generamos el dataframe solo con las dos variables elegidas
    df_heatmap = df[[variable_dependiente, variable_independiente]]

    # Calculamos la matriz de correlación
    correlation_matrix = df_heatmap.corr().abs()  # Valor absoluto para que siempre sea positivo

    # Creamos el heatmap con Plotly
    fig_heatmap = px.imshow(
        correlation_matrix,
        text_auto=True,
        color_continuous_scale=["#F7C59F", "#E5B25D", "#C25E4C"], 
        labels=dict(color="Correlación"),
        aspect="auto"
    )

    fig_heatmap.update_layout(
        paper_bgcolor="#F4F0EB",  # Fondo cremita
        plot_bgcolor="#F4F0EB",
        xaxis_title="Variables",
        yaxis_title="Variables",
        margin=dict(l=40, r=40, t=40, b=40)
    )

    # Mostrar el heatmap
    st.plotly_chart(fig_heatmap, use_container_width=True)

    # ---------------- HEATMAP INTERACTIVO ----------------
    st.sidebar.subheader("Heatmap general")
    mostrar_heatmap = st.sidebar.button("Generar heatmap")

    if mostrar_heatmap:
        st.subheader("Mapa de calor general")
        
        # ----------------- VARIABLES SELECCIONADAS -----------------
        variables_heatmap = [
            'accommodates',
            'bathrooms',
            'bedrooms',
            'beds',
            'price',
            'minimum_nights',
            'maximum_nights',
            'availability_30',
            'availability_90',
            'availability_365',
            'number_of_reviews',
            'review_scores_rating',
            'review_scores_accuracy',
            'review_scores_cleanliness',
            'review_scores_checkin',
            'review_scores_value'
        ]

        # ----------------- FILTRAR DATOS -----------------
        df_heatmap = df[variables_heatmap]

        # ----------------- CALCULAR CORRELACIÓN -----------------
        correlation_matrix = df_heatmap.corr().abs()  # Correlación en valor absoluto, como en tu práctica

        # ----------------- GENERAR EL HEATMAP -----------------
        import plotly.express as px

        fig_heatmap = px.imshow(
            correlation_matrix,
            text_auto=True,
            color_continuous_scale=["#F7C59F", "#E5B25D", "#C25E4C"],  
            labels=dict(color="Correlación"),
            aspect="auto"
        )

        fig_heatmap.update_layout(
            #paper_bgcolor="#F4F0EB",   # Fondo cremita como en tu app
            #plot_bgcolor="#F4F0EB",
            xaxis_title="Variables",
            yaxis_title="Variables",
            margin=dict(l=40, r=40, t=40, b=40)
        )

        st.plotly_chart(fig_heatmap, use_container_width=True)

# ------------------ VISTA 3 ------------------------------
elif View == "Regresión lineal múltiple":
    st.header("Regresión lineal múltiple")

    # Borrar las columnas del dataframe
    df = df.drop(columns=["longitude", "latitude"], errors="ignore")
    numeric_cols = df.select_dtypes(['float', 'int']).columns

    st.sidebar.subheader("Variables")
    variable_dependiente = st.sidebar.selectbox("Variable dependiente (y)", options=numeric_cols)

    variables_independientes = st.sidebar.multiselect(
        "Variables independientes (X)",
        options=[col for col in numeric_cols if col != variable_dependiente],
        default=[col for col in numeric_cols if col != variable_dependiente][:3]
    )

    if not variables_independientes:
        st.warning("⚠️ Selecciona al menos una variable independiente para continuar.")
    else:
        # --------- FORMULA PARA EL MODELO ---------
        formula = f"{variable_dependiente} ~ {' + '.join(variables_independientes)}"

        from statsmodels.formula.api import ols
        modelo = ols(formula=formula, data=df).fit()

        # --------- GENERAR LAS PREDICCIONES ---------
        df['predicciones'] = modelo.predict(df[variables_independientes])

        # --------- COEFICIENTES Y R², r ---------
        resultados = []
        for var in variables_independientes:
            corr = df[[variable_dependiente, var]].corr().iloc[0, 1]
            coef = modelo.params.get(var, None)
            resultados.append({
                "Variable": var,
                "Coef. Regresión (β)": coef,
                "Correlación (r)": corr
            })

        st.sidebar.subheader("Diagrama comparativo")

        # ----------------- SELECTBOX PARA LA VARIABLE A MOSTRAR -----------------
        variable_seleccionada = st.sidebar.selectbox(
            "Variable independiente (X)",
            options=variables_independientes
        )

        # ----------------- SCATTERPLOT ORIGINAL -----------------
        st.subheader("Diagrama de dispersión")

        # Creamos un dataframe largo (long format) para graficar las variables independientes originales
        df_long_original = pd.melt(
            df,
            id_vars=[variable_dependiente],
            value_vars=variables_independientes,
            var_name='Variable Independiente',
            value_name='Valor'
        )

        # Ahora sí el scatterplot para los datos originales:
        fig_scatter_original = px.scatter(
            df_long_original,
            x='Valor',
            y=variable_dependiente,
            color='Variable Independiente',
            labels={'Valor': 'Variables independientes', variable_dependiente: variable_dependiente},
            color_discrete_sequence=custom_palette  # Usando la paleta personalizada
        )

        fig_scatter_original.update_traces(marker=dict(size=5), selector=dict(mode='markers'))
        fig_scatter_original.update_layout(
            xaxis_title="Variables independientes",
            yaxis_title=variable_dependiente,
            legend_title="Variable independiente",
        )

        st.plotly_chart(fig_scatter_original, use_container_width=True)

        # ---------------- Tabla ----------------
        resultados_df = pd.DataFrame(resultados)
        st.subheader("Coeficientes del modelo y correlaciones")
        st.dataframe(resultados_df)

        # ---------------- Indicadores ----------------
        st.subheader("Indicadores del modelo")

        # ---------------- ÍCONOS SVG ----------------
        icon_r2 = """<svg width="24" height="24" viewBox="0 0 24 24" fill="#E5B25D" xmlns="http://www.w3.org/2000/svg"><path d="M12 2C6.49 2 2 4.69 2 8V16C2 19.31 6.49 22 12 22C17.51 22 22 19.31 22 16V8C22 4.69 17.51 2 12 2ZM12 4C16.97 4 21 6.13 21 8C21 9.87 16.97 12 12 12C7.03 12 3 9.87 3 8C3 6.13 7.03 4 12 4ZM12 20C7.03 20 3 17.87 3 16V14.15C5.03 15.82 8.36 17 12 17C15.64 17 18.97 15.82 21 14.15V16C21 17.87 16.97 20 12 20Z"/></svg>"""
        icon_r = """<svg width="24" height="24" viewBox="0 0 24 24" fill="#E5B25D" xmlns="http://www.w3.org/2000/svg"><path d="M12 2C6.49 2 2 4.69 2 8V16C2 19.31 6.49 22 12 22C17.51 22 22 19.31 22 16V8C22 4.69 17.51 2 12 2ZM12 4C16.97 4 21 6.13 21 8C21 9.87 16.97 12 12 12C7.03 12 3 9.87 3 8C3 6.13 7.03 4 12 4ZM12 20C7.03 20 3 17.87 3 16V14.15C5.03 15.82 8.36 17 12 17C15.64 17 18.97 15.82 21 14.15V16C21 17.87 16.97 20 12 20Z"/></svg>"""
        icon_significativa = """<svg width="24" height="24" viewBox="0 0 24 24" fill="#8DA47E" xmlns="http://www.w3.org/2000/svg"><path d="M9 16.2L4.8 12L3.4 13.4L9 19L21 7L19.6 5.6L9 16.2Z"/></svg>"""
        icon_datos = """<svg width="24" height="24" viewBox="0 0 24 24" fill="#E5B25D" xmlns="http://www.w3.org/2000/svg"><path d="M12 2C6.49 2 2 4.69 2 8V16C2 19.31 6.49 22 12 22C17.51 22 22 19.31 22 16V8C22 4.69 17.51 2 12 2ZM12 4C16.97 4 21 6.13 21 8C21 9.87 16.97 12 12 12C7.03 12 3 9.87 3 8C3 6.13 7.03 4 12 4ZM12 20C7.03 20 3 17.87 3 16V14.15C5.03 15.82 8.36 17 12 17C15.64 17 18.97 15.82 21 14.15V16C21 17.87 16.97 20 12 20Z"/></svg>"""

        # ---------------- FUNCIÓN KPI CARD ----------------
        def kpi_card(icon_svg, title, value, delta, title_color):
            st.markdown(f"""
                <div style='
                    background-color: #FFFFFF;
                    border: 2px solid #E5B25D;
                    border-radius: 15px;
                    padding: 8px 12px;
                    height: 120px;  /* Altura fija */
                    box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
                    text-align: center;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;  /* Centramos todo */
                    gap: 6px;  /* Espacio entre título, número e icono */
                    overflow: hidden;
                '>
                    <h3 style='
                        color: {title_color}; 
                        font-size: 15px; 
                        margin: 0;
                        overflow: hidden;
                        text-overflow: ellipsis;
                        white-space: nowrap;
                    '>{title}</h3>
                    <div style='
                        display: flex; 
                        align-items: center; 
                        justify-content: center;
                        margin: 0;
                        flex-wrap: nowrap;
                        max-height: 40px;  /* Control del bloque del número + ícono */
                    '>
                        {icon_svg}
                        <h1 style='
                            margin: 0 0 0 10px; 
                            color: #000000; 
                            font-size: 26px;
                            overflow: hidden;
                            text-overflow: ellipsis;
                            white-space: nowrap;
                        '>{value}</h1>
                    </div>
                    <p style='
                        margin: 0; 
                        font-size: 13px;
                        overflow: hidden;
                        text-overflow: ellipsis;
                        white-space: nowrap;
                    '>{delta}</p>
                </div>
            """, unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)

        r_squared = modelo.rsquared
        n_datos = df[[variable_dependiente] + variables_independientes].dropna().shape[0]
        relacion_porcentaje = r_squared * 100  # Relación significativa en %

        with col1:
            kpi_card(icon_r2, "R² (Coef. Determinación)", f"{r_squared:.4f}", "Proporción de la variabilidad", "#C25E4C")
        with col2:
            kpi_card(icon_r, "Promedio r (Correlación)", f"{resultados_df['Correlación (r)'].mean():.4f}", "Grado de variación promedio", "#F28C38")
        with col3:
            kpi_card(icon_significativa, "Relación (%)", f"{relacion_porcentaje:.2f}%", "Porcentaje de relación significativa", "#8DA47E")
        with col4:
            kpi_card(icon_datos, "Datos analizados", n_datos, "Registros utilizados en el modelo", "#E5B25D")


        # ----------------- SCATTERPLOT CON PREDICCIONES -----------------
        st.subheader(f"Diagrama comparativo")

        # Creamos un dataframe largo (long format) para graficar la variable seleccionada y las predicciones
        df_long_predicciones = pd.melt(
            df,
            id_vars=[variable_dependiente],
            value_vars=[variable_seleccionada, 'predicciones'],  # Solo la variable seleccionada y las predicciones
            var_name='Variable',
            value_name='Valor'
        )

        # Ahora sí el scatterplot para los datos reales y las predicciones de la variable seleccionada:
        fig_scatter_predicciones = px.scatter(
            df_long_predicciones,
            x='Valor',
            y=variable_dependiente,
            color='Variable',  # Diferencia entre valores reales y predichos
            labels={'Valor': f'{variable_seleccionada}', variable_dependiente: variable_dependiente},
            color_discrete_sequence=["#C25E4C", "#E5B25D"]  # Usando la paleta personalizada
        )

        fig_scatter_predicciones.update_traces(marker=dict(size=5), selector=dict(mode='markers'))
        fig_scatter_predicciones.update_layout(
            xaxis_title=f"{variable_seleccionada} ",
            yaxis_title=variable_dependiente,
            legend_title="Variable / Predicción",
        )

        st.plotly_chart(fig_scatter_predicciones, use_container_width=True)

        # -------- HEATMAP DE VARIABLES SELECCIONADAS ---------
        st.sidebar.subheader("Heatmap")
        mostrar_heatmap = st.sidebar.button("Generar heatmap")

        if mostrar_heatmap:
            st.subheader("Mapa de calor")

            df_heatmap = df[[variable_dependiente] + variables_independientes]
            correlation_matrix = df_heatmap.corr().abs()

            fig_heatmap = px.imshow(
                correlation_matrix,
                text_auto=True,
                color_continuous_scale=["#F7C59F", "#E5B25D", "#C25E4C"],  
                labels=dict(color="Correlación"),
                aspect="auto"
            )

            fig_heatmap.update_layout(
                paper_bgcolor="#F4F0EB",
                plot_bgcolor="#F4F0EB",
                xaxis_title="Variables",
                yaxis_title="Variables",
                margin=dict(l=40, r=40, t=40, b=40)
            )

            st.plotly_chart(fig_heatmap, use_container_width=True)

# ------------------ VISTA 4 ------------------------------
elif View == "Regresión logística":
    st.header("Regresión logística")

    # ------------ VARIABLES DEPENDIENTES (BINARIAS) ------------
    variables_dependientes_log = [
        'host_is_superhost',
        'instant_bookable',
        'host_identity_verified',
        'has_availability'
    ]

    # ------------ VARIABLES INDEPENDIENTES -------------------
    variables_independientes_log = [
        'number_of_reviews', 'review_scores_rating',
        'review_scores_accuracy', 'review_scores_cleanliness',
        'review_scores_checkin', 'review_scores_communication',
        'review_scores_location', 'review_scores_value',
        'host_response_rate', 'host_acceptance_rate',
        'availability_365', 'availability_30', 'availability_90',
        'host_listings_count', 'minimum_nights', 'accommodates',
        'price', 'beds'
    ]

    # ------------ SIDEBAR -----------------
    st.sidebar.subheader("Variables")
    variable_dependiente = st.sidebar.selectbox("Variable dependiente (Y)", options=variables_dependientes_log)
    variables_independientes = st.sidebar.multiselect("Variables independientes (X)", options=variables_independientes_log,  default=variables_independientes_log[:3] ) 

    if not variables_independientes:
        st.warning("⚠️ Selecciona al menos una variable independiente para continuar.")
    else:
        # ----------------- PREPARAR DATOS -----------------
        from sklearn.linear_model import LogisticRegression
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix, roc_auc_score, roc_curve
        import numpy as np

        # Limpieza de datos: eliminamos NaN
        data = df[[variable_dependiente] + variables_independientes].dropna()

        # Transformar la variable dependiente (Sí/No a 1/0 si es texto)
        if data[variable_dependiente].dtype == 'object':
            data[variable_dependiente] = data[variable_dependiente].apply(lambda x: 1 if x in ['Yes', 't', 'Sí', 'si', 'TRUE', 'True'] else 0)

        X = data[variables_independientes]
        y = data[variable_dependiente]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

        model = LogisticRegression(max_iter=1000)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        y_proba = model.predict_proba(X_test)[:, 1]

        # ----------------- MATRIZ DE CONFUSIÓN -----------------
        cm = confusion_matrix(y_test, y_pred)
        st.subheader("Matriz de confusión")
        st.write(pd.DataFrame(cm, columns=["Pred. Negativo", "Pred. Positivo"], index=["Real Negativo", "Real Positivo"]))

        st.subheader("Heatmap de la matriz de confusión")
        import plotly.express as px
        fig_cm = px.imshow(cm, text_auto=True, color_continuous_scale=["#F7C59F", "#E5B25D", "#C25E4C"])
        fig_cm.update_layout(xaxis_title="Predicción", yaxis_title="Real")
        st.plotly_chart(fig_cm, use_container_width=True)

        # ----------------- MÉTRICAS -----------------
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)

        # ----------------- FUNCIÓN MÉTRICAS-----------------
        def kpi_card_metric(title, value, delta, title_color):
            st.markdown(f"""
                <div style='
                    background-color: #FFFFFF;
                    border: 2px solid #E5B25D;
                    border-radius: 15px;
                    padding: 10px 16px;
                    height: 100px;  
                    box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
                    text-align: center;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;  
                    overflow: hidden;
                '>
                    <div style='margin: 0; padding: 0; line-height: 1.1;'>  <!-- Aquí se hace el truco -->
                        <span style='
                            color: {title_color}; 
                            font-size: 20px; 
                            margin: 0;
                            padding: 0;
                        '>{title}</span><br>
                        <span style='
                            color: #000000; 
                            font-size: 25px;
                            font-weight: bold;
                            margin: 0;
                            padding: 0;
                        '>{value}</span>
                    </div>
                    <p style='
                        margin: 4px 0 0 0; 
                        font-size: 13px;
                        color: #555555;
                        overflow: hidden;
                        text-overflow: ellipsis;
                        white-space: nowrap;
                    '>{delta}</p>
                </div>
            """, unsafe_allow_html=True)

        # ----------------- MÉTRICAS COMO KPIs -----------------
        st.subheader("Métricas del modelo")

        col1, col2, col3 = st.columns(3)

        with col1:
            kpi_card_metric("Precisión", f"{precision:.2%}", "Relación positivos predichos correctamente", "#C25E4C")
        with col2:
            kpi_card_metric("Exactitud", f"{accuracy:.2%}", "Proporción total de aciertos", "#F28C38")
        with col3:
            kpi_card_metric("Sensibilidad", f"{recall:.2%}", "Capacidad de encontrar positivos reales", "#8DA47E")

        # ----------------- LINEPLOT DE MEJORA DEL MODELO -----------------
        if len(variables_independientes) > 1:  # Solo si hay más de una variable
            st.subheader("Evolución del modelo")

            metrics_data = []

            for i in range(1, len(variables_independientes) + 1):
                selected_vars = variables_independientes[:i]

                X = data[selected_vars]
                y = data[variable_dependiente]

                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

                model = LogisticRegression(max_iter=1000)
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)

                acc = accuracy_score(y_test, y_pred)
                prec = precision_score(y_test, y_pred)
                rec = recall_score(y_test, y_pred)

                metrics_data.append({
                    'Variables usadas': ', '.join(selected_vars),
                    'Número de variables': i,
                    'Precisión': prec,
                    'Exactitud': acc,
                    'Sensibilidad': rec
                })

            metrics_df = pd.DataFrame(metrics_data)

            # Lineplot de las métricas
            fig_metrics = px.line(
                metrics_df,
                x='Número de variables',
                y=['Precisión', 'Exactitud', 'Sensibilidad'],
                markers=True,
                labels={"value": "Métrica", "variable": "Tipo de métrica", "Número de variables": "Número de variables"},
                color_discrete_sequence=custom_palette
            )

            fig_metrics.update_layout(
                legend_title="Métrica",
                xaxis=dict(tickmode='linear', dtick=1)
            )

            st.plotly_chart(fig_metrics, use_container_width=True)

        # ----------------- TABLA DE MÉTRICAS POR VARIABLES -----------------
        st.subheader("Tabla de la evolución del modelo")

        # Quitamos la columna 'Número de variables'
        metrics_df_tabla = metrics_df[['Variables usadas', 'Precisión', 'Exactitud', 'Sensibilidad']]

        # Mostramos la tabla
        st.dataframe(metrics_df_tabla)
