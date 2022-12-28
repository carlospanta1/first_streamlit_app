
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
streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])

#se añadió una función para mostrar solo la fruta seleccionada en la lista
fruits_to_show = my_fruit_list.loc[fruits_selected]

#mostrar la tabla en la página
streamlit.dataframe(my_fruit_list)



