import pandas as pd,json,requests,streamlit as st,time #type:ignore

def getNewData(rows: int) -> pd.DataFrame:
    input_data = {'rows': rows}
    result = requests.post('https://us-central1-project-finance-400806.cloudfunctions.net/getFunctionLogs', json=input_data)

    if result.status_code == 200:
        data = json.loads(result.text)
        return pd.DataFrame(data)
    else:
        print(result.status_code)
        st.error(f'Error occurred: {result.status_code}', icon="🚨")
        return pd.DataFrame()  # return an empty DataFrame in case of error

# UI start
st.set_page_config(layout="wide")
st.title("Function Status")
placeholder = st.empty()

while True:
    df = getNewData(15)
    if df.empty:
        continue  # skip if no data is returned

    df['time'] = pd.to_datetime(df['time'], format='%c')

    # Group by time and function, then count the occurrences
    df_counts = df.groupby(['time', 'function']).size().reset_index(name='count')

    # Pivot the DataFrame to have functions as columns and times as index
    df_pivot = df_counts.pivot(index='time', columns='function', values='count').fillna(0)

    with placeholder.container():
        st.write(df_pivot)
        # Display first and last time and their difference
        if not df.empty:
            st.write(f"Time difference: {df['time'].iloc[-1] - df['time'].iloc[0]}")
            st.dataframe(df)

        # Plotting the line chart
        st.line_chart(df_pivot)
        
    time.sleep(0.1)
