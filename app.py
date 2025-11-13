"""
PDF Belge Asistanı - Google Gemini Edition (Optimize Edilmiş)
Kullanıcıların PDF dosyası yükleyip sorular sorabileceği bir Streamlit uygulaması.
"""

import streamlit as st
from PyPDF2 import PdfReader
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json
from datetime import datetime
import time

# Ortam değişkenlerini yükle
load_dotenv()

# Sayfa yapılandırması
st.set_page_config(
    page_title="PDF Belge Asistanı",
    page_icon="📄",
    layout="wide"
)

from i18n import get_translation


def t(key, **kwargs):
    lang = st.session_state.get("selected_language", "tr")
    return get_translation(lang, key, **kwargs)


# Başlık ve açıklama (localize edilmiş)
st.title(t("title"))
st.markdown(t("description"))


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
            if page_text.strip():  # Boş sayfaları atla
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


def chunk_text(text, max_chars=3000):
    """
    Metni küçük parçalara böler (token tasarrufu için).
    
    Args:
        text: Bölünecek metin
        max_chars: Maksimum karakter sayısı
        
    Returns:
        list: Metin parçaları
    """
    chunks = []
    current_chunk = ""
    
    for line in text.split('\n'):
        if len(current_chunk) + len(line) < max_chars:
            current_chunk += line + '\n'
        else:
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = line + '\n'
    
    if current_chunk:
        chunks.append(current_chunk)
    
    return chunks


def search_relevant_chunks(chunks, query, top_k=2):
    """
    Soruyla ilgili en alakalı metin parçalarını bulur (basit keyword arama).
    
    Args:
        chunks: Metin parçaları listesi
        query: Kullanıcı sorusu
        top_k: Kaç parça döndürülecek
        
    Returns:
        str: Birleştirilmiş alakalı metin parçaları
    """
    query_words = set(query.lower().split())
    
    # Her chunk için skor hesapla
    scored_chunks = []
    for chunk in chunks:
        chunk_words = set(chunk.lower().split())
        score = len(query_words & chunk_words)  # Ortak kelime sayısı
        scored_chunks.append((score, chunk))
    
    # En yüksek skorlu parçaları al
    scored_chunks.sort(reverse=True, key=lambda x: x[0])
    relevant_chunks = [chunk for score, chunk in scored_chunks[:top_k] if score > 0]
    
    # Eğer hiç eşleşme yoksa ilk chunk'ı döndür
    if not relevant_chunks and chunks:
        relevant_chunks = [chunks[0]]
    
    return '\n\n'.join(relevant_chunks)


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
        # Model adına "models/" prefix'i ekle
        full_model_name = f"models/{model_name}" if not model_name.startswith("models/") else model_name
        
        # Optimized generation config
        generation_config = {
            "temperature": 0.7,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 2048,  # Çıkış token limiti
        }
        
        model = genai.GenerativeModel(
            full_model_name,
            generation_config=generation_config
        )
        return model
    except Exception as e:
        st.error(f"Model başlatılırken hata: {str(e)}")
        return None


def get_gemini_response(model, prompt, pdf_chunks, chat_history):
    """
    Gemini'den yanıt alır (Optimize Edilmiş - Daha Az Token).
    
    Args:
        model: Gemini model instance
        prompt: Kullanıcı sorusu
        pdf_chunks: PDF içeriği parçaları
        chat_history: Sohbet geçmişi
        
    Returns:
        str: Model yanıtı
    """
    try:
        # Soruyla ilgili en alakalı metinleri bul
        relevant_context = search_relevant_chunks(pdf_chunks, prompt, top_k=2)
        
        # Sadece son 2 sohbet turunu dahil et (token tasarrufu)
        recent_history = chat_history[-4:] if len(chat_history) > 4 else chat_history
        
        # Kısa chat history formatla
        history_text = ""
        if recent_history:
            for msg in recent_history:
                role = "K" if msg["role"] == "user" else "A"
                # Uzun mesajları kısalt
                content = msg['content'][:200] + "..." if len(msg['content']) > 200 else msg['content']
                history_text += f"{role}: {content}\n"
        
        # Kısaltılmış ve optimize edilmiş prompt
        system_prompt = """PDF belge asistanısın. Sadece verilen bilgilere göre yanıt ver.

İlgili Metin:
{context}

{history}
Soru: {question}

Yanıt:"""

        # Prompt'u hazırla
        full_prompt = system_prompt.format(
            context=relevant_context[:3500],  # Daha az token
            history=f"Önceki:\n{history_text}\n" if history_text else "",
            question=prompt
        )
        
        # Güvenlik ayarları
        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_ONLY_HIGH"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_ONLY_HIGH"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_ONLY_HIGH"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_ONLY_HIGH"}
        ]
        
        # Rate limiting - her istekten önce kısa bir bekleme
        if 'last_request_time' in st.session_state:
            elapsed = time.time() - st.session_state.last_request_time
            if elapsed < 2:  # 2 saniyeden kısa sürede istek atılmışsa bekle
                time.sleep(2 - elapsed)
        
        st.session_state.last_request_time = time.time()
        
        # Gemini'den yanıt al
        response = model.generate_content(
            full_prompt,
            safety_settings=safety_settings
        )
        
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

