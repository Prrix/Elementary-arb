# import streamlit as st
# from streamlit_extras.metric_cards import style_metric_cards
# from streamlit_extras.card import card

# # Define the layout with three columns
# # col1, col2, col3 = st.columns(3)
# col1, col2 = st.columns(2, gap="large")

# # First row of input boxes
# with col1:
#     st.header("Account 1", anchor="left")
#     odds1 = st.number_input("Odds 1", value=0.0)
#     limit1 = st.number_input("Limit 1", value=0.0)
#     account_balance1 = st.number_input("Account Balance 1", value=0.0)

# # Account 2 input boxes
# with col2:
#     st.header("Account 2", anchor="right")
#     odds2 = st.number_input("Odds 2", value=0.0)
#     limit2 = st.number_input("Limit 2", value=0.0)
#     account_balance2 = st.number_input("Account Balance 2", value=0.0)
# # with col1:
# #     odds1 = st.number_input("Odds 1", value=0.0)
# # with col2:
# #     limit1 = st.number_input("Limit 1", value=0.0)
# # with col3:
# #     account_balance1 = st.number_input("Account Balance 1", value=0.0)

# # # Second row of input boxes
# # with col1:
# #     odds2 = st.number_input("Odds 2", value=0.0)
# # with col2:
# #     limit2 = st.number_input("Limit 2", value=0.0)
# # with col3:
# #     account_balance2 = st.number_input("Account Balance 2", value=0.0)

# # Button to run
# button_placeholder = st.empty()
# with button_placeholder:
#     run_button = st.button(
#         "Run",
#         key="run_button",
#         use_container_width=True,
#         kwargs={"height": 60},
#     )
# if run_button and (
#     odds1 > 0
#     and odds2 > 0
#     # and limit1 > 0
#     # and limit2 > 0
#     # and account_balance1 > 0
#     # and account_balance2 > 0
# ):

#     # Calculate investments based on limits and account balances
#     invest1 = min(limit1, account_balance1)
#     invest2 = min(limit2, account_balance2)

#     # Calculate potential profit and profit percentage
#     profit_percent = 100 - (1 / odds1 + 1 / odds2) * 100

#     if profit_percent < 0:
#         style_metric_cards(
#             border_left_color="red", border_color="red", background_color="black"
#         )
#     else:
#         style_metric_cards(
#             border_left_color="grren", border_color="green", background_color="black"
#         )

#     if odds1 * invest1 < odds2 * invest2:
#         investment = {
#             "odds1": invest1,
#             "odds2": odds1 * invest1 / odds2,
#         }
#     else:
#         investment = {
#             "odds2": invest2,
#             "odds1": odds2 * invest2 / odds1,
#         }

#     col1.metric(
#         label="Profit Percentage",
#         value=f"{profit_percent:.2f}%",
#     )
#     col2.metric(
#         label="Total Investment",
#         value=f"{profit_percent:.2f}%",
#     )
#     col1.metric(label="Invest1 ", value=f"""{investment["odds1"]:.2f}""")
#     col2.metric(label="Invest2", value=f"""{investment["odds2"]:.2f}""")
#     col1.metric(label="Payout", value=f"""{(odds2*investment["odds2"]):.2f}""")

#     # col3.metric(label="Gain", value=5000, delta=1000)
#     # if(odds1> odds2):
#     #     investment = {
#     #         "odds1": invest1,
#     #         "odds2" : odds1*invest1/odds2,
#     #     }

#     # Display calculated values in cards


import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.card import card

# Define a form with the button inside it
with st.form(key="arbitrage_form"):
    # Define the layout with two columns
    col1, col2 = st.columns(2, gap="large")

    # First row of input boxes
    with col1:
        st.header("Account 1", anchor="left")
        odds1 = st.number_input("Odds 1", value=0.0, key="odds1")
        limit1 = st.number_input("Limit 1", value=0.0, key="limit1")
        account_balance1 = st.number_input(
            "Account Balance 1", value=0.0, key="account_balance1"
        )

    # Account 2 input boxes
    with col2:
        st.header("Account 2", anchor="right")
        odds2 = st.number_input("Odds 2", value=0.0, key="odds2")
        limit2 = st.number_input("Limit 2", value=0.0, key="limit2")
        account_balance2 = st.number_input(
            "Account Balance 2", value=0.0, key="account_balance2"
        )

    # Button to run
    run_button = st.form_submit_button(
        "Run",
        use_container_width=True,
    )

if run_button and (odds1 > 0 and odds2 > 0):
    # Calculate investments based on limits and account balances
    invest1 = min(limit1, account_balance1)
    invest2 = min(limit2, account_balance2)

    # Calculate potential profit and profit percentage
    profit_percent = 100 - (1 / odds1 + 1 / odds2) * 100

    if profit_percent < 0:
        style_metric_cards(
            border_left_color="red", border_color="red", background_color="black"
        )
    else:
        style_metric_cards(
            border_left_color="green", border_color="green", background_color="black"
        )

    if odds1 * invest1 < odds2 * invest2:
        investment = {
            "odds1": invest1,
            "odds2": odds1 * invest1 / odds2,
        }
    else:
        investment = {
            "odds2": invest2,
            "odds1": odds2 * invest2 / odds1,
        }
    profit = investment["odds1"] * odds1 - investment["odds1"] - investment["odds2"]
    st.markdown("---")
    # Displaying metrics with custom styling
    col1, col2 = st.columns(2, gap="large")
    col1.metric(
        label="Profit Percentage",
        value=f"{profit_percent:.2f}%",
    )
    col2.metric(
        label="Total Investment",
        value=f"{profit_percent:.2f}%",
    )
    col1.metric(label="Invest1", value=f"{investment['odds1']:.2f}")
    col2.metric(label="Invest2", value=f"{investment['odds2']:.2f}")
    col1.metric(label="Payout", value=f"{(odds2 * investment['odds2']):.2f}")
    # col1.metric(label="Payout", value=f"{(odds2 * investment['odds2']):.2f}")
    col2.metric(label="Profit", value=f"{(profit):.2f}")
