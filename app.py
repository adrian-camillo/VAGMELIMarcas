import streamlit as st
import pandas as pd
import plotly.express as px

# Carga de datos
def load_data():
    df = pd.read_csv('Ventas por Artículo (7).csv', encoding="ISO-8859-1", delimiter=';')
    df['Fecha'] = pd.to_datetime(df['Fecha'], dayfirst=True)
    
    # Convertir columnas con comas en decimales a float
    df['Cantidad'] = df['Cantidad'].str.replace(',', '.').astype(float)
    
    return df

df = load_data()

# Título de la aplicación
st.title('Análisis de Ventas por Marca')

# Selección de Rango de Fechas
fecha_min = df['Fecha'].min().date()
fecha_max = df['Fecha'].max().date()
fecha_inicio, fecha_fin = st.date_input('Selecciona un rango de fechas:', [fecha_min, fecha_max])
fecha_inicio = pd.Timestamp(fecha_inicio)
fecha_fin = pd.Timestamp(fecha_fin)

df_filtrado = df[(df['Fecha'] >= fecha_inicio) & (df['Fecha'] <= fecha_fin)]
df_filtrado = df_filtrado[df_filtrado['Cantidad'] >= 0]

# Agrupamos por Fecha y Marca para obtener la suma de las cantidades vendidas por marca en cada fecha
df_grouped = df_filtrado.groupby(['Fecha', 'Marca']).agg({'Cantidad': 'sum'}).reset_index()

# Seleccionamos las marcas con las mayores cantidades vendidas en el rango de fechas seleccionado
top_marcas = df_grouped.groupby('Marca').agg({'Cantidad': 'sum'}).sort_values(by='Cantidad', ascending=False)

# Permitimos al usuario seleccionar cuántas marcas quiere visualizar o seleccionar marcas individuales
all_marcas = top_marcas.index.tolist()
options = ['TODO'] + all_marcas
selected_marcas = st.multiselect('Selecciona las marcas a mostrar:', options, default='TODO')

if 'TODO' in selected_marcas:
    num_marcas = st.slider('Selecciona el número de marcas principales a mostrar:', 1, len(all_marcas), 5)
    marcas_seleccionadas = all_marcas[:num_marcas]
else:
    marcas_seleccionadas = selected_marcas

# Filtramos el dataframe para solo incluir las marcas seleccionadas
df_final = df_grouped[df_grouped['Marca'].isin(marcas_seleccionadas)]

# Generar gráfico de líneas
fig = px.line(df_final, x='Fecha', y='Cantidad', color='Marca', title=f"Tendencia de ventas por Marca")

fig.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",  # Fondo transparente
    xaxis_title="Fecha",
    yaxis_title="Cantidad",
    xaxis_tickangle=-90  # Etiquetas del eje X rotadas a 90 grados
)

st.plotly_chart(fig)