if "pdf_chunks" not in st.session_state:
    st.session_state.pdf_chunks = []

if "pdf_info" not in st.session_state:
    st.session_state.pdf_info = {}

if "gemini_model" not in st.session_state:
    st.session_state.gemini_model = None

if "last_request_time" not in st.session_state:
    st.session_state.last_request_time = 0


# Sidebar - Ayarlar ve Kontroller
with st.sidebar:
    st.header(t("settings"))

    # Dil seçimi
    lang_default = st.session_state.get("selected_language", "tr")
    lang_choice = st.selectbox(
        t("language_label"),
        options=[("tr", "Türkçe"), ("en", "English")],
        format_func=lambda x: x[1],
        index=0 if lang_default == "tr" else 1,
    )
    st.session_state.selected_language = lang_choice[0]

    # API Key kontrolü - GEMINI
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        api_key = st.text_input(
            t("api_key_input"),
            type="password",
            help=t("api_key_help")
        )

    if api_key:
        st.success(t("api_key_loaded"))
    else:
        st.warning(t("api_key_missing"))

    # Model seçimi - GÜNCEL GEMINI MODELLER
    st.subheader("🤖 " + t("model_selection"))

    # Güncel Gemini model kategorileri ve açıklamaları
    model_info = {
        "gemini-flash-latest": "💨 Ultra hafif - En az token (ÖNERİLEN)",
        "gemini-1.5-flash": "⚡ Hızlı ve dengeli",
        "gemini-2.0-flash-exp": "🚀 Yeni deneysel model",
        "gemini-1.5-pro": "💎 En güçlü (daha fazla token)"
    }

    selected_model = st.selectbox(
        t("model_selection"),
        list(model_info.keys()),
        index=0,
        format_func=lambda x: f"{x} - {model_info[x]}",
        help="Quota sorunu için gemini-1.5-flash-8b önerilir"
    )

    # Model bilgisi
    st.info(t("selected_model_info", model=selected_model))

    # Optimizasyon bilgisi
    with st.expander(t("optimization_notes")):
        st.markdown(t("optimization_content"))

    # API Key alma bilgisi
    with st.expander(t("how_to_get_key")):
        st.markdown(t("how_to_get_key_steps"))

    st.divider()

    # PDF yükleme
    st.subheader("📤 " + t("upload_pdf"))
    uploaded_file = st.file_uploader(
        t("upload_pdf"),
        type=["pdf"],
        help=t("upload_help")
    )

    # Dosya boyutu kontrolü
    if uploaded_file is not None:
        file_size_mb = uploaded_file.size / (1024 * 1024)

        if file_size_mb > 10:
            st.error(t("file_too_large"))
            uploaded_file = None
        else:
            st.info(t("file_size_info", size=f"{file_size_mb:.2f}"))

            # PDF işleme
            if st.button(t("process_pdf"), type="primary"):
                with st.spinner("PDF okunuyor..."):
                    text, page_count = extract_text_from_pdf(uploaded_file)

                    if text:
                        st.session_state.pdf_text = text

                        # Metni parçalara böl
                        with st.spinner("Metin parçalanıyor..."):
                            chunks = chunk_text(text, max_chars=3000)
                            st.session_state.pdf_chunks = chunks

                        st.session_state.pdf_info = {
                            "filename": uploaded_file.name,
                            "pages": page_count,
                            "stats": get_text_stats(text),
                            "chunks": len(chunks)
                        }

                        # Gemini modelini başlat
                        if api_key:
                            with st.spinner(f"{selected_model} başlatılıyor..."):
                                model = initialize_gemini(selected_model, api_key)
                                if model:
                                    st.session_state.gemini_model = model
                                    st.success(f"✅ PDF yüklendi! ({page_count} sayfa, {len(chunks)} parça)")
                                else:
                                    st.error("❌ Model başlatılamadı. API Key'inizi kontrol edin.")
                        else:
                            st.error(t("api_key_missing"))

                        if st.session_state.gemini_model:
                            st.rerun()

    # PDF bilgileri
    if st.session_state.pdf_text:
        st.divider()
        st.subheader(t("document_info"))
        st.write(f"**{t('file_label')}** {st.session_state.pdf_info['filename']}")
        st.write(f"**{t('pages_label')}** {st.session_state.pdf_info['pages']}")
        st.write(f"**{t('word_count')}** {st.session_state.pdf_info['stats']['words']:,}")
        st.write(f"**{t('chunks_label')}** {st.session_state.pdf_info['chunks']}")

        # Token tahmini
        estimated_tokens = st.session_state.pdf_info['stats']['characters'] // 4
        st.write(f"**{t('estimated_tokens')}** ~{estimated_tokens:,}")

        # PDF önizleme
        with st.expander(t("preview_label")):
            preview_text = st.session_state.pdf_text[:500] + "..."
            st.text_area(t('first_500_chars'), preview_text, height=150, disabled=True)

    # Sohbet kontrolü
    if st.session_state.messages:
        st.divider()
        st.subheader(t("chat_control"))

        st.info(t("chat_count_info", count=len(st.session_state.messages)))

        # Sohbeti temizle
        if st.button(t("clear_chat"), type="secondary"):
            st.session_state.messages = []
            st.rerun()

        # Sohbeti indir
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label=t("download_txt"),
                data=export_chat_history(st.session_state.messages, "txt"),
                file_name=f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True
            )
        with col2:
            st.download_button(
                label=t("download_json"),
                data=export_chat_history(st.session_state.messages, "json"),
                file_name=f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )


