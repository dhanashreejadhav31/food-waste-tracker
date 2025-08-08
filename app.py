
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date

# Load or initialize data
DATA_PATH = "data/food_waste_log.csv"
try:
    df = pd.read_csv(DATA_PATH)
except:
    df = pd.DataFrame(columns=["Date", "Food Type", "Amount"])

st.title("🍽️ Food Waste Tracker")
st.subheader("Support Zero Hunger - SDG 2")

# Form to enter waste
with st.form("waste_form"):
    waste_date = st.date_input("Date", value=date.today())
    food_type = st.selectbox("Food Type", ["Vegetables", "Fruits", "Grains", "Meat", "Dairy", "Other"])
    amount = st.number_input("Amount of Waste (grams)", min_value=1)
    submitted = st.form_submit_button("Log Waste")

    if submitted:
        new_entry = pd.DataFrame([[waste_date, food_type, amount]], columns=["Date", "Food Type", "Amount"])
        df = pd.concat([df, new_entry], ignore_index=True)
        df.to_csv(DATA_PATH, index=False)
        st.success("Waste logged successfully!")

# Show summary
if not df.empty:
    st.markdown("### 📊 Waste Summary")

    # Total waste
    total = df["Amount"].sum()
    st.metric("Total Food Waste Logged", f"{total:.2f} grams")

    # Bar chart
    st.bar_chart(df.groupby("Food Type")["Amount"].sum())

    # Pie chart
    fig, ax = plt.subplots()
    df.groupby("Food Type")["Amount"].sum().plot(kind='pie', autopct='%1.1f%%', ax=ax)
    ax.set_ylabel('')
    st.pyplot(fig)

# Tips
st.markdown("### 💡 Food Saving Tip")
with open("tips.txt", "r") as f:
    tips = f.readlines()

import random
st.info(random.choice(tips))
