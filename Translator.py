import requests
import PyPDF2
import streamlit as st
from io import StringIO

# تنظیمات سبک و جهت برای RTL
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:opez,wght@9..40,500&family=Noto+Sans+Arabic:wght@500&display=swap');
html{direction: rtl}
.st-emotion-cache-1fttcpj , .st-emotion-cache-nwtri{display:none;}
.st-emotion-cache-5rimss p{text-align:right; font-family: 'DM Sans', sans-serif;
font-family: 'Noto Sans Arabic', sans-serif;}
pre{text-align:left;}
h1,h2,h3,h4,h5,h6{font-family: 'Noto Sans Arabic', sans-serif;}
span,p,a,button,ol,li {text-align:right; font-family: 'DM Sans', sans-serif;}
</style>
""", unsafe_allow_html=True)

# تنظیمات API
API_URL = 'https://api.one-api.ir/translate/v1/google/'
API_TOKEN = '388704:67bdd1ea1d2dc'  # جایگزین با توکن API خود

def translate_text(source, target, text):
    """ترجمه یک متن با استفاده از API"""
    headers = {
        'one-api-token': API_TOKEN,
        'Content-Type': 'application/json'
    }
    
    data = {
        'source': source,
        'target': target,
        'text': text
    }
    
    response = requests.post(API_URL, json=data, headers=headers)
    
    if response.status_code == 200:
        return response.json().get('result', 'Translation not found')
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")

def translate_file(file, source, target):
    """ترجمه محتوای یک فایل txt یا PDF"""
    if file.name.endswith('.txt'):
        text = StringIO(file.getvalue().decode("utf-8")).read()
    elif file.name.endswith('.pdf'):
        text = ''
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            text += page.extract_text()
    else:
        raise ValueError('Unsupported file type. Only .txt and .pdf are supported.')

    return translate_text(source, target, text)

# لیست زبان‌ها
languages = {
    "انگلیسی": "en",
    "فارسی": "fa",
    "عربی": "ar",
    "فرانسوی": "fr",
    "آلمانی": "de",
    "اسپانیایی": "es",
    "چینی": "zh",
    "روسی": "ru",
    "ژاپنی": "ja",
    "ایتالیایی": "it"
}

# رابط کاربری Streamlit
st.title("مترجم متن")

source_lang = st.selectbox("زبان مبدأ", list(languages.keys()), index=0)
target_lang = st.selectbox("زبان مقصد", list(languages.keys()), index=1)

text_input = st.text_area("متن برای ترجمه")

translate_button = st.button("ترجمه متن")
if translate_button and text_input:
    try:
        translated_text = translate_text(languages[source_lang], languages[target_lang], text_input)
        st.success(translated_text)
    except Exception as e:
        st.error(f"خطایی رخ داد: {e}")

st.header("یا")

uploaded_file = st.file_uploader("فایل آپلود کنید (txt یا pdf)", type=['txt', 'pdf'])
translate_file_button = st.button("ترجمه فایل")
if translate_file_button and uploaded_file:
    try:
        translated_text = translate_file(uploaded_file, languages[source_lang], languages[target_lang])
        st.success(translated_text)
    except Exception as e:
        st.error(f"خطایی رخ داد: {e}")
