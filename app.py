import streamlit as st 
import pandas as pd

# Load the data
@st.cache_data
def load_data():
    aggregated_rounds = pd.read_excel("aggregated_round_win_percentages.xlsx", sheet_name=None)
    test_predictions = pd.read_excel("test_with_predictions.xlsx")
    test_predictions_elo = pd.read_excel("test_with_predictionselo.xlsx")
    
    return aggregated_rounds, test_predictions, test_predictions_elo

aggregated_rounds, test_predictions, test_predictions_elo = load_data()

# Sidebar Navigation
st.sidebar.title("🏀 **March Madness Predictions**")

st.sidebar.success("📊 **Developed for interactive exploration of tournament predictions.**")

st.sidebar.info("🔮 **Simulated Final 4:**\n- 🏀 **Auburn**\n- 🏀 **Duke**\n- 🏀 **Texas Tech**\n- 🏀 **Houston**")

st.sidebar.info("🏆 **Simulated Champion:** **Auburn**")

st.sidebar.info("🏆 **Dark Horse Champion:** **Texas Tech**")

st.sidebar.warning("📊 **Data Sources:**\n🔹 **KenPom.com**\n🔹 **BartTorvik.com**\n🔹 **Historical NCAA Tournament Data**")
st.sidebar.info("📈 All predictions are made using a Gradient Boosting Regressor (GBR) model. This model is trained and tested on NCAA tournament games from the past 10 years.")
st.sidebar.info("By David Mustard")

# Tabs for Navigation
tab1, tab2, tab3 = st.tabs(["🏆 Tournament Probabilities", "📋 Game Predictions", "📈 Team Ratings"])

# Tab 1: Tournament Probabilities
with tab1:
    st.markdown("## 📊 Tournament Probabilities")
    st.write("Filter by **Seed** and **Region** to view a team's chances of making each round. This is based on 10,000 simulations of the tournament.")

    df_list = [df for df in aggregated_rounds.values()]
    full_df = pd.concat(df_list, ignore_index=True)

    col1, col2 = st.columns(2)
    seed_options = ["All"] + [str(i) for i in range(1, 17)]
    region_options = ["All"] + sorted(full_df["Region"].dropna().unique().tolist())

    with col1:
        selected_seed = st.multiselect("Filter by Seed:", seed_options, default=["All"])
    with col2:
        selected_region = st.multiselect("Filter by Region:", region_options, default=["All"])

    if st.button("Reset Filters"):
        selected_seed, selected_region = ["All"], ["All"]

    if "All" not in selected_seed:
        full_df = full_df[full_df["Seed"].astype(str).isin(selected_seed)]
    if "All" not in selected_region:
        full_df = full_df[full_df["Region"].isin(selected_region)]

    full_df = full_df.drop(columns=["Round"], errors="ignore")

    st.dataframe(
        full_df.style.format({
            "Round of 32": "{:.1%}",
            "Sweet 16": "{:.1%}",
            "Elite 8": "{:.1%}",
            "Final 4": "{:.1%}",
            "Title Game": "{:.1%}",
            "Champion": "{:.1%}"
        }),
        use_container_width=True
    )

# Tab 2: Game Predictions
with tab2:
    st.markdown("## 📋 Second Round Matchup Predictions")
    st.write("Predicted game outcomes. ***These predictions do not account for injuries.***")
    st.dataframe(test_predictions, use_container_width=True)


# Tab 3: Team Ratings
with tab3:
    st.markdown("## 📈 Team Ratings")
    st.write("Team Ratings against an average team in the field. ***These predictions do not account for injuries.***")
    st.dataframe(test_predictions_elo, use_container_width=True)