# Ana alan - Sohbet
if not st.session_state.pdf_text:
    st.info(t("start_hint"))
elif not st.session_state.gemini_model:
    st.warning(t("model_not_started"))
else:
    # Sohbet geçmişini göster
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Kullanıcı girişi
    if prompt := st.chat_input(t("chat_placeholder")):
        if not api_key:
            st.error(t("api_key_missing"))
        else:
            # Kullanıcı mesajını ekle
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Asistan yanıtı
            with st.chat_message("assistant"):
                with st.spinner(t("gemini_thinking")):
                    try:
                        # Gemini'den yanıt al
                        response = get_gemini_response(
                            st.session_state.gemini_model,
                            prompt,
                            st.session_state.pdf_chunks,
                            st.session_state.messages[:-1]  # Son mesaj hariç
                        )
                        
                        st.markdown(response)
                        st.session_state.messages.append({"role": "assistant", "content": response})
                    
                    except Exception as e:
                        error_msg = f"{t('error_prefix')} {str(e)}"
                        st.error(error_msg)

                        # Hata türüne göre öneriler (kısaltılmış, lokalize)
                        error_str = str(e).lower()
                        if "429" in error_str or "quota" in error_str or "limit" in error_str:
                            st.warning(t('quota_suggestions'))
                        elif "api key" in error_str or "authentication" in error_str or "401" in error_str:
                            st.warning(t('invalid_key_suggestion'))
                        elif "safety" in error_str or "blocked" in error_str:
                            st.warning(t('safety_blocked'))
                        elif "404" in error_str or "not found" in error_str:
                            st.warning(t('model_not_found'))

                        st.session_state.messages.append({"role": "assistant", "content": error_msg})


# Footer
st.divider()
col1, col2, col3 = st.columns(3)
with col1:
    if st.session_state.pdf_chunks:
        st.metric("Metin Parçaları", len(st.session_state.pdf_chunks))
with col2:
    if st.session_state.messages:
        st.metric("Sohbet Mesajları", len(st.session_state.messages))
with col3:
    st.metric("Aktif Model", selected_model.split('-')[1] if '-' in selected_model else selected_model)

st.markdown(t('footer_html'), unsafe_allow_html=True)