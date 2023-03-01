#these are the libraries used for these sns.twitter scrape methods using a customizes streamlit website
import streamlit as st
import base64
from PIL import Image
import snscrape.modules.twitter as sntwitter
import numpy as np
import datetime
import json
import matplotlib.pyplot as plt
from wordcloud import WordCloud
#from wordcloud import STOPWORDS
import pandas as pd
from pymongo import MongoClient
from streamlit_option_menu import option_menu

#connecting MongoDB-Database and creating a collection
conn = MongoClient("mongodb+srv://danavasanth:Krishnaveni@cluster0.0azflq3.mongodb.net/?retryWrites=true&w=majority")
db = conn["snscrape"]
coll = db["twitter-data"]
img = Image.open("C:/Users/DELL/Desktop/Twitter--scraping-main/media/twitter.png")
st.set_page_config(page_title="Twitter scraping",page_icon = img,layout = "wide")

#This is used to make the streamlit web-page customized
def get_img_as_base64(file):
    with open(file,"rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()
img = get_img_as_base64("C:/Users/DELL/Desktop/Twitter--scraping-main/images/twitter-splash.jpg")
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image :url("data:image/png;base64,{img}");
background-size : cover;
}}
[data-testid="stHeader"]{{
background:rgba(0,0,0,0);
}}
</style>

