import pandas as pd
import mysql.connector
import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import time
import pymysql
from datetime import datetime

# Load data into a dictionary and ensure unique routes
state_data = {
    "Meghalaya": pd.read_csv(r"Bus_details\df_Meghalaya.csv")["Route_name"].unique().tolist(),
    "Andhra Pradesh": pd.read_csv(r"Bus_details\df_andhra.csv")["Route_name"].unique().tolist(),
    "Telangana": pd.read_csv(r"Bus_details\df_Telangana.csv")["Route_name"].unique().tolist(),
    "Goa": pd.read_csv(r"Bus_details\df_Kadamba.csv")["Route_name"].unique().tolist(),
    "Rajastan": pd.read_csv(r"Bus_details\df_Rajastan.csv")["Route_name"].unique().tolist(),
    "Gujarat": pd.read_csv(r"Bus_details\df_Gujarat.csv")["Route_name"].unique().tolist(),
    "Sikkim": pd.read_csv(r"Bus_details\df_Sikkim.csv")["Route_name"].unique().tolist(),
    "Assam": pd.read_csv(r"Bus_details\df_Assam.csv")["Route_name"].unique().tolist(),
    "Uttar Pradesh": pd.read_csv(r"Bus_details\df_Uttar_pradesh.csv")["Route_name"].unique().tolist(),
    "Kerala": pd.read_csv(r"Bus_details\df_Kerala.csv")["Route_name"].unique().tolist()
}

st.set_page_config(layout="wide")

web = option_menu(
    menu_title="🏕️🚍RedBus",
    options=["Home", "🔍Search"],
    icons=["house", "info-circle"],
    orientation="horizontal"
)

if web == "Home":
    st.image(image="https://s3.rdbuz.com/Images/rdc/rdc-redbus-logo.webp", width=200)
    st.title("Redbus-India's No. 1 Online Bus Ticket Booking Site")
    st.markdown("## **About Us**")
    st.markdown("redBus is India’s largest online bus ticketing platform that has transformed bus travel in the country by bringing ease and convenience to millions of Indians who travel using buses. Founded in 2006, redBus is part of India’s leading online travel company MakeMyTrip Limited (NASDAQ: MMYT). By providing widest choice, superior customer service, lowest prices and unmatched benefits, redBus has served over 18 million customers. redBus has a global presence with operations across Indonesia, Singapore, Malaysia, Colombia and Peru apart from India.")
    st.markdown("Booking a bus ticket online on the redBus app or website is very simple. You can download the redBus app or visit redbus.in and enter your source, destination & travel date to check the top-rated bus services available. You can then compare bus prices, user ratings & amenities, select your preferred seat, boarding & dropping points and pay using multiple payment options like UPI, debit or credit card, net banking and more. With redBus, get assured safe & secure payment methods and guaranteed travel with the best seat and bus operator of your choice. Once the bus booking payment is confirmed, all you have to do is pack your bags and get ready to travel with the m-ticket, which you can show to the bus operator on your mobile before boarding the bus. Online bus ticket booking with redBus is that simple!")
    st.markdown("redBus also offers other exclusive benefits on online bus tickets like flexible ticket rescheduling options, easy & friendly cancellation policies, and instant payment refunds. With a live bus tracking feature, you can plan travel and never miss the bus. You can get the cheapest bus tickets by availing the best discounts for new & existing customers. With redDeals, you can also get exclusive & additional discounts on your online bus ticket booking. You will get 24/7 customer support on call, chat & help to resolve all your queries in English & local languages.")
    st.markdown("redBus offers Primo bus services, specially curated by redBus, which have highly rated buses and best-in-class service. With Primo by redBus, you can be assured of safe, comfortable, and on-time bus service at no additional cost. With multiple boarding and dropping points available across all major cities in India, you can select at your convenience and enjoy a smooth travel experience.")
    st.markdown("redBus operates in six countries, including India, Malaysia, Singapore, Indonesia, Peru, and Colombia. Through its website and app, it has sold over 220 million bus tickets worldwide. With over 36 million satisfied customers, redBus is committed to providing its users with a world-class online bus booking experience.")
    st.markdown("redBus offers bus tickets from some of the top private bus operators, such as Orange Travels, VRL Travels, SRS Travels, Chartered Bus, and Praveen Travels, and state government bus operators, such as APSRTC, TSRTC, GSRTC, Kerala RTC, TNSTC, RSRTC, UPSRTC, and more. With redBus, customers can easily book bus tickets for different bus types, such as AC/non-AC, Sleeper, Seater, Volvo, Multi-axle, AC Sleeper, Electric buses, and more.")

