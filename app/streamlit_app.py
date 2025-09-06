import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from streamlit_option_menu import option_menu
from pusula_chatbot import pusula_advisor

# --- 1. Veri Yükleme Fonksiyonu ---
@st.cache_data
def load_data(file_path):
    """Veri setini yükler ve temel ön işleme yapar."""
    df = pd.read_excel(file_path)
    # Kolon isimlerini temizleme
    df.columns = df.columns.str.strip()
    return df

# --- 2. Streamlit Uygulaması ---
st.set_page_config(layout="wide", page_title="Pusula Dashboard", page_icon="🏥")

# Veriyi yükle
data_path = '../data/Talent_Academy_Case_DT_2025.xlsx'
try:
    df = load_data(data_path)
except FileNotFoundError:
    st.error(f"'{data_path}' dosyası bulunamadı. Lütfen dosyayı projenizin 'data' klasörüne koyduğunuzdan emin olun.")
    st.stop()

# Sidebar Menüsü
selected = option_menu(
        menu_title="Ana Menü",
        options=["Genel Bakış", "Görsel Analiz", "Chatbot"],
        icons=["house", "bar-chart", "chat"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {
                "background-color": "#0F172A",
                "border-radius": "12px",
                "box-shadow": "0 4px 12px rgba(0,0,0,0.5)"
            },
            "icon": {
                "color": "#FFFFFF",
                "font-size": "24px"
            },
            "nav-link": {
                "font-size": "18px",
                "color": "#E5E5E5",
                "text-align": "center",
                "margin": "5px",
                "padding": "12px 20px",
                "border-radius": "8px",
                "--hover-color": "#1F7A3A",
                "transition": "all 0.3s ease-in-out"
            },
            "nav-link-selected": {
                "background-color": "#C5B358",
                "color": "#0F172A",
                "font-weight": "bold",
                "box-shadow": "0 0 10px rgba(197,179,88,0.7)"
            }
        }

    )

# --- Sayfa İçerikleri ---

# 1. Genel Bakış Sayfası
if selected == "Genel Bakış":
    st.title("📊 Veri Seti Genel Bakış")
    st.write("Veri setinin ilk hali ve temel profil raporu.")

    st.subheader("Veri Setinin İlk 5 Satırı")
    st.dataframe(df.head())

    st.subheader("Veri Seti Bilgileri")
    buffer = pd.DataFrame({
        'Sütun Adı': df.columns,
        'Veri Tipi': df.dtypes,
        'Eksik Değer Sayısı': df.isnull().sum()
    })
    st.dataframe(buffer)


# 2. Görsel Analiz Sayfası
elif selected == "Görsel Analiz":
    st.title("📈 Görsel Analizler")
    st.write("Seçtiğiniz verilere göre dinamik grafikler oluşturun.")

    st.subheader("Hasta Demografisi")
    col1, col2 = st.columns(2)
    with col1:
        fig_gender = px.pie(df, names='Cinsiyet', title='Cinsiyete Göre Dağılım', hole=0.3)
        st.plotly_chart(fig_gender, use_container_width=True)
    with col2:
        fig_age = px.histogram(df.dropna(subset=['Yas']), x='Yas', nbins=20, title='Yaş Dağılımı')
        st.plotly_chart(fig_age, use_container_width=True)

    st.subheader("Tedavi ve Bölüm Analizi")
    col3, col4 = st.columns(2)
    with col3:
        fig_department = px.bar(df['Bolum'].value_counts(),
                                title='Bölümlere Göre Hasta Sayısı',
                                labels={'index': 'Bölüm', 'value': 'Hasta Sayısı'})
        st.plotly_chart(fig_department, use_container_width=True)
    with col4:
        fig_treatment = px.bar(df['TedaviAdi'].value_counts().head(10),
                               title='En Sık Uygulanan 10 Tedavi',
                               labels={'index': 'Tedavi Adı', 'value': 'Sayı'})
        st.plotly_chart(fig_treatment, use_container_width=True)

    st.subheader("Uygulama Süreleri")
    fig_duration = px.histogram(df, x='UygulamaSuresi', title='Uygulama Süresi Dağılımı', nbins=20)
    st.plotly_chart(fig_duration, use_container_width=True)

    # --- Dinamik Groupby Görselleştirme ---
    st.subheader("🔍 Dinamik GroupBy Görselleştirme")
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(exclude=[np.number]).columns.tolist()

    group_col = st.selectbox("Gruplamak istediğiniz kategorik değişken:", categorical_cols, index=0)
    value_col = st.selectbox("Analiz etmek istediğiniz sayısal değişken:", numeric_cols, index=0)
    agg_func = st.selectbox("Özetleme yöntemi:", ["mean", "sum", "count", "median", "max", "min"], index=0)
    chart_type = st.selectbox("Grafik tipi:", ["Bar", "Box", "Line"], index=0)

    if group_col and value_col:
        grouped_df = df.groupby(group_col)[value_col].agg(agg_func).reset_index()

        if chart_type == "Bar":
            fig_dynamic = px.bar(grouped_df, x=group_col, y=value_col,
                                 title=f"{group_col} bazında {value_col} ({agg_func})",
                                 labels={group_col: group_col, value_col: f"{agg_func} {value_col}"})
        elif chart_type == "Line":
            fig_dynamic = px.line(grouped_df, x=group_col, y=value_col,
                                  title=f"{group_col} bazında {value_col} ({agg_func})",
                                  markers=True)
        else:  # Box Plot (kutu grafiği için direkt orijinal df kullanıyoruz)
            fig_dynamic = px.box(df, x=group_col, y=value_col,
                                 title=f"{group_col} bazında {value_col} dağılımı")

        st.plotly_chart(fig_dynamic, use_container_width=True)

    # --- Dinamik Çoklu GroupBy Görselleştirme ---
    st.subheader("🔍 Dinamik Çoklu GroupBy Görselleştirme")
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(exclude=[np.number]).columns.tolist()

    group_cols = st.multiselect("Gruplamak istediğiniz kategorik değişken(ler):",
                                categorical_cols,
                                default=[categorical_cols[0]],
                                key="group_cols")

    value_col = st.selectbox("Analiz etmek istediğiniz sayısal değişken:",
                             numeric_cols,
                             index=0,
                             key="value_col")

    agg_func = st.selectbox("Özetleme yöntemi:",
                            ["mean", "sum", "count", "median", "max", "min"],
                            index=0,
                            key="agg_func")

    chart_type = st.selectbox("Grafik tipi:",
                              ["Bar", "Line", "Box"],
                              index=0,
                              key="chart_type")

    if group_cols and value_col:
        grouped_df = df.groupby(group_cols)[value_col].agg(agg_func).reset_index()

        # 2 kolonlu layout
        col1, col2 = st.columns(2)

        if chart_type == "Bar":
            fig_dynamic = px.bar(
                grouped_df,
                x=group_cols[0],
                y=value_col,
                color=group_cols[1] if len(group_cols) > 1 else None,
                barmode="group",
                title=f"{' + '.join(group_cols)} bazında {value_col} ({agg_func})",
                labels={value_col: f"{agg_func} {value_col}"}
            )
            col1.plotly_chart(fig_dynamic, use_container_width=True)

        elif chart_type == "Line":
            fig_dynamic = px.line(
                grouped_df,
                x=group_cols[0],
                y=value_col,
                color=group_cols[1] if len(group_cols) > 1 else None,
                markers=True,
                title=f"{' + '.join(group_cols)} bazında {value_col} ({agg_func})"
            )
            col2.plotly_chart(fig_dynamic, use_container_width=True)

        else:  # Box Plot
            fig_dynamic = px.box(
                df,
                x=group_cols[0],
                y=value_col,
                color=group_cols[1] if len(group_cols) > 1 else None,
                title=f"{' + '.join(group_cols)} bazında {value_col} dağılımı"
            )
            col1.plotly_chart(fig_dynamic, use_container_width=True)



elif selected == "Chatbot":
    st.info("Bu bölümde Pusula Talent Academy Case verisi ile ilgili sorularınızı sorabilirsiniz.")
    # Chat geçmişi
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # sohbeti temizle
    if st.button("🗑️ Sohbeti Temizle"):
        st.session_state.chat_history = []
        st.success("Sohbet geçmişi temizlendi!")

    # Kullanıcıdan giriş al
    user_input = st.chat_input("Veri seti ile ilgili sorularınızı buraya yazın...")

    # Sohbet kutusunu göster
    for role, message in st.session_state.chat_history:
        with st.chat_message(role):
            st.markdown(message)

    if user_input:
        # Kullanıcının mesajı
        st.session_state.chat_history.append(("user", user_input))
        with st.chat_message("user"):
            st.markdown(user_input)

        # Asistanın yanıtı
        with st.chat_message("assistant"):
            with st.spinner("Yanıtlanıyor..."):
                try:
                    answer = pusula_advisor(user_input)

                except Exception as e:
                    answer = f"Hata oluştu: {str(e)}"
                st.markdown(answer)
                st.session_state.chat_history.append(("assistant", answer))


