
import streamlit
import pandas

streamlit.title('Breakfast Favorites')

streamlit.header('Breakfast Menu')
streamlit.text('🥣Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞Avocado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

#se extrae la lista de frutas desde el bucket de s3
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

#se puso como index el nombre de la fruta para elegir
my_fruit_list = my_fruit_list.set_index('Fruit')

#se añade una lista de selección para poder elegir la fruta
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])

#se añadió una función para mostrar solo la fruta seleccionada en la lista
fruits_to_show = my_fruit_list.loc[fruits_selected]

#mostrar la tabla en la página
streamlit.dataframe(fruits_to_show)

#SECCIÓN PARA MOSTRAR FRUITYVICE API 
streamlit.header("Fruityvice Fruit Advice!")

#codigo para extraer via streamlit
fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)

import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
#streamlit.text(fruityvice_response.json()) #solo escribe la data en la pantalla   #estaba originalmente pero ya no se usa

#extrae la version json de la respuesta y la normaliza
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())

#muestra como tabla la información
streamlit.dataframe(fruityvice_normalized)

import snowflake.connector

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_data_row = my_cur.fetchone()
streamlit.text("Hello from Snowflake:")
streamlit.text(my_data_row)



