import streamlit as st
import pandas as pd




st.set_page_config(
        page_title="Water Calculator",
        layout="wide",
)




# Container to hold the elements
st.markdown('<div class="vertical-end">', unsafe_allow_html=True)
st.title("Water Conservation Calculator 💧")
emirate= st.selectbox("Choose your residing Emirate", ["Dubai", "Abu Dhabi"])
famNum= st.number_input("Enter the number of family members", 2)


st.subheader("Duration of usage(Minutes)")
col1, col2, col3, col4= st.columns(4)
with col1:# Shower head time 
    showerTime = st.number_input("Showerhead", value=10, min_value=0)
with col2:# Bathroom Faucet
    bathroomTime = st.number_input("Bathroom Faucet", value= 6, min_value=0)
with col3:# Kitchen Faucet
    kitchenTime = st.number_input("Kitchen Faucet",  value=8, min_value=0)
with col4:# Washing Dishes(manually)
    mDishTime = st.number_input("Washing Dishes(Manual)",  value=5, min_value=0)

st.subheader("Frequency of usage(Weekly)")
col1, col2, col3, col4= st.columns(4)
with col1:# Shower head time 
    showerFreq = st.number_input("Showerhead", value=5, key="showerFreq", min_value=0)
    carFreq = st.number_input("Car Washing",  value=1, key="carFreq", min_value=0)
with col2:# Bathroom Faucet
    bathroomFreq = st.number_input("Bathroom Faucet",  value=7, key="bathroomFreq", min_value=0)
    toiletFreq = st.number_input("Toilet Flush",  value=14, key="toiletFreq", min_value=0)
with col3:# Kitchen Faucet
    kitchenFreq = st.number_input("Kitchen Faucet",  value=7, key="kitchenFreq", min_value=0)
    aDishFreq = st.number_input("Dishwasher", value= 5, key="aDishFreq", min_value=0)
with col4:# Washing Dishes(manually)
    mDishFreq = st.number_input("Washing Dishes(Manual)",  value=7, key="mDishFreq", min_value=0)
    clothesFreq = st.number_input("Clothes Washer",  value=3, key="clothesFreq", min_value=0)



bathFreq = st.number_input("Bathtub", 1)
bathType= st.selectbox("Choose your Bathtub Type", ["Medium", "Small", "Large"])
toleranceLimit= st.number_input("Water conservation tolerance limit", 150)




ideal={}

if(emirate=="Dubai"):
    consumed = {
        'Shower': 8*showerTime*showerFreq*famNum,
        'Bathroom Faucet': 6*bathroomTime*bathroomFreq*famNum,
        'Kitchen Faucet': 7*kitchenTime*kitchenFreq*famNum,
        'Washing Dishes(Manual)': 7*mDishTime*mDishFreq*famNum,
        'Car Washing': 274*carFreq*famNum,
        'Bathtub': 0,
        'Toilet Flush': 5*toiletFreq*famNum,
        'Dishwasher': 43*aDishFreq*famNum,
        'Clothes Washing': 151*clothesFreq*famNum,
        }
elif (emirate=="Abu Dhabi"):
    consumed = {
        'Shower': 9.5*showerTime*showerFreq*famNum,
        'Bathroom Faucet': 6.0 *bathroomTime*bathroomFreq*famNum,
        'Kitchen Faucet': 6.0*kitchenTime*kitchenFreq*famNum,
        'Washing Dishes(Manual)': 6.0*mDishTime*mDishFreq*famNum,
        'Car Washing': 274*carFreq*famNum,
        'Bathtub': 0,
        'Toilet Flush': 6*toiletFreq*famNum,
        'Dishwasher': 43*aDishFreq*famNum,
        'Clothes Washing': 151*clothesFreq*famNum,
        }
    
if(bathType=="Small"):
    consumed['Bathtub'] = 151*bathFreq*famNum
if(bathType=="Medium"):
    consumed['Bathtub'] = 302*bathFreq*famNum
if(bathType=="Large"):
    consumed['Bathtub'] = 416*bathFreq*famNum

ideal = {
        'Shower': round(5.6*showerTime*showerFreq*famNum,3),
        'Bathroom Faucet': round(3.8 *bathroomTime*bathroomFreq*famNum, 3),
        'Kitchen Faucet': round(3.8*kitchenTime*kitchenFreq*famNum, 3),
        'Washing Dishes(Manual)': round(3.8*mDishTime*mDishFreq*famNum, 3),
        'Car Washing': round(19*carFreq*famNum, 3),
        'Bathtub': 0,
        'Toilet Flush': round(4.8*toiletFreq*famNum, 3),
        'Dishwasher': round(22*aDishFreq*famNum, 3),
        'Clothes Washing': round(60*clothesFreq*famNum, 3),
        }
saved = {key: round((consumed[key] - ideal[key]), 3) for key in consumed}

wantedTimeFrame =1.0
tableType="Weekly"

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Daily"):
        wantedTimeFrame=1/7
        tableType="Daily"
with col2:
    if st.button("Weekly"):
        wantedTimeFrame=1
        tableType="Weekly"
with col3:
    if st.button("Yearly"):
        wantedTimeFrame=365/7
        tableType="Yearly"

consumedTable = pd.DataFrame([consumed])
consumedTable.index = [tableType]
consumedTable = consumedTable.mul(wantedTimeFrame)
consumedTable = consumedTable.round(2)
consumedTable = consumedTable.applymap("{:.2f}".format)


idealTable = pd.DataFrame([ideal])
idealTable.index = [tableType]
idealTable = idealTable.mul(wantedTimeFrame)
idealTable = idealTable.round(2)
idealTable = idealTable.applymap("{:.2f}".format)


savedTable = pd.DataFrame([saved])
savedTable.index = [tableType]
savedTable = savedTable.mul(wantedTimeFrame)
savedTable = savedTable.round(2)
savedTable = savedTable.applymap("{:.2f}".format)




st.subheader("Consumed")
st.table(consumedTable)
st.subheader("Ideal")
st.table(idealTable)
st.subheader("Saved")
st.table(savedTable)

totalSavedAmount=round(sum(saved.values())*wantedTimeFrame, 2)

statement = f"<p style='font-size: 24px;'>The total Savings Are: <span style='color: #6495ED; font-weight: bold; text-decoration: underline; font-size:40px'>{totalSavedAmount}</span> Litres {tableType}</p>"
st.markdown(statement, unsafe_allow_html=True)


def highlight_cell(x):
    try:
        if float(x) < toleranceLimit*wantedTimeFrame:
            return "background-color: #3498DB; color: white", "True"
        else:
            return "background-color: #FF5733; color: white", "False"
    except ValueError:
        return "", str(x)  # Return empty style for non-numeric values

styled_df = savedTable.style.applymap(lambda x: highlight_cell(x)[0])
st.write("## Fields That Can Be Improved")
st.table(styled_df)
