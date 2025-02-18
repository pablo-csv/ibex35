import streamlit as st
import pandas as pd

def main():
    # load data
    df = pd.read_csv('IBEX.csv', encoding='utf-8')

    # date as index
    df.rename(columns={'Unnamed: 0': 'dia'}, inplace=True)
    df['dia'] = pd.to_datetime(df['dia'], format='ISO8601')
    df.set_index('dia', inplace=True)

    # title
    st.title("IBEX close prices")

    # date slider
    min_date = df.index.min().date()
    max_date = df.index.max().date()

    period = st.slider(
        "Period",
        min_value=min_date,
        max_value=max_date,
        value=(min_date, max_date),
        format="YYYY-MM-DD"
    )

    # get companies
    companies = sorted(df.columns.tolist())

    # selection
    select_all = st.checkbox("Select all", value=False)

    selected_comps = st.multiselect(
        "",
        companies,
        default=companies if select_all else []
    )

    # filter
    df_filtered= df.loc[
        (df.index >= pd.to_datetime(period[0])) & (df.index <= pd.to_datetime(period[1])), 
        selected_comps
    ]

    # graph
    if not df_filtered.empty:
        st.line_chart(df_filtered)
    else:
        st.warning("No data available.")

if __name__ == "__main__":
    main()
