import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.card import card

st.set_page_config(page_title="Arbitrage Calculator", page_icon="🔧")

same_odds = st.checkbox("Same as old odds")

with st.form(key="arbitrage_form"):
    # Define the layout with two columns
    col1, col2 = st.columns(2, gap="large")

    # First row of input boxes
    with col1:
        st.header("Account 1", anchor="left")
        old_odds1 = st.number_input("Old Odds 1", value=0.0, key="odds1")
        invested1 = st.number_input("Invested 1", value=0.0, key="invested1")
        new_odds1 = st.number_input(
            "New Odds 1", value=old_odds1 if same_odds else 0.0, key="new_odds1"
        )

    # Account 2 input boxes
    with col2:
        st.header("Account 2", anchor="right")
        old_odds2 = st.number_input("Odds 2", value=0.0, key="odds2")
        invested2 = st.number_input("Invested 2", value=0.0, key="invested2")
        new_odds2 = st.number_input(
            "New Odds 2", value=old_odds2 if same_odds else 0.0, key="new_odds2"
        )

    run_button = st.form_submit_button(
        "Run",
        use_container_width=True,
    )

if run_button and (old_odds1 > 0 and old_odds2 > 0):

    payout1 = invested1 * old_odds1
    payout2 = invested2 * old_odds2
    delta = True if (payout1 - payout2) > 0 else False
    print(payout1 - payout2)
    if delta:

        to_invest = (payout1 - payout2) / new_odds2
        payout2 = payout1
    else:
        to_invest = (payout2 - payout1) / new_odds1
        payout1 = payout2

    col1, col2 = st.columns(2)

    account_no = 2 if delta else 1
    col1.metric(label=f"Invest Into", value=f"Account {account_no}")
    col2.metric(label=f"Invest{account_no}", value=f"{to_invest:.2f}")

    col1.metric(
        label=f"Profit", value=f"{abs(payout1 - invested1 - invested2 - to_invest):.2f}"
    )
    col2.metric(
        label=f"Profit Percentage",
        value=f"{(((payout1 - invested1 - invested2 - to_invest)/(invested1 +invested2 + to_invest))*100):.2f%}",
    )
