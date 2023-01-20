import streamlit as st
from prototype_predict import load_model, get_prediction



# SETTING PAGE CONFIG TO WIDE MODE
st.set_page_config(layout="wide")

st.title("News Article Answer Model")


def main():
    st.title("News Article Answer Model")

    # 모델 불러오기
    model, tokenizer = load_model()
    # 데이터 받기
    with st.form(key="입력 from"):
        sentence = st.text_input("Question")
        st.form_submit_button("Submit")


    prediction, df = get_prediction(model, tokenizer, sentence)
    context = df['context'][0]
    st.write(f'label is {prediction}')
    st.write(f'label is {context}')

main()