import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
from prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE

load_dotenv()

st.set_page_config(
    page_title="Telegram Minutes AI",
    page_icon="📝",
    layout="centered"
)

st.title("📝 صورت‌جلسه هوشمند از چت تلگرام")
st.caption("تبدیل چت‌های شلوغ به صورت‌جلسه تمیز + لیست تسک‌ها | قدرت‌گرفته از DeepSeek")

with st.sidebar:
    st.header("تنظیمات")
    api_key = st.text_input("DeepSeek API Key", value=os.getenv("DEEPSEEK_API_KEY", ""), type="password")
    base_url = st.text_input("Base URL", value=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"))
    model = st.selectbox("مدل", ["deepseek-chat", "deepseek-reasoner", "deepseek-flash"], index=0)
    st.markdown("---")
    st.markdown("**نکته:** اگر از درگاه ایرانی استفاده می‌کنید، Base URL را تغییر دهید.")

tab1, tab2 = st.tabs(["متن چت", "آپلود فایل"])

chat_text = ""

with tab1:
    chat_text = st.text_area(
        "متن چت را اینجا پیست کنید:",
        height=300,
        placeholder="مثال:\nعلی: سلام بچه‌ها\nسارا: پروژه رو تا چهارشنبه باید تموم کنیم\n..."
    )

with tab2:
    uploaded_file = st.file_uploader("فایل .txt یا export تلگرام را آپلود کنید", type=["txt"])
    if uploaded_file:
        chat_text = uploaded_file.read().decode("utf-8")

if st.button("🚀 تولید صورت‌جلسه", type="primary", use_container_width=True):
    if not chat_text.strip():
        st.warning("لطفاً متن چت را وارد کنید.")
    elif not api_key:
        st.error("لطفاً API Key را وارد کنید.")
    else:
        with st.spinner("در حال تولید صورت‌جلسه..."):
            try:
                client = OpenAI(
                    api_key=api_key,
                    base_url=base_url
                )

                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": USER_PROMPT_TEMPLATE.format(chat_text=chat_text)}
                    ],
                    temperature=0.3,
                    max_tokens=2000
                )

                result = response.choices[0].message.content

                st.success("صورت‌جلسه آماده شد!")
                st.markdown(result)

                st.download_button(
                    label="دانلود به صورت فایل متنی",
                    data=result,
                    file_name="meeting_minutes.txt",
                    mime="text/plain"
                )

            except Exception as e:
                st.error(f"خطا در ارتباط با مدل:\n{str(e)}")

st.markdown("---")
st.caption("ساخته شده برای تیم‌های ایرانی | استفاده از DeepSeek برای هزینه پایین")
