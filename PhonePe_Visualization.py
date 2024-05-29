import os
import json 
import pandas as pd
import numpy as np
import mysql.connector
import streamlit as st
import plotly.express as px 
import altair as alt

# Database connection
connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Taffy&0402",
        database="phonepay_db"
    )
cursor = connection.cursor()

cursor.execute("use phonepay_db")

# Load data from MySQL
cursor.execute("SELECT * FROM phonepay_db.aggregated_transaction")
table1 = cursor.fetchall()
Aggre_transsaction = pd.DataFrame(table1, columns=[
    "State", "Year", "Quarter", "Transaction_type", "Transaction_count", "Transaction_amount"
])

cursor.execute("SELECT * FROM phonepay_db.aggregated_user")
table2 = cursor.fetchall()
Aggre_user = pd.DataFrame(table2, columns=[
    "State", "Year", "Quarter", "Brand", "Transaction_count", "Percentage"
])

cursor.execute("SELECT * FROM phonepay_db.map_transaction")
table3 = cursor.fetchall()
Map_trans = pd.DataFrame(table3, columns=[
    "State", "Year", "Quarter", "District", "Transaction_count", "Transaction_amount"
])

cursor.execute("SELECT * FROM phonepay_db.map_user")
table4 = cursor.fetchall()
Map_user = pd.DataFrame(table4, columns=[
    "State", "Year", "Quarter", "District", "Registered_user", "App_open"
])

cursor.execute("SELECT * FROM phonepay_db.top_transaction")
table5 = cursor.fetchall()
Top_trans = pd.DataFrame(table5, columns=[
    "State", "Year", "Quarter", "Entity_name", "Transaction_count", "Transaction_amount"
])

cursor.execute("SELECT * FROM phonepay_db.top_user")
table6 = cursor.fetchall()
Top_user = pd.DataFrame(table6, columns=[
    "State", "Year", "Quarter", "District", "Registered_user"
])

