import pandas as pd, json,requests,streamlit as st #type:ignore


url = 'https://us-central1-project-finance-400806.cloudfunctions.net/getFunctionLogs'

def getNewData(rows):
    input_data = {'rows':rows}
    result = requests.post(url,json=input_data)

    if result.status_code == 200:
        data = json.loads(result.text)
        data = pd.DataFrame(data)
        return pd.DataFrame(data)
    else:
        print(result.status_code)
        st.error(f'Error occurred: {result.status_code}', icon="🚨")

st.title("Function Status")
placeholder = st.empty()
while True:
    df = getNewData(100)
    
    with placeholder.container():
        st.dataframe(df)