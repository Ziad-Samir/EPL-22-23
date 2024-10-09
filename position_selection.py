
import streamlit as st
import joblib
import pandas as pd

scaler = joblib.load( "Scaler.pkl")
res = joblib.load( "res.pkl")
model  = joblib.load( "Model.pkl")
Inputs = joblib.load( "Inputs.pkl")
Smote = joblib.load("smote.pkl")

### Abtedy adef el variables elly bt2asar 3ala el predection
def Prediction(A,B,C, Dist, D, PrgDist, E,F, CrsPA, PrgP, G): ###Ba3mel data frame bel columns elly 3andy we ashof btebtedy mn 3and kam we asameha
    df = pd.DataFrame(columns= ['90s', 'Sh/90', 'SoT/90', 'Dist', 'Cmp%', 'PrgDist', 'Cmp%_Short','Cmp%_Medium', 'CrsPA', 'PrgP', '3/1'])
    df.at[0,"90s"]= A
    df.at[0,"Sh/90"]= B
    df.at[0,"SoT/90"]= C
    df.at[0,"Dist"]= Dist
    df.at[0,"Cmp%"]= D
    df.at[0,"PrgDist"]= PrgDist
    df.at[0,"Cmp%_Short"]= E
    df.at[0,"Cmp%_Medium"]= F
    df.at[0,"CrsPA"]= CrsPA
    df.at[0,"PrgP"]= PrgP
    df.at[0,"3/1"]= G
 
    df= scaler.transform(df)
       
    result = model.predict(df)
    return result[0]

###ba3mel hena design el shakl bta3y
def Main():
    A= st.slider( "Mtch Played",min_value= 0 , max_value=38 , step= 1 , value=25)
    B= st.slider("Shots in Match",min_value= 0 , max_value=15 , step= 1 , value=5)
    C = st.slider("Shots on target per Match",min_value= 0 , max_value=15 , step= 1 , value=5)
    Dist = st.slider("Average distance, in yards, from goal of all shots taken",min_value= 0 , max_value=35 , step= 1 , value=5)
    D= st.slider("Pass Completion Percentage",min_value= 0 , max_value=100 , step= 1 , value=5)
    PrgDist = st.slider("Progressive Passes",min_value= 0 , max_value=10115 , step= 1 , value=5)
    E = st.slider("Pass Completion % Short",min_value= 0 , max_value=100 , step= 1 , value=5)
    F = st.slider("Pass Completion % Medium",min_value= 0 , max_value=100 , step= 1 , value=5)
    CrsPA = st.slider("Crosses into Penalty Area",min_value= 0 , max_value=25 , step= 1 , value=5)
    PrgP = st.slider("Progressive Passes",min_value= 0 , max_value=270 , step= 1 , value=5)
    G= st.slider("Passes into Final Third",min_value= 0 , max_value=240 , step= 1 , value=5)
    if st.button("Predict"):
        result = Prediction(A,B,C, Dist, D, PrgDist, E,F, CrsPA, PrgP, G)
        if result==0:
            st.text(f"You most probably a FW")
        elif result==1:
            st.text(f"You most probably a MF")
        elif result==2:
            st.text(f"You most probably a GK")
        elif result==3:
            st.text(f"You most probably a DF")
        
    
    

Main()
