"""
PDF Belge Asistanı - Google Gemini Edition
Kullanıcıların PDF dosyası yükleyip sorular sorabileceği bir Streamlit uygulaması.
"""

import streamlit as st
from PyPDF2 import PdfReader
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json
from datetime import datetime

# Ortam değişkenlerini yükle
load_dotenv()

# Sayfa yapılandırması
st.set_page_config(
    page_title="PDF Belge Asistanı",
    page_icon="📄",
    layout="wide"
)

# Başlık ve açıklama
st.title("📄 PDF Belge Asistanı")
st.markdown("PDF dosyanızı yükleyin ve içeriği hakkında sorular sorun! *(Google Gemini ile çalışır)*")


def extract_text_from_pdf(pdf_file):
    """
    PDF dosyasından metin çıkarır.
    
    Args:
        pdf_file: Yüklenen PDF dosyası
        
    Returns:
        tuple: (metin, sayfa_sayısı)
    """
    try:
        pdf_reader = PdfReader(pdf_file)
        text = ""
        page_count = len(pdf_reader.pages)
        
        for page_num, page in enumerate(pdf_reader.pages, 1):
            page_text = page.extract_text()
            text += f"\n--- Sayfa {page_num} ---\n{page_text}"
        
        return text, page_count
    except Exception as e:
        st.error(f"PDF okunurken hata oluştu: {str(e)}")
        return None, 0


def get_text_stats(text):
    """
    Metin istatistiklerini hesaplar.
    
    Args:
        text: Analiz edilecek metin
        
    Returns:
        dict: Karakter ve kelime sayısı
    """
    word_count = len(text.split())
    char_count = len(text)
    return {"words": word_count, "characters": char_count}


def initialize_gemini(model_name, api_key):
    """
    Google Gemini modelini başlatır.
    
    Args:
        model_name: Kullanılacak Gemini model adı
        api_key: Google API anahtarı
        
    Returns:
        GenerativeModel: Yapılandırılmış Gemini modeli
    """
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        return model
    except Exception as e:
        st.error(f"Model başlatılırken hata: {str(e)}")
        return None


def get_gemini_response(model, prompt, pdf_context, chat_history):
    """
    Gemini'den yanıt alır.
    
    Args:
        model: Gemini model instance
        prompt: Kullanıcı sorusu
        pdf_context: PDF içeriği
        chat_history: Sohbet geçmişi
        
    Returns:
        str: Model yanıtı
    """
    try:
        # Sistem mesajı ve context oluştur
        system_prompt = """Sen yardımsever bir PDF belge asistanısın. Kullanıcının yüklediği belge hakkında sorular sormasına yardımcı oluyorsun.
        
Belge İçeriği:
{pdf_context}

Önceki Konuşmalar:
{chat_history}

Kullanıcı Sorusu: {user_question}

Lütfen soruyu belge içeriğine göre yanıtla. Eğer bilgi belgede yoksa bunu belirt."""

        # Chat history formatla
        history_text = ""
        for msg in chat_history[-6:]:  # Son 3 sohbet (6 mesaj)
            role = "Kullanıcı" if msg["role"] == "user" else "Asistan"
            history_text += f"{role}: {msg['content']}\n"
        
        # Prompt'u hazırla
        full_prompt = system_prompt.format(
            pdf_context=pdf_context[:8000],  # Token limiti için
            chat_history=history_text,
            user_question=prompt
        )
        
        # Gemini'den yanıt al
        response = model.generate_content(full_prompt)
        return response.text
    
    except Exception as e:
        raise Exception(f"Gemini yanıt hatası: {str(e)}")


def export_chat_history(messages, format_type="txt"):
    """
    Sohbet geçmişini dışa aktarır.
    
    Args:
        messages: Sohbet mesajları listesi
        format_type: Dosya formatı ("txt" veya "json")
        
    Returns:
        str: Dışa aktarılacak içerik
    """
    if format_type == "txt":
        content = "PDF Belge Asistanı - Sohbet Geçmişi\n"
        content += "=" * 50 + "\n"
        content += f"Tarih: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        for msg in messages:
            role = "Kullanıcı" if msg["role"] == "user" else "Asistan"
            content += f"{role}: {msg['content']}\n\n"
        
        return content
    
    elif format_type == "json":
        export_data = {
            "export_date": datetime.now().isoformat(),
            "messages": messages
        }
        return json.dumps(export_data, ensure_ascii=False, indent=2)


