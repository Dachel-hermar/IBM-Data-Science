# Import required libraries
import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output

# Load the dataset
data = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")
print(data.head())
print(data.columns)
print(f"Los sitios de lanzamientos son: {data['Launch Site'].unique()}")

# Create a Dash application
app = dash.Dash(__name__)


# Ejercise 1: Agregar un Componente de Entrada de Desplegable para el Sitio de Lanzamiento
# Tenemos cuatro sitios de lanzamiento diferentes y nos gustaría primero ver cuál tiene la mayor cantidad de éxitos. Luego, nos gustaría seleccionar un sitio específico y verificar su tasa de éxito detallada (clase=0 vs. clase=1).
# Por lo tanto, necesitaremos un menú desplegable que nos permita seleccionar diferentes sitios de lanzamiento
# atributo value con el valor predeterminado del desplegable como ALL, lo que significa que se seleccionan todos los sitios
# atributo placeholder para mostrar una descripción de texto sobre esta área de entrada, como Select a Launch Site here
# atributo searchable para ser True para que podamos ingresar palabras clave para buscar sitios de lanzamiento
app.layout = html.Div([
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'},
            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
            
        ],
        value='ALL',
        placeholder="Select a Launch Site here",
        searchable=True 
    ),
    dcc.Graph(
        id='success-pie-chart'
    ),
    # TAREA 3: Agregar un Control deslizante de rango para seleccionar la carga útil
    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=10000,
        step=1000,
        value=[0, 10000],
        marks={i : str(i) for i in range(0, 10001, 2000)}
    ),
    dcc.Graph(
        id='success-payload-scatter-chart'
    )
])

# TAREA 2: Agregar una función de callback para renderizar success-pie-chart basado en el sitio seleccionado en el menú desplegable
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def update_pie_chart(selected_site):
    # Filtrar los datos para todos los sitios
    filtered_data = data
    if selected_site == 'ALL':
        # Crear un gráfico circular de éxito para todos los sitios
        fig = px.pie(filtered_data, names='Launch Site', values='class', title='Total Success Launches by Site')
    else:
        # Filtrar los datos para el sitio seleccionado
        filtered_data = data[data['Launch Site'] == selected_site]
        # Crear un gráfico circular de éxito para el sitio seleccionado
        fig = px.pie(filtered_data, names='class', title=f'Total Success Launches for site {selected_site}')
    
    return fig

# TAREA 4: Agregar una función de callback para renderizar success-payload-scatter-chart basado en el sitio seleccionado y el rango de carga útil
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def update_scatter_chart(selected_site, payload_range):
    # Filtrar los datos para el sitio seleccionado
    filtered_data = data
    if selected_site == 'ALL':
        # Filtrar los datos para todos los sitios por rango de carga útil
        filtered_data = data[(data['Payload Mass (kg)'] >= payload_range[0]) & (data['Payload Mass (kg)'] <= payload_range[1])] # Filtrar por rango de carga útil
        # Crear un gráfico de dispersión de éxito por carga útil para todos los sitios
        fig = px.scatter(filtered_data, x='Payload Mass (kg)', y='class', color='Booster Version', title='Success Launches by Payload Mass for all sites')
    else:
        # Filtrar los datos para el sitio seleccionado
        filtered_data = data[data['Launch Site'] == selected_site]
        # Filtrar los datos para el sitio seleccionado
        filtered_data = data[(data['Launch Site'] == selected_site) & (data['Payload Mass (kg)'] >= payload_range[0]) & (data['Payload Mass (kg)'] <= payload_range[1])] # Filtrar por rango de carga útil
    # Crear un gráfico de dispersión de éxito por carga útil
        fig = px.scatter(filtered_data, x='Payload Mass (kg)', y='class', color='Booster Version', title=f'Success Launches by Payload Mass for site {selected_site}')
    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)