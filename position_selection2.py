
import streamlit as st
import joblib
import pandas as pd
import plotly.express as px
# Load models and scaler
res = joblib.load( "res.pkl")
Inputs = joblib.load( "Inputs.pkl")
Smote = joblib.load("smote.pkl")
scaler = joblib.load("Scaler.pkl")
model = joblib.load("Model.pkl")
df_EFL_Standing=pd.read_csv("FPL.csv")
df_EFL_Standing.index = df_EFL_Standing.index + 1
df_vis=pd.read_csv("FPL_vis.csv")

# Function to create a DataFrame for prediction
def Prediction(A, B, C, Dist, D, PrgDist, E, F, CrsPA, PrgP, G):
    df = pd.DataFrame(columns=['90s', 'Sh/90', 'SoT/90', 'Dist', 'Cmp%', 
                               'PrgDist', 'Cmp%_Short', 'Cmp%_Medium', 
                               'CrsPA', 'PrgP', '3/1'])
    df.at[0, "90s"] = A
    df.at[0, "Sh/90"] = B
    df.at[0, "SoT/90"] = C
    df.at[0, "Dist"] = Dist
    df.at[0, "Cmp%"] = D
    df.at[0, "PrgDist"] = PrgDist
    df.at[0, "Cmp%_Short"] = E
    df.at[0, "Cmp%_Medium"] = F
    df.at[0, "CrsPA"] = CrsPA
    df.at[0, "PrgP"] = PrgP
    df.at[0, "3/1"] = G

    df = scaler.transform(df)
    result = model.predict(df)
    return result[0]

# Main function to build the UI
def Main():
    st.sidebar.title("Premier League Season 22/23 ")
    
    # Sidebar selection
    option = st.sidebar.selectbox("Select an Option", ["Season Over View","Team Anaylsis","Predict Player Position"])
    
    if option == "Predict Player Position":
        st.title("Player Position Prediction")
        st.write("Input the statistics of a player, and the model will suggest the most likely position they play.")

        # User input sliders
        A = st.number_input("Match Played", min_value=0, max_value=38, step=1, value=25)
        B = st.number_input("Shots in Match", min_value=0, max_value=15, step=1, value=5)
        C = st.number_input("Shots on Target per Match", min_value=0, max_value=15, step=1, value=5)
        Dist = st.number_input("Average Distance of Shots (yards)", min_value=0, max_value=35, step=1, value=5)
        D = st.number_input("Pass Completion Percentage", min_value=0, max_value=100, step=1, value=75)
        PrgDist =st.number_input("Total distance, in yards, that completed passes have traveled towards the opponent's goal.", min_value=0, max_value=15000, step=1)
        E = st.number_input("Pass Completion % Short", min_value=0, max_value=100, step=1, value=75)
        F = st.number_input("Pass Completion % Medium", min_value=0, max_value=100, step=1, value=75)
        CrsPA = st.number_input("Crosses into Penalty Area", min_value=0, max_value=25, step=1, value=5)
        PrgP = st.number_input("Number of completed Progressive Passes", min_value=0, max_value=270, step=1, value=5)
        G = st.number_input("Passes into Final Third", min_value=0, max_value=240, step=1, value=5)

        if st.button("Predict"):
            result = Prediction(A, B, C, Dist, D, PrgDist, E, F, CrsPA, PrgP, G)
            position_map = {0: "DF", 1: "FW", 2: "GK", 3: "MF"}
            st.text(f"You most probably play as a {position_map[result]}.")

    elif option == "Season Over View":
        
        st.title("EPL 2022/2023 OverAll Stats")
        st.subheader("Standings of EFL")
        st.dataframe(df_EFL_Standing,width=2000,height=740)
        st.subheader("Top scoring teams in season")
        fig1=px.histogram(df_EFL_Standing.groupby("Team")["GF"].sum().sort_values(ascending=False).reset_index(),x="Team",y="GF",width=2000,text_auto=True)
        st.plotly_chart(fig1)         
        st.subheader("Top scorers in season")
        fig2=px.histogram(df_vis.groupby("Player")["Gls"].sum().sort_values(ascending=False).reset_index().head(20),x="Player",y="Gls",width=2000,text_auto=True)
        st.plotly_chart(fig2) 
        fig3=px.scatter(data_frame=df_vis.groupby("Player")[["xG","Gls"]].sum().sort_values(by="Gls",ascending=False).reset_index().head(20),x="Gls",y="xG",color="Player")
        st.subheader("A scatter plot between Goals scored and the Expected goals of top 20 player")
        st.plotly_chart(fig3)
        st.subheader("Top Assists in season")
        fig4=px.histogram(data_frame=df_vis.groupby("Player")["Ast"].sum().sort_values(ascending=False).reset_index().head(20),x="Player",y="Ast",text_auto=True)
        st.plotly_chart(fig4)
        st.subheader("Top players who completed passes in season")
        fig5=px.histogram(data_frame=df_vis.groupby(["Player","Squad"])["Cmp"].sum().sort_values(ascending=False).reset_index().head(20),x="Player",y="Cmp",text_auto=True)
        st.plotly_chart(fig5)
        st.subheader("Graph between completed passes and the persentage of successful passses attempted")
        fig6=px.scatter(data_frame=df_vis.groupby("Player")[["Cmp","Cmp%"]].sum().sort_values(by="Cmp",ascending=False).reset_index().head(20),x="Cmp",y="Cmp%",color="Player")
        st.plotly_chart(fig6)
        
    elif option == "Team Anaylsis":
        st.header('Team Anaylsis')
        
        clubs=df_vis["Squad"].unique()
        Club = st.selectbox("Select a Team",clubs)
        Posi=st.selectbox("Select a position",["FW","DF","MF","GK"])
        df_club=df_vis[df_vis["Squad"]==Club]
        st.subheader("Goals contribution")
        fig8=px.histogram(df_club[df_club["Pos"]==Posi].sort_values(by='Sh',ascending=False),y=["xA","xG","Ast","Gls"],x="Player",barmode="group")
        st.plotly_chart(fig8)
        st.caption("Gls: Gls")
        st.caption("Ast: Assists")
        st.caption("xG: Expected goals")
        st.caption("xA: Expected assists\t")
        st.divider()
        st.subheader("Passes of the players")
        fig7=px.histogram(df_club[df_club["Pos"]==Posi].sort_values(by='Cmp',ascending=False),y=["Cmp%","3/1","KP","PrgP"],x="Player",barmode="group")
        st.plotly_chart(fig7)
        st.caption("Cmp: Passes Completed\t")
        st.caption("3/1: Passes in the final third\t")
        st.caption("KP: Key passes\t")
        st.caption("PrgP: Number of progressive passes\t")
        
        
        
        
        
 
        
        

# Run the main function
if __name__ == "__main__":
    Main()
