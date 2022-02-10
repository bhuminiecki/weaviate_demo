import pandas as pd
import streamlit as st
import warnings
warnings.filterwarnings("ignore")

import weaviate
client = weaviate.Client("http://localhost:8080")

#input for the searched text
search_text = st.text_input('Search')

#create a filter that looks for similar phrases, certainty defines minimal similarity threshold at which the phrase is accepted
near_text_filter_syn = {
    'concepts': [search_text],
    "certainty": 0.33
}

#constructing a query, additional "certainty" field returns similarity of given phrase to searched text
query_result_syn = client.query\
    .get("Thesis", ["name"])\
    .with_near_text(near_text_filter_syn)\
    .with_additional(['certainty'])\
    .with_limit(10)\
    .do()

if search_text != "" : #don't perform search if the field is empty
    query_results_syn = [(x['name'],x['_additional']['certainty']) for x in  query_result_syn['data']['Get']["Thesis"]]

    df3 = pd.DataFrame(query_results_syn, columns=['Thesis', 'Certainty'])
    st.dataframe(df3, width=1000)