# Session state başlatma
if "messages" not in st.session_state:
    st.session_state.messages = []

if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = None

if "pdf_info" not in st.session_state:
    st.session_state.pdf_info = {}

if "gemini_model" not in st.session_state:
    st.session_state.gemini_model = None


# Sidebar - Ayarlar ve Kontroller
with st.sidebar:
    st.header("⚙️ Ayarlar")
    
    # API Key kontrolü - GEMINI
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        api_key = st.text_input(
            "Google Gemini API Key", 
            type="password", 
            help="API key'inizi .env dosyasına veya buraya girebilirsiniz"
        )
    
    if api_key:
        st.success("✅ Gemini API Key yüklendi")
    else:
        st.warning("⚠️ Lütfen Gemini API Key girin")
    
    # Model seçimi - GEMINI MODELLER
    st.subheader("🤖 Model Seçimi")
    
    # Gemini model kategorileri ve açıklamaları
    model_info = {
        "gemini-1.5-flash": "⚡ Hızlı ve verimli (Önerilen)",
        "gemini-1.5-flash-8b": "🚀 Ultra hızlı, hafif model",
        "gemini-1.5-pro": "💎 En güçlü Gemini modeli",
        "gemini-2.0-flash-exp": "🧪 Deneysel yeni model"
    }
    
    selected_model = st.selectbox(
        "Model",
        list(model_info.keys()),
        index=0,
        format_func=lambda x: f"{x} - {model_info[x]}",
        help="Gemini modelleri ücretsiz kullanıma sahiptir"
    )
    
    # Model bilgisi
    st.info(f"ℹ️ Seçili: **{selected_model}**")
    
    # API Key alma bilgisi
    with st.expander("🔑 Gemini API Key nasıl alınır?"):
        st.markdown("""
        **Gemini API Key Alma Adımları:**
        1. [Google AI Studio](https://aistudio.google.com/app/apikey) sayfasına gidin
        2. Google hesabınızla giriş yapın
        3. "Get API Key" butonuna tıklayın
        4. API Key'i kopyalayın
        5. `.env` dosyasına `GEMINI_API_KEY=your_key_here` şeklinde ekleyin
        
        **Avantajlar:**
        - ✅ Ücretsiz kullanım limiti
        - ✅ Kredi kartı gerekmez
        - ✅ Güçlü modeller
        """)
    
    st.divider()
    
    # PDF yükleme
    st.subheader("📤 PDF Yükle")
    uploaded_file = st.file_uploader(
        "PDF Dosyası Seçin",
        type=["pdf"],
        help="Maksimum 10MB boyutunda PDF yükleyebilirsiniz"
    )
    
    # Dosya boyutu kontrolü
    if uploaded_file is not None:
        file_size_mb = uploaded_file.size / (1024 * 1024)
        
        if file_size_mb > 10:
            st.error("❌ Dosya boyutu 10MB'dan büyük olamaz!")
            uploaded_file = None
        else:
            st.info(f"📊 Dosya boyutu: {file_size_mb:.2f} MB")
            
            # PDF işleme
            if st.button("📖 PDF'i İşle", type="primary"):
                with st.spinner("PDF okunuyor..."):
                    text, page_count = extract_text_from_pdf(uploaded_file)
                    
                    if text:
                        st.session_state.pdf_text = text
                        st.session_state.pdf_info = {
                            "filename": uploaded_file.name,
                            "pages": page_count,
                            "stats": get_text_stats(text)
                        }
                        
                        # Gemini modelini başlat
                        if api_key:
                            with st.spinner(f"{selected_model} başlatılıyor..."):
                                model = initialize_gemini(selected_model, api_key)
                                if model:
                                    st.session_state.gemini_model = model
                                    st.success(f"✅ PDF ve Gemini modeli başarıyla yüklendi! ({page_count} sayfa)")
                                else:
                                    st.error("❌ Model başlatılamadı. API Key'inizi kontrol edin.")
                        else:
                            st.error("❌ Lütfen Gemini API Key girin!")
                        
                        if st.session_state.gemini_model:
                            st.rerun()
    
    # PDF bilgileri
    if st.session_state.pdf_text:
        st.divider()
        st.subheader("📋 Belge Bilgileri")
        st.write(f"**Dosya:** {st.session_state.pdf_info['filename']}")
        st.write(f"**Sayfa Sayısı:** {st.session_state.pdf_info['pages']}")
        st.write(f"**Kelime Sayısı:** {st.session_state.pdf_info['stats']['words']:,}")
        st.write(f"**Karakter Sayısı:** {st.session_state.pdf_info['stats']['characters']:,}")
        
        # PDF önizleme
        with st.expander("👁️ Metin Önizleme"):
            preview_text = st.session_state.pdf_text[:500] + "..."
            st.text_area("İlk 500 karakter", preview_text, height=150, disabled=True)
    
    # Sohbet kontrolü
    if st.session_state.messages:
        st.divider()
        st.subheader("💬 Sohbet Kontrolü")
        
        # Sohbeti temizle
        if st.button("🗑️ Sohbeti Temizle", type="secondary"):
            st.session_state.messages = []
            st.rerun()
        
        # Sohbeti indir
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="📄 TXT",
                data=export_chat_history(st.session_state.messages, "txt"),
                file_name=f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True
            )
        with col2:
            st.download_button(
                label="📋 JSON",
                data=export_chat_history(st.session_state.messages, "json"),
                file_name=f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )


