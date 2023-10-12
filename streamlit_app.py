import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('Zenas Amaizing Athleisure Catalog')

#import pandas
my_clothes_list = pandas.read_txt("https://uni-klaus.s3.us-west-2.amazonaws.com/swt_product_line.txt")
my_clothes_list = my_clothes_list.set_index('clothes')
# Let's put a pick list here so they can pick the clothes 
clothes_selected = streamlit.multiselect("Pick sweatsuit color or style:", list(my_clothes_list.index))
clothes_to_show = my_clothes_list.loc[clothes_selected]
# Display the table on the page.
streamlit.dataframe(clothes_to_show)

streamlit.stop()

# create the repeatable code block (called a function)
def get_fruityvice_data(this_fruit_choice):
#def get_fruityvice_data(banana):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

#new section to display fruityvice api response
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?') #banana 
  #streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select fruit to get information.")
  else:
    #fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    #fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    back_from_function = get_fruityvice_data(fruit_choice)
    #back_from_function = fruityvice_normalized 
    #back_from_function =  get_fruityvice_data(fruit_choice)
    #streamlit.dataframe(fruityvice_normalized)
    streamlit.dataframe(back_from_function)
    #back_from_function

except URLError as e:
    streamlit.error()





streamlit.stop()

#import requests

# fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
# streamlit.text(fruityvice_response.json())

# write your own comment -what does the next line do? 
# fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# write your own comment - what does this do?
# streamlit.dataframe(fruityvice_normalized)

# don't run anything below here while we troubleshoot
streamlit.stop()

#import snowflake.connector

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from fruit_load_list")
my_data_row = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_row)

# Allow the end user to add a fruit to the list
add_my_fruit = streamlit.text_input('What fruit would you like to add?','e.g. jackfruit')
streamlit.write('Thanks for adding ', add_my_fruit)

my_cur.execute("insert into fruit_load_list values ('from streamlit')")
