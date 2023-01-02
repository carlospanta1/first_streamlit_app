
import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

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

#CREACION DE LA FUNCION
def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
    #extrae la version json de la respuesta y la normaliza
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())  
    return fruityvice_normalized

#SECCION PARA MOSTRAR FRUITYVICE API
try:
    #codigo para extraer via streamlit
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
        streamlit.error("Please select a fruit to get information.")
    else:
        back_from_function = get_fruityvice_data(fruit_choice)
        #muestra como tabla la información
        streamlit.dataframe(back_from_function)
        
except URLError as e:
    streamlit.error()
          

streamlit.write('The user entered ', fruit_choice)

#import requests

#streamlit.text(fruityvice_response.json()) #solo escribe la data en la pantalla   #estaba originalmente pero ya no se usa



#streamlit.stop()

#import snowflake.connector


streamlit.header("The fruit load list contains:")
#Snowflake-related functions
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
         my_cur.execute("select * from fruit_load_list")
         return my_cur.fetchall()
 
#Add a button to load the fruit
if streamlit.button('Get Fruit Load List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"]) 
    my_data_rows = get_fruit_load_list()
    my_cnx.close()
    streamlit.dataframe(my_data_rows)

#permite al usuario añadir frutas a la lista
def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
         my_cur.execute("insert into fruit_load_list values ('"+ new_fruit +"')")
         return "Thanks for adding " + new_fruit


#codigo para agregar la fruta
def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
         my_cur.execute("insert into fruit_load_list values ('from streamlit')")
         return "Thanks for adding "+ new_fruit
         
add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a Fruit to the List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function = insert_row_snowflake(add_my_fruit)
    streamlit.text(back_from_function)
    