# Ana alan - Sohbet
if not st.session_state.pdf_text:
    st.info("👈 Başlamak için sol taraftan bir PDF dosyası yükleyin")
elif not st.session_state.gemini_model:
    st.warning("⚠️ Model başlatılamadı. Lütfen Gemini API Key'inizi kontrol edip PDF'i tekrar işleyin.")
else:
    # Sohbet geçmişini göster
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Kullanıcı girişi
    if prompt := st.chat_input("PDF hakkında bir soru sorun..."):
        if not api_key:
            st.error("❌ Lütfen önce Gemini API Key girin!")
        else:
            # Kullanıcı mesajını ekle
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Asistan yanıtı
            with st.chat_message("assistant"):
                with st.spinner("Gemini düşünüyor..."):
                    try:
                        # Gemini'den yanıt al
                        response = get_gemini_response(
                            st.session_state.gemini_model,
                            prompt,
                            st.session_state.pdf_text,
                            st.session_state.messages[:-1]  # Son mesaj hariç
                        )
                        
                        st.markdown(response)
                        st.session_state.messages.append({"role": "assistant", "content": response})
                    
                    except Exception as e:
                        error_msg = f"❌ Hata oluştu: {str(e)}"
                        st.error(error_msg)
                        
                        # Hata türüne göre öneriler
                        error_str = str(e).lower()
                        if "api key" in error_str or "authentication" in error_str:
                            st.warning("💡 **Çözüm Önerisi:** API Key'iniz geçersiz olabilir. [Google AI Studio](https://aistudio.google.com/app/apikey) üzerinden yeni bir key alın.")
                        elif "quota" in error_str or "limit" in error_str:
                            st.warning("💡 **Çözüm Önerisi:** Günlük limitiniz dolmuş olabilir. Birkaç saat bekleyip tekrar deneyin.")
                        elif "safety" in error_str or "blocked" in error_str:
                            st.warning("💡 **Çözüm Önerisi:** Gemini güvenlik filtresi içeriği engelledi. Sorunuzu farklı şekilde ifade edin.")
                        
                        st.session_state.messages.append({"role": "assistant", "content": error_msg})


# Footer
st.divider()
st.markdown(
    """
    <div style='text-align: center; color: gray; font-size: 0.8em;'>
    📄 PDF Belge Asistanı | Powered by Google Gemini<br>
    <small>Ücretsiz Gemini API ile çalışır • <a href="https://aistudio.google.com/app/apikey" target="_blank">API Key Al</a></small>
    </div>
    """,
    unsafe_allow_html=True
)