if web == "🔍Search":
    S = st.selectbox("States", list(state_data.keys()))

    col1, col2, col3 = st.columns(3)
    with col1:
        select_type = st.selectbox("Select the Bustype", ["sleeper", "semi-sleeper", "seater", "others"])
    with col2:
        select_price = st.selectbox("Select the Busprice", ["0-500", "500-1000", "1000-2000", "2000 and above"])
    with col3:
        select_rating = st.selectbox("Select the Rating", ["1-2", "2-3", "3-4", "4-5", "New"])
    TIME = st.time_input("select the time")

    def type_and_price(state, bustype, price_range, rating):
        conn = pymysql.connect(host="localhost", user="root", password="3123", database="redbus_project")
        my_cursor = conn.cursor()
        # Define price range based on selection
        if price_range == "0-500":
            price_min, price_max = 0, 500
        elif price_range == "500-1000":
            price_min, price_max = 500, 1000
        elif price_range == "1000-2000":
            price_min, price_max = 1000, 2000
        else:
            price_min, price_max = 2000, 100000

        # Define rating condition
        if rating == "1-2":
            rating_condition = "star_rating BETWEEN 1 AND 2"
        elif rating == "2-3":
            rating_condition = "star_rating BETWEEN 2 AND 3"
        elif rating == "3-4":
            rating_condition = "star_rating BETWEEN 3 AND 4"
        elif rating == "4-5":
            rating_condition = "star_rating BETWEEN 4 AND 5"
        else:
            rating_condition = "star_rating < 1"

        # Define bus type condition
        if bustype == "sleeper":
            bustype_condition = "bustype LIKE '%Sleeper%'"
        elif bustype == "semi-sleeper":
            bustype_condition = "bustype LIKE '%A/c Semi Sleeper%'"
        elif bustype == "seater":
            bustype_condition = "bustype LIKE '%Seater%'"
        else:
            bustype_condition = "bustype NOT LIKE '%Sleeper%' AND bustype NOT LIKE '%Semi-Sleeper%'"

        query = f"""
        SELECT * FROM redbus_info
        WHERE Price BETWEEN {price_min} AND {price_max}
        AND route_name = '{state}'
        AND {rating_condition}
        AND {bustype_condition}
        AND departing_time >= '{TIME}'
        ORDER BY Price, departing_time DESC
        """

        my_cursor.execute(query)
        out = my_cursor.fetchall()
        conn.close()
        
        new_order = ['id', 'Route_name', 'Route_link', 'Bus_name', 'Bus_type', 'Start_time', 'Total_duration', 'End_time', 'Ratings', 'Price', 'Seats_Available']
        df = pd.DataFrame(out, columns=new_order)
        # Convert Start_time and End_time to 24-hour format 
        df['Start_time'] = df['Start_time'].apply(lambda x: (datetime.min + x).time().strftime('%H:%M') if isinstance(x, pd.Timedelta) else x) 
        df['End_time'] = df['End_time'].apply(lambda x: (datetime.min + x).time().strftime('%H:%M') if isinstance(x, pd.Timedelta) else x)
        return df

    K = st.selectbox("Routes", state_data[S])
    df_result = type_and_price(K, select_type, select_price, select_rating)
    st.dataframe(df_result)
