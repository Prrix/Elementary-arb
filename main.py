import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.card import card

st.set_page_config(page_title="Arbitrage Calculator", page_icon=":moneybag:")


def layout_arb_prrix(max_profit_percent, investment, profit_win, payout):
    col1, col2 = st.columns(2, gap="large")
    col1.metric(
        label="Max Profit Percentage",
        value=f"{max_profit_percent:.2f}%",
    )
    col2.metric(
        label="Total Investment",
        value=f"""{(investment["odds1"] + investment["odds2"]):.2f}""",
    )
    col1.metric(label="Invest1", value=f"{investment['odds1']:.2f}")
    col2.metric(label="Invest2", value=f"{investment['odds2']:.2f}")
    col1.metric(label="Payout 1 Win", value=f"{payout['odds1']:.2f}")
    col2.metric(label="Payout 2 Win", value=f"{payout['odds2']:.2f}")
    col1.metric(label="Profit 1 Win", value=f"{profit_win['odds1']:.2f}")
    col2.metric(label="Profit 2 Win", value=f"{profit_win['odds2']:.2f}")


def layout_arb(profit_percent, investment, odds2, profit):
    col1, col2 = st.columns(2, gap="large")
    col1.metric(
        label="Profit Percentage",
        value=f"{profit_percent:.2f}%",
    )
    col2.metric(
        label="Total Investment",
        value=f"""{(investment["odds1"] + investment["odds2"]):.2f}""",
    )
    col1.metric(label="Invest1", value=f"{investment['odds1']:.2f}")
    col2.metric(label="Invest2", value=f"{investment['odds2']:.2f}")
    col1.metric(label="Payout", value=f"{(odds2 * investment['odds2']):.2f}")
    # col1.metric(label="Payout", value=f"{(odds2 * investment['odds2']):.2f}")
    col2.metric(label="Profit", value=f"{(profit):.2f}")


def arb_calculate(odds1, odds2):
    profit_percent = 100 - (1 / odds1 + 1 / odds2) * 100

    if profit_percent < 0:
        style_metric_cards(
            border_left_color="red", border_color="red", background_color="black"
        )
    else:
        style_metric_cards(
            border_left_color="green", border_color="green", background_color="black"
        )
    return profit_percent


def not_deposit_arb(limit1, limit2, odds1, odds2, total_balance):
    account_balance1 = odds2 * total_balance / (odds1 + odds2)
    account_balance2 = total_balance - account_balance1
    deposit_arb(limit1, limit2, odds1, odds2, account_balance1, account_balance2)


def not_deposit_arb_prrix(limit1, limit2, odds1, odds2, total_balance):
    if odds2 > odds1:
        deposit_arb_prrix(
            limit1,
            limit2,
            odds1,
            odds2,
            total_balance - total_balance / odds2,
            total_balance / odds2,
        )
    else:
        deposit_arb_prrix(
            limit1,
            limit2,
            odds1,
            odds2,
            total_balance / odds1,
            total_balance - total_balance / odds1,
        )
    return


def deposit_arb(limit1, limit2, odds1, odds2, account_balance1, account_balance2):
    invest1 = min(limit1, account_balance1)
    invest2 = min(limit2, account_balance2)

    # Calculate potential profit and profit percentage
    profit_percent = arb_calculate(odds1, odds2)

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
    layout_arb(profit_percent, investment, odds2, profit)


