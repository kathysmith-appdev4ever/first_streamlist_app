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
# New Code with Control Flow and Error Handling
# New Section to display frutiyvice api response
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?', 'Kiwi')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    # Take the JSON version of the response and normalize it
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    # Output it to the screen as a table
    streamlit.dataframe(fruityvice_normalized)
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

# -- Don't run anything past here while we troubleshoot --
streamlit.stop()

# import snowflake.connector -- Moved to the top

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
# my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_cur.execute("select * from fruit_load_list")
# my_data_row = my_cur.fetchone()
my_data_rows = my_cur.fetchall()
# streamlit.text("Hello from Snowflake:")
# streamlit.text("The fruit load list contains: ")
# streamlit.text(my_data_row)

streamlit.header("The fruit load list contains:")
# streamlit.dataframe(my_data_row)
streamlit.dataframe(my_data_rows)

# Allow the end user to add a fruit to the list
add_my_fruit = streamlit.text_input('What fruit would you like to add?', 'jackfruit')
streamlit.write('Thanks for adding ', add_my_fruit)

# This will not work correctly, but just go with it for now.
# It has a control flow issue.  This piece of code is executing everytime we interact with the page.
# It should on execute when we want to add a fruit.
my_cur.execute("insert into fruit_load_list values ('from streamlit')")
