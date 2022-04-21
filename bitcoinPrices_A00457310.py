import pandas as pd
import requests
import streamlit as st


def fetchData(currency, numDays):
    # Exception Handling
    currency, numDays = handleEdgeCase(currency, numDays)

    # Calling api using requests library
    _data = requests.get(
        f"https://api.coingecko.com/api/v3/coins/bitcoin/market_chart",
        params={
            "vs_currency": currency,
            "days": numDays,
            "interval": "daily"
        }
    )
    return _data.json()


def handleEdgeCase(currency, numDays):
    if currency is None:
        print("Currency Undefined, using default value")
        currency = "cad"
    if numDays is None:
        print("numDays Undefined, using default value")
        numDays = 1
    return currency, numDays


def main():
    st.title('A00457310 Bitcoin prices')
    numDays = st.slider(
        label="No of days",
        min_value=1,
        max_value=365,
        format=None
    )
    currency = st.radio(
        label="Currency",
        options=["INR", "CAD", "USD"],
        index=0
    ).lower()

    # fetch Data
    _data = fetchData(
        currency=currency,
        numDays=numDays
    )

    df = pd.DataFrame(
        data=(elem[1] for elem in _data['prices'])
    )

    dfTillNumDays = df[df.index < numDays]
    mean = (dfTillNumDays.mean()).iloc[0]

    st.line_chart(
        data=df,
        use_container_width=True
    )
    st.write(f"Average price during this time was {mean} {currency}")


if __name__ == "__main__":
    main()