def deposit_arb_prrix(limit1, limit2, odds1, odds2, account_balance1, account_balance2):
    invest1 = min(limit1, account_balance1)
    invest2 = min(limit2, account_balance2)

    if odds2 > odds1:
        investment = {"odds2": max(invest2, invest1 / (odds2 - 1)), "odds1": invest1}
        investment["odds1"] = investment["odds2"] * (odds2 - 1)
        max_profit_percent = (
            investment["odds1"] * odds1 - investment["odds1"] - investment["odds2"]
        ) / (investment["odds1"] + investment["odds2"])
    else:
        investment = {"odds1": max(invest1, invest2 / (odds1 - 1)), "odds2": invest2}
        investment["odds2"] = investment["odds1"] * (odds1 - 1)
        max_profit_percent = (
            investment["odds2"] * odds2 - investment["odds2"] - investment["odds1"]
        ) / (investment["odds1"] + investment["odds2"])
        # invest1 = invest2 * (odds2 - 1)
    if max_profit_percent < 0:
        style_metric_cards(
            border_left_color="red", border_color="red", background_color="black"
        )
    else:
        style_metric_cards(
            border_left_color="green", border_color="green", background_color="black"
        )

    # Calculate potential profit and profit percentage
    max_profit_percent = max_profit_percent * 100
    profit_1_win = (
        investment["odds1"] * odds1 - investment["odds1"] - investment["odds2"]
    )
    payout_1_win = investment["odds1"] * odds1
    profit_2_win = (
        investment["odds2"] * odds2 - investment["odds2"] - investment["odds1"]
    )
    payout_2_win = investment["odds2"] * odds2
    st.markdown("---")
    layout_arb_prrix(
        max_profit_percent,
        investment,
        {
            "odds1": profit_1_win,
            "odds2": profit_2_win,
        },
        {
            "odds1": payout_1_win,
            "odds2": payout_2_win,
        },
    )


arb_type = st.radio(
    "Option 1",
    options=[True, False],
    format_func=lambda x: "Basic Arb" if x else "PrrixArb",
    label_visibility="collapsed",
    horizontal=True,
)
option_deposit = st.radio(
    "Option 1",
    options=[True, False],
    format_func=lambda x: "Deposited" if x else "Not Deposited",
    label_visibility="collapsed",
    horizontal=True,
)

with st.form(key="arbitrage_form"):
    # Define the layout with two columns
    col1, col2 = st.columns(2, gap="large")

    # First row of input boxes
    with col1:
        st.header("Account 1", anchor="left")
        odds1 = st.number_input("Odds 1", value=0.0, key="odds1")
        limit1 = st.number_input("Limit 1", value=0.0, key="limit1")
        # with tabs[0]:
        if option_deposit:
            account_balance1 = st.number_input(
                "Account Balance 1", value=0.0, key="account_balance1"
            )
        # account_balance1 = st.number_input(
        #     "Account Balance 1", value=0.0, key="account_balance1"
        # )

    # Account 2 input boxes
    with col2:
        st.header("Account 2", anchor="right")
        odds2 = st.number_input("Odds 2", value=0.0, key="odds2")
        limit2 = st.number_input("Limit 2", value=0.0, key="limit2")
        # with tabs[0]:
        if option_deposit:
            account_balance2 = st.number_input(
                "Account Balance 2", value=0.0, key="account_balance2"
            )
    if not option_deposit:
        total_balance = st.number_input("Total Balance", value=0.0, key="total_balance")
    # total_balance = st.number_input("Total Balance", value=0.0, key="total_balance")
    # Button to run
    run_button = st.form_submit_button(
        "Run",
        use_container_width=True,
    )
if arb_type:

    if run_button and option_deposit and (odds1 > 0 and odds2 > 0):
        deposit_arb(limit1, limit2, odds1, odds2, account_balance1, account_balance2)
    if run_button and not option_deposit and (odds1 > 0 and odds2 > 0):
        not_deposit_arb(limit1, limit2, odds1, odds2, total_balance)
else:
    if run_button and option_deposit and (odds1 > 0 and odds2 > 0):
        deposit_arb_prrix(
            limit1, limit2, odds1, odds2, account_balance1, account_balance2
        )
    if run_button and not option_deposit and (odds1 > 0 and odds2 > 0):
        not_deposit_arb_prrix(limit1, limit2, odds1, odds2, total_balance)

    # Calculate investments based on limits and account balances

    # Displaying metrics with custom styling