# Streamlit app
tab1,tab2=st.tabs(["Visualization","Insights"])
with tab1:
    st.title('Phonepe Pulse Data Visualization and Exploration')
    dataset_option = st.sidebar.selectbox(
        'Select Dataset',
        ['Aggregated Transactions', 'Aggregated Users', 'Map Transactions', 'Map Users', 'Top Transactions', 'Top Users']
    )

    # Add year selection option
    year_option = st.sidebar.selectbox(
        'Select Year',
        sorted(Aggre_transsaction['Year'].unique())
    )


    # Dropdown options for quarter selection
    quarter_option = st.sidebar.selectbox(
        'Select Quarter',
        [1, 2, 3, 4]
    )

    # Filter data based on the selected year and quarter
    def filter_data_by_year_and_quarter(df, year, quarter):
        return df[(df['Year'] == year) & (df['Quarter'] == quarter)]


    # GeoJSON URL for India states
    geojson_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"

    # Display selected data based on dataset and quarter
    def display_agg_info_and_map(filtered_data, count_column, amount_column, color_column,type, color_scale, title, show_amount=True):
        total_count = filtered_data[count_column].sum()
        st.write(f"**Total Count:** {total_count:,}")
        
        if show_amount and amount_column:
            total_amount = filtered_data[amount_column].sum()
            st.write(f"**Total Amount:** ₹{total_amount:,.2f} Cr")

        fig = px.choropleth(
            filtered_data,
            geojson=geojson_url,
            featureidkey='properties.ST_NM',
            locations='State',
            color=color_column,
            color_continuous_scale=color_scale,
            title=title
        )
        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig)
        display_agg_trans_info(filtered_data,amount_column,type)
        
    # Display selected data based on dataset and quarter
    def display_map_info_and_map(filtered_data, count_column, amount_column, color_column,district, color_scale, title, show_amount=True):
        total_count = filtered_data[count_column].sum()
        st.write(f"**Total Count:** {total_count:,}")
        
        if show_amount and amount_column:
            total_amount = filtered_data[amount_column].sum()
            st.write(f"**Total Amount:** ₹{total_amount:,.2f} Cr")

        fig = px.choropleth(
            filtered_data,
            geojson=geojson_url,
            featureidkey='properties.ST_NM',
            locations='State',
            color=color_column,
            color_continuous_scale=color_scale,
            title=title
        )
        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig)
        display_map_trans_info(filtered_data, amount_column, count_column, district, type)
        
    # Display selected data based on dataset and quarter
    def display_top_info_and_map(filtered_data, count_column, amount_column, color_column, entity,color_scale, title, show_amount=True):
        total_count = filtered_data[count_column].sum()
        st.write(f"**Total Count:** {total_count:,}")
        
        if show_amount and amount_column:
            total_amount = filtered_data[amount_column].sum()
            st.write(f"**Total Amount:** ₹{total_amount:,.2f} Cr")

        fig = px.choropleth(
            filtered_data,
            geojson=geojson_url,
            featureidkey='properties.ST_NM',
            locations='State',
            color=color_column,
            color_continuous_scale=color_scale,
            title=title
        )
        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig)
        display_top_trans_info(filtered_data, count_column,amount_column,entity)
        

        
    def agg_user_info(filtered_data, registered_user_column, brand, percentage, title):
        total_registered_users = filtered_data[registered_user_column].sum()
        total_percentage = filtered_data[percentage].sum()
        st.write(f"Total Registered Users: {total_registered_users:,}")
        st.write(f"Total percentage: {total_percentage}")
        fig = px.choropleth(
        filtered_data,
        geojson=geojson_url,
        featureidkey='properties.ST_NM',
        locations='State',
        color=registered_user_column,
        hover_data={brand: True},
        color_continuous_scale='blues',
        title=title
        )
        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig)

        display_agg_users_info(filtered_data, registered_user_column, brand)
        
        
    # Display selected data based on dataset and quarter for user-related metrics
    def map_user_info(filtered_data, registered_user_column, app_open_column, title):
        total_registered_users = filtered_data[registered_user_column].sum()
        total_app_opens = filtered_data[app_open_column].sum()
        st.write(f"Total Registered Users: {total_registered_users:,}")
        st.write(f"Total App Opens: {total_app_opens:,}")
        fig = px.choropleth(
        filtered_data,
        geojson=geojson_url,
        featureidkey='properties.ST_NM',
        locations='State',
        color=registered_user_column,
        hover_data={app_open_column: True},
        color_continuous_scale='blues',
        title=title
        )
        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig)

        display_map_users_info(filtered_data, registered_user_column, app_open_column)
        
    # Display selected data based on dataset and quarter for user-related metrics
    def top_user_info(filtered_data, registered_user_column, title):
        total_registered_users = filtered_data[registered_user_column].sum()
        st.write(f"Total Registered Users: {total_registered_users:,}")
        fig = px.choropleth(
        filtered_data,
        geojson=geojson_url,
        featureidkey='properties.ST_NM',
        locations='State',
        color=registered_user_column,
        color_continuous_scale='blues',
        title=title
        )
        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig)

        display_top_users_info(filtered_data, registered_user_column)
        
        

    # Display top 10 users (both state-wise and district-wise)
    def display_agg_trans_info(filtered_data, transaction_amount, type):
        # Display top 10 states by Registered_user
        st.subheader("Top 10 States by Transaction Amount")
        top_states = filtered_data.groupby('State')[transaction_amount].sum().nlargest(10).reset_index()
        st.write(top_states)

        # Display top 10 districts by App_open
        st.subheader("Categories")
        top_districts_brand = filtered_data.groupby('Transaction_type')[transaction_amount].sum().nlargest().reset_index()
        st.write(top_districts_brand)   
        
        
    # Display top 10 users (both state-wise and district-wise)
    def display_agg_users_info(filtered_data, registered_user_column, brand):
        # Display top 10 states by Registered_user
        st.subheader("Top 10 States by Transaction Count")
        top_states = filtered_data.groupby('State')[registered_user_column].sum().nlargest(10).reset_index()
        st.write(top_states)

        # Display top 10 districts by App_open
        st.subheader("Top 10 Brands by Transacation Count")
        top_districts_brand = filtered_data.groupby('Brand')[registered_user_column].sum().nlargest(10).reset_index()
        st.write(top_districts_brand)
        
    # Display top 10 users (both state-wise and district-wise)
    def display_map_trans_info(filtered_data, transaction_amount, transaction_count, district, type):
        # Display top 10 states by Registered_user
        st.subheader("Top 10 States by Transaction Amount")
        top_states = filtered_data.groupby('State')[transaction_amount].sum().nlargest(10).reset_index()
        st.write(top_states)

        # Display top 10 districts by App_open
        st.subheader("Top 10 District by Transaction Amount")
        top_districts_brand = filtered_data.groupby('District')[transaction_amount].sum().nlargest(10).reset_index()
        st.write(top_districts_brand)   
        
    # Display top 10 users (both state-wise and district-wise)
    def display_map_users_info(filtered_data, registered_user_column, app_open_column):
        # Display top 10 states by Registered_user
        st.subheader("Top 10 States by Registered Users")
        top_states = filtered_data.groupby('State')[registered_user_column].sum().nlargest(10).reset_index()
        st.write(top_states)

        # Display top 10 districts by Registered_user
        st.subheader("Top 10 Districts by Registered Users")
        top_districts = filtered_data.groupby('District')[registered_user_column].sum().nlargest(10).reset_index()
        st.write(top_districts)

        # Display top 10 districts by App_open
        st.subheader("Top 10 Districts by App Opens")
        top_districts_app_open = filtered_data.groupby('District')[app_open_column].sum().nlargest(10).reset_index()
        st.write(top_districts_app_open)
        
    # Display top 10 users (both state-wise and district-wise)
    def display_top_users_info(filtered_data, registered_user_column ):
        # Display top 10 states by Registered_user
        st.subheader("Top 10 States by Registered User")
        top_states = filtered_data.groupby('State')[registered_user_column].sum().nlargest(10).reset_index()
        st.write(top_states)

        # Display top 10 districts by Registered_user
        st.subheader("Top 10 District by Registered User")
        top_districts = filtered_data.groupby('District')[registered_user_column].sum().nlargest(10).reset_index()
        st.write(top_districts)

    # Display top 10 users (both state-wise and district-wise)
    def display_top_trans_info(filtered_data, count_column,amount_column,entity):
        # Display top 10 states by Registered_user
        st.subheader("Top 10 Entity by Transaction count")
        top_states = filtered_data.groupby('Entity_name')[count_column].sum().nlargest(10).reset_index()
        st.write(top_states)

        # Display top 10 districts by Registered_user
        st.subheader("Top 10 Entity by Transaction Amount")
        top_districts = filtered_data.groupby('Entity_name')[amount_column].sum().nlargest(10).reset_index()
        st.write(top_districts)



        

        
    if dataset_option == 'Aggregated Transactions':
        st.write('Aggregated Transactions')
        filtered_data = filter_data_by_year_and_quarter(Aggre_transsaction, year_option, quarter_option)
        display_agg_info_and_map(filtered_data, 'Transaction_count', 'Transaction_amount', 'Transaction_amount', 'Transaction_type','reds', f'Aggregated Transactions by State - {year_option} Q{quarter_option}')

    elif dataset_option == 'Aggregated Users':
        st.write('Aggregated Users')
        filtered_data = filter_data_by_year_and_quarter(Aggre_user, year_option, quarter_option)
        agg_user_info(filtered_data, 'Transaction_count', 'Brand', 'Percentage', f'Aggregated Users by State - {year_option} Q{quarter_option}')

    elif dataset_option == 'Map Transactions':
        st.write('Map Transactions')
        filtered_data = filter_data_by_year_and_quarter(Map_trans, year_option, quarter_option)
        display_map_info_and_map(filtered_data, 'Transaction_count', 'Transaction_amount', 'Transaction_amount','District', 'reds', f'Map Transactions by State - {year_option} Q{quarter_option}')

    elif dataset_option == 'Map Users':
        st.write('Map Users')
        filtered_data = filter_data_by_year_and_quarter(Map_user, year_option, quarter_option)
        map_user_info(filtered_data, 'Registered_user', 'App_open', f'Map Users by State - {year_option} Q{quarter_option}')

    elif dataset_option == 'Top Transactions':
        st.write('Top Transactions')
        filtered_data = filter_data_by_year_and_quarter(Top_trans, year_option, quarter_option)
        display_top_info_and_map(filtered_data, 'Transaction_count', 'Transaction_amount', 'Transaction_amount','Entity', 'reds', f'Top Transactions by State - {year_option} Q{quarter_option}')

    elif dataset_option == 'Top Users':
        st.write('Top Users')
        filtered_data = filter_data_by_year_and_quarter(Top_user, year_option, quarter_option)
        top_user_info(filtered_data, 'Registered_user', f'Top Users by State - {year_option} Q{quarter_option}')

