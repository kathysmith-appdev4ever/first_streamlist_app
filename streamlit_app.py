import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError  # -- New Import for Control Flow error message handling

streamlit.title('My Mom\'s New Healthy Diner')

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.title('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# import pandas -- Moved to the top
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page
streamlit.dataframe(fruits_to_show)

# =================================================================================================
# Create the repeatable code block (called a function)
def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())  # Take the JSON version of the response and normalize it
  return fruityvice_normalized
# =================================================================================================

# =================================================================================================
# New Section to display frutiyvice api response - New Code with Control Flow and Error Handling
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)                 # Output it to the screen as a table

    # ---------------------------------------------------------------------------------------
    # fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    # fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())  # Take the JSON version of the response and normalize it
    # streamlit.dataframe(fruityvice_normalized)                                 # Output it to the screen as a table
    # ---------------------------------------------------------------------------------------
except URLError as e:
    streamlit.error()
# =================================================================================================

# =================================================================================================
# Old Code with No Control Flow and No Error Handling
# New Section to display frutiyvice api response
# streamlit.header("Fruityvice Fruit Advice!")
# streamlit.write('The user entered ', fruit_choice)

# import requests -- Moved to the top
# fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)

# Take the JSON version of the response and normalize it
# fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# Output it to the screen as a table
# streamlit.dataframe(fruityvice_normalized)
# =================================================================================================

# import snowflake.connector -- Moved to the top

# =================================================================================================
# streamlit.header("The fruit load list contains:")
# my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
# my_cur = my_cnx.cursor()
# my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
# my_cur.execute("select * from fruit_load_list")
# my_data_row = my_cur.fetchone()
# my_data_rows = my_cur.fetchall()
# streamlit.text("Hello from Snowflake:")
# streamlit.text("The fruit load list contains: ")
# streamlit.text(my_data_row)
   
# streamlit.dataframe(my_data_row)
# streamlit.dataframe(my_data_rows)
# =================================================================================================

# =================================================================================================
# streamlit.header("The fruit load list contains:")
streamlit.header("View Our Fruit List - Add Your Favorites!")

# Snowflake-Related Functions
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
       my_cur.execute("select * from fruit_load_list")
       return my_cur.fetchall()
      
# Add a button to load the fruit
if streamlit.button('Get Fruit List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  my_cnx.close()  # Close Snowflake Connection
  streamlit.dataframe(my_data_rows)
# =================================================================================================

# -- Don't run anything past here while we troubleshoot --
# streamlit.stop()

# =================================================================================================
# Allow the end user to add a fruit to the list
# add_my_fruit = streamlit.text_input('What fruit would you like to add?', 'jackfruit')
# streamlit.write('Thanks for adding ', add_my_fruit)

# This will not work correctly, but just go with it for now.
# It has a control flow issue.  This piece of code is executing everytime we interact with the page.
# It should on execute when we want to add a fruit.
# my_cur.execute("insert into fruit_load_list values ('from streamlit')")
# =================================================================================================

# =================================================================================================
# Allow the end user to add a fruit to the list
def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
       my_cur.execute("insert into fruit_load_list values ('" + new_fruit + "')")
       return "Thanks for adding " + new_fruit
      
add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a Fruit to the List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  back_from_function = insert_row_snowflake(add_my_fruit)
  my_cnx.close()  # Close Snowflake Connection
  streamlit.text(back_from_function)
# =================================================================================================