"""
st.markdown(page_bg_img, unsafe_allow_html=True)
st.header("TWITTER SCRAPPING USING SNSCRAPE")

#It enables user to scrape the data from twitter using "snscrape"
def ScrapingTheBird(word,From,To,maxTweets):
  tweets_list = []
  for i,tweet in enumerate(sntwitter.TwitterSearchScraper(f'{word} since:{From} until:{To}').get_items()):
      if i>maxTweets-1:
          break
      tweets_list.append([tweet.date,tweet.id,tweet.user.username,tweet.url,tweet.rawContent,tweet.replyCount,tweet.likeCount,tweet.retweetCount,tweet.lang,tweet.source ])
  tweets_df = pd.DataFrame(tweets_list, columns=['Datetime', 'Tweet Id','User Name','URL','Content','ReplyCount','LikeCount','Retweet-Count','Language','Source'])
  tweets_df.to_json("user-tweets.json")
  tweets_df.to_csv("user-tweets.csv")
  return tweets_df

#It is to visualize the most frequent word used by peoples along with the search word in wordcloud form
def word_cloud():
   # stopwords = set(STOPWORDS)
    data = pd.read_csv("user-tweets.csv")
    mask = np.array(Image.open("C:/Users/DELL/Desktop/Twitter--scraping-main/media/tweetie.png"))
    text = " ".join(review for review in data.Content)
    wordcloud = WordCloud(background_color = "white",max_words=500,mask=mask).generate(text)
    plt.figure()
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()
    plt.savefig("C:/Users/DELL/Desktop/Twitter--scraping-main/media/word-cloud.png",format="png")
    return plt.show()

#It is to upload the search document in Mongodb database
def Bird_In_Database(n_word):
    with open("user-tweets.json","r") as file:
        data = json.load(file)
    dt = datetime.datetime.today()
    db.twitter_data.insert_many([{
            "Key-Word":n_word,
            "datetime":dt,
            "Data":data
            }])

#creating a navigation menu used to select the user to what to visible and perform
#with st.sidebar:
choice = option_menu(
    menu_title = None,
    options = ["Search","Visualize","Home","Data-Base","Download","Contact"],
    icons =["search","camera2","house","boxes","download","at"],
    default_index=3,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "white","size":"cover"},
        "icon": {"color": "cyan", "font-size": "20px"},
        "nav-link": {"font-size": "20px", "text-align": "center", "margin": "-2px", "--hover-color": "#29BDE9 "},
        "nav-link-selected": {"background-color": "black"},}
    )
#It remains default web-page
if choice=="Home":
    col1, col2,col3 = st.columns(3)
    col1.image(Image.open("C:/Users/DELL/Desktop/Twitter--scraping-main/media/tweet.png"),width = 500)
    col2.header("“There are NO magic wands, NO hidden tracks, NO secret handshakes that can bring you immediate success..! But with Time, Energy and Determination you can get there...!”")
    col3.image(Image.open("C:/Users/DELL/Desktop/Twitter--scraping-main/media/smiles.png"),width = 500)

#It enables user to search the key-word , from date , to date and no of datas
if choice=="Search":
    col1,col2,col3 = st.columns(3)
    col1.image(Image.open("C:/Users/DELL/Desktop/Twitter--scraping-main/media/blue-tick.png"),width = 250)
    col2.image(Image.open("C:/Users/DELL/Desktop/Twitter--scraping-main/media/search.png"),width = 400)
    col3.image(Image.open("C:/Users/DELL/Desktop/Twitter--scraping-main/media/database.png"),width= 250)                     
    word = st.text_input("Enter Word to Search")
    if word:
        From = st.date_input("From Date")
        if From:
            To = st.date_input("To Date")
            if To:
                maxTweets = st.number_input("Number of Tweets",1,1000)
                if maxTweets:
                    check = st.button("Caught the Bird")
                    if check:
                        st.dataframe(ScrapingTheBird(word,From,To,maxTweets).iloc[0:10])
                        col1, col2 = st.columns(2)
                        col1.image(Image.open("C:/Users/DELL/Desktop/Twitter--scraping-main/media/smiles.png"))
                        col2.image(Image.open("C:/Users/DELL/Desktop/Twitter--scraping-main/media/thumbsup.png"))
                        st.snow()

#It enables user to visualize the data in wordcloud form with similar tag's
if choice=="Visualize":
    col1,col2,col3= st.columns(3)
    col1 = (st.button("Click to here to Release :bird:"))
    col2.image(Image.open("C:/Users/DELL/Desktop/Twitter--scraping-main/media/cage bird.png"),width = 250)
    if (col1):
        st.balloons()
        word_cloud()
        col3.image(Image.open("C:/Users/DELL/Desktop/Twitter--scraping-main/C:/Users/DELL/Desktop/Twitter--scraping-main/media/word-cloud.png"))

#It enables user to download the search data in JSON or CSV file
if choice=="Download":
    col1,col2,= st.columns(2)
    col1.image(Image.open("C:/Users/DELL/Desktop/Twitter--scraping-main/media/bell.png"),width = 300)
    col2.header("*You can Download the previous search data ( or ) You can search for new-data")
    choice1 = ["--SELECT-OPTIONS--", "Pre-Search-data", "New-Search"]
    menu=st.selectbox("SELECT", choice1)
    if menu=="Pre-Search-data":
        with open("user-tweets.csv") as CSV:
            if st.download_button("DOWNLOAD THE BIRD IN --> .csv ",CSV,file_name="My-Blue-Bird.csv"):
                st.image("C:/Users/DELL/Desktop/Twitter--scraping-main/media/baby-right.png",width = 250)
                st.success("My-Blue-Bird.csv..! has been downloaded")
        with open("user-tweets.json") as JSON:
            if st.download_button("DOWNLOAD THE BIRD IN --> .json",JSON,file_name="My-Blue-Bird.json"):
                st.image("C:/Users/DELL/Desktop/Twitter--scraping-main/media/baby-left.png",width = 250)
                st.success("My-Blue-Bird.json..! has been downloaded")

    if menu=="New-Search":
        word = st.text_input("Enter Word to Search")
        if word:
            From = st.date_input("From Date")
            if From:
                To = st.date_input("To Date")
                if To:
                    maxTweets = st.number_input("Number of Tweets", 1, 1000)
                    if maxTweets:
                        check = st.button("Caught the Bird")
                        if check:
                            st.dataframe(ScrapingTheBird(word, From, To, maxTweets).iloc[0:10])
                            with open("user-tweets.csv") as CSV:
                                st.download_button("DOWNLOAD THE BIRD IN --> .csv ", CSV,file_name="My-Blue-Bird.csv")
                            with open("user-tweets.json") as JSON:
                                st.download_button("DOWNLOAD THE BIRD IN --> .json", JSON,file_name="My-Blue-Bird.json")

#It is to upload the search data into mongodb database
if choice=="Data-Base":
    col1,col2,col3 = st.columns(3)
    col1.image(Image.open("C:/Users/DELL/Desktop/Twitter--scraping-main/media/data-base.png"),width = 250)
    col3.image(Image.open("C:/Users/DELL/Desktop/Twitter--scraping-main/media/Mongodb.png"))
    col2.header("You can ADD your Previous Search DATA into MongoDB data base to work with Cloud-Network")

    list = ['',"store in data-base","view as data-frame"]
    CHOICE = st.selectbox("SELECT",list)
    if CHOICE=="store in data-base":
        if "n_word" not in st.session_state:
            st.session_state["n_word"] = ""
        n_word = st.text_input("Enter the KEY-WORD",st.session_state["n_word"])
        upload = st.button("upload")
        if upload:
            Bird_In_Database(n_word)
            st.success("Your DATA-BASE has been UPDATED SUCCESSFULLY :smiley:")
            col1,col2,col3=st.columns(3)
            col1.image(Image.open("C:/Users/DELL/Desktop/Twitter--scraping-main/media/jerry-cheese.png"))
            col2.header("THANKS FOR THE CHEESE..!")
            col3.image(Image.open("C:/Users/DELL/Desktop/Twitter--scraping-main/media/tom.png"))
    if CHOICE=="view as data-frame":
        if st.button("view :goggles:"):
            df = pd.read_csv("user-tweets.csv")
            st.dataframe(df)
            st.balloons()


#It is to tell about myself and my social-pages
if choice=="Contact":
    name = "Vishal Kumar"
    mail = (f'{"Mail Me At :"}  {"vishal18051998@gmail.com"}')
    description = "An aspiring DATA-SCIENTIST with un-discribable idea's"
    social_media = {
        

    }
    col1,col2,col3= st.columns(3)
    col1.image(Image.open("C:/Users/DELL/Desktop/Twitter--scraping-main/media/space.png"),width = 500)
   # col2.image(Image.open("C:/Users/DELL/Desktop/Twitter--scraping-main/media/my.png"),width = 400)
    with col3:
        st.title(name)
        st.write("---")
        st.write(description)
        st.write(mail)
   





