with tab2:
    st.header("Insight on PhonePe Data")
    
    # # Helper function to execute queries and log the results
    # def execute_query(query, columns):
    #     cursor.execute(query)
    #     data = cursor.fetchall()
    #     return pd.DataFrame(data, columns=columns)
    
    

    # 1. Increase in Merchant Payments
    with st.expander("1) Increase in Merchant Payments"):
        
        cursor.execute("""
            SELECT Year, SUM(Transaction_amount) 
            FROM phonepay_db.aggregated_transaction 
            WHERE Transaction_type='Merchant payments' And Year != 2024
            GROUP BY Year
        """)
        data=cursor.fetchall()
        col = ["Year", "Total_Amount"]
        chart_data = pd.DataFrame(data, columns=col)
        chart_data["Total_Amount"] = chart_data["Total_Amount"].astype(float)
        # Create Altair chart
        bar_chart = alt.Chart(chart_data).mark_bar().encode(
        x=alt.X('Year:O', title='Year'),  # 'Year:O' ensures the Year is treated as ordinal
        y=alt.Y('Total_Amount:Q', title='Total Amount (in currency unit)')
        ).properties(
        title='Total Merchant Payments by Year'
        )

        # Display the chart in Streamlit
        st.altair_chart(bar_chart, use_container_width=True)
        st.write("By examining the bar chart, one can identify trends in merchant payments over time. This includes observing whether there is an increase, decrease, or stability in the total transaction amounts across years.")

    # 2. Growth in P2P Transactions
    with st.expander("2) Growth in P2P Transactions"):
        cursor.execute("""
            SELECT Year, SUM(Transaction_amount) 
            FROM phonepay_db.aggregated_transaction 
            WHERE Transaction_type='Peer-to-peer payments' And Year != 2024
            GROUP BY Year
        """)
        data = cursor.fetchall()
        df = pd.DataFrame(data, columns=["Year", "Total_Amount"])
        df["Total_Amount"] = df["Total_Amount"].astype(float)
        df["Year"] = df["Year"].astype(int)
        st.line_chart(df.set_index("Year"))

    # 3. High Transaction Volume in Metropolitan Areas
    with st.expander("3) High Transaction Volume in Metropolitan Areas"):
        cursor.execute("""
            SELECT State, SUM(Transaction_count) 
            FROM phonepay_db.map_transaction 
            GROUP BY State
            ORDER BY SUM(Transaction_count) DESC
            LIMIT 10
        """)
        data = cursor.fetchall()
        df = pd.DataFrame(data, columns=["State", "Total_Transactions"])
        df["Total_Transactions"] = df["Total_Transactions"].astype(float)
        st.bar_chart(df.set_index("State"))

    # 4. Most Popular States for Digital Transactions
    with st.expander("4) Most Popular States for Digital Transactions"):
        selected_year = st.number_input("Enter the year", min_value=2000, max_value=2100, step=1)
    
        # Execute the SQL query to fetch transaction data for the specified year
        cursor.execute("""
        SELECT State, SUM(Transaction_amount) 
        FROM phonepay_db.map_transaction 
        WHERE Year = %s
        GROUP BY State
        ORDER BY SUM(Transaction_amount) DESC
        LIMIT 10
        """, (selected_year,))
        data = cursor.fetchall()
        df = pd.DataFrame(data, columns=["State", "Total_Amount"])
        df["Total_Amount"] = df["Total_Amount"].astype(float)
        st.bar_chart(df.set_index("State"))

    # 5. Significant Increase in Registered Users
    with st.expander("5) Significant Increase in Registered Users"):
        cursor.execute("""
            SELECT Year, SUM(Registered_user) 
            FROM phonepay_db.map_user 
            WHERE Year!=2024
            GROUP BY Year
        """)
        data = cursor.fetchall()
        df = pd.DataFrame(data, columns=["Year", "Total_Users"])
        df["Total_Users"] = df["Total_Users"].astype(float)
        st.line_chart(df.set_index("Year"))
        

    # 6. Top Brands by Transaction Count
    with st.expander("6) Top Brands by Transaction Count"):
        cursor.execute("""
            SELECT Brand, SUM(Transaction_count) 
            FROM phonepay_db.aggregated_user 
            GROUP BY Brand
            ORDER BY SUM(Transaction_count) DESC
            LIMIT 10
        """)
        data = cursor.fetchall()
        df = pd.DataFrame(data, columns=["Brand", "Total_Transactions"])
        df["Total_Transactions"] = df["Total_Transactions"].astype(float)
        st.bar_chart(df.set_index("Brand"))

    # 7. Transaction Trends by Quarter
    with st.expander("7) Transaction Trends by Quarter"):
        cursor.execute("""
            SELECT CONCAT(Year, ' Q', Quarter) as Period, SUM(Transaction_amount) 
            FROM phonepay_db.aggregated_transaction 
            GROUP BY Year, Quarter
        """)
        data = cursor.fetchall()
        df = pd.DataFrame(data, columns=["Period", "Total_Amount"])
        df["Total_Amount"] = df["Total_Amount"].astype(float)
        st.line_chart(df.set_index("Period"))

    # 8. Increase in App Opens
    with st.expander("8) Increase in App Opens"):
        cursor.execute("""
            SELECT Year, SUM(App_open) 
            FROM phonepay_db.map_user 
            GROUP BY Year
        """)
        data = cursor.fetchall()
        df = pd.DataFrame(data, columns=["Year", "Total_App_Opens"])
        df["Total_App_Opens"] = df["Total_App_Opens"].astype(float)
        st.line_chart(df.set_index("Year"))

    # 9. Top Entities by Transaction Amount
    with st.expander("9) Top Entities by Transaction Amount"):
        cursor.execute("""
            SELECT Entity_name, SUM(Transaction_amount) 
            FROM phonepay_db.top_transaction 
            GROUP BY Entity_name
            ORDER BY SUM(Transaction_amount) DESC
            LIMIT 10
        """)
        data = cursor.fetchall()
        df = pd.DataFrame(data, columns=["Entity", "Total_Amount"])
        df["Total_Amount"] = df["Total_Amount"].astype(float)
        st.bar_chart(df.set_index("Entity"))

    # 10. Yearly Transaction Comparison
    with st.expander("10) Yearly Transaction Comparison"):
        cursor.execute("""
            SELECT Year, SUM(Transaction_amount) 
            FROM phonepay_db.aggregated_transaction 
            GROUP BY Year
        """)
        data = cursor.fetchall()
        df = pd.DataFrame(data, columns=["Year", "Total_Amount"])
        df["Total_Amount"] = df["Total_Amount"].astype(float)
        st.line_chart(df.set_index("Year"))
