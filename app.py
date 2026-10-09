import streamlit as st
import json
import os

FILE_NAME = "articles.json"


st.set_page_config(page_title="База Знаний", page_icon="📚", layout="centered")

def load_articles():
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, "r", encoding="utf-8") as f:
        return json.load(f)

def save_articles(articles):
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=4)

articles = load_articles()

st.title("📚 Моя База Знаний и Статей")
st.write("Коллекция полезных материалов, заметок и ссылок")

st.divider()

st.sidebar.header("➕ Добавить статью")
with st.sidebar.form("add_form", clear_on_submit=True):
    title = st.text_input("Название статьи")
    category = st.text_input("Категория (например: Python, Math, English)")
    content = st.text_area("Текст статьи или ссылка")
    submit = st.form_submit_button("Сохранить")

if submit:
    if title and category and content:
        new_article = {
            "title": title.strip(),
            "category": category.strip().capitalize(),
            "content": content.strip()
        }
        articles.insert(0, new_article)
        save_articles(articles)
        st.sidebar.success(f"Статья '{title}' сохранена!")
        st.rerun()
    else:
        st.sidebar.error("Заполните все поля!")

search_query = st.text_input("🔍 Поиск по названию или категории", "")

filtered_articles = [
    a for a in articles 
    if search_query.lower() in a["title"].lower() or search_query.lower() in a["category"].lower()
]

st.subheader(f"Все статьи ({len(filtered_articles)})")

if not filtered_articles:
    st.info("Статей пока нет или ничего не найдено.")

for idx, article in enumerate(filtered_articles):
    with st.expander(f"📌 [{article['category']}] {article['title']}"):
        if article["content"].startswith("http://") or article["content"].startswith("https://"):
            st.markdown(f"[Открыть ссылку 🔗]({article['content']})")
        else:
            st.write(article["content"])
        
        if st.button("Удалить статью", key=f"del_{idx}"):
            articles.remove(article)
            save_articles(articles)
            st.success("Удалено!")
            st.rerun()