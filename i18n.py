"""
Simple i18n module for the PDF assistant.
Contains translations and a helper to get a formatted translation string.
"""

translations = {
    "tr": {
        "title": "📄 PDF Belge Asistanı",
        "description": "PDF dosyanızı yükleyin ve içeriği hakkında sorular sorun! *(Google Gemini ile çalışır)*",
        "settings": "⚙️ Ayarlar",
        "language_label": "Dil / Language",
        "api_key_input": "Google Gemini API Key",
        "api_key_help": "API key'inizi .env dosyasına veya buraya girebilirsiniz",
        "api_key_loaded": "✅ Gemini API Key yüklendi",
        "api_key_missing": "⚠️ Lütfen Gemini API Key girin",
        "model_selection": "Model",
        "selected_model_info": "ℹ️ Seçili: **{model}**",
        "optimization_notes": "⚡ Optimizasyon Notları",
        "optimization_content": "**Token Tasarrufu İçin Yapılanlar:**\n- ✅ Akıllı metin parçalama (chunking)\n- ✅ Soruyla ilgili kısımlar aranıyor\n- ✅ Sadece son 2 sohbet turunu gönderme\n- ✅ 2 saniye rate limiting\n- ✅ Kısaltılmış prompt formatı\n- ✅ Maksimum 3500 karakter context\n\n**Öneriler:**\n- Kısa ve net sorular sorun\n- gemini-1.5-flash-8b modelini kullanın\n- Çok uzun PDF'ler için soruları spesifik yapın",
        "how_to_get_key": "🔑 Gemini API Key nasıl alınır?",
        "how_to_get_key_steps": "**Gemini API Key Alma Adımları:**\n1. Google AI Studio sayfasına gidin\n2. Google hesabınızla giriş yapın\n3. API Key oluşturun ve kopyalayın\n4. `.env` dosyasına `GEMINI_API_KEY=your_key_here` ekleyin",
        "upload_pdf": "PDF Dosyası Seçin",
        "upload_help": "Maksimum 10MB boyutunda PDF yükleyebilirsiniz",
        "file_too_large": "❌ Dosya boyutu 10MB'dan büyük olamaz!",
        "file_size_info": "📊 Dosya boyutu: {size} MB",
        "process_pdf": "📖 PDF'i İşle",
        "document_info": "📋 Belge Bilgileri",
        "file_label": "Dosya:",
        "pages_label": "Sayfa Sayısı:",
        "word_count": "Kelime Sayısı:",
        "chunks_label": "Metin Parçaları:",
        "estimated_tokens": "Tahmini Token:",
        "preview_label": "👁️ Metin Önizleme",
        "first_500_chars": "İlk 500 karakter",
        "chat_control": "💬 Sohbet Kontrolü",
        "chat_count_info": "📊 {count} mesaj",
        "clear_chat": "🗑️ Sohbeti Temizle",
        "download_txt": "📄 TXT",
        "download_json": "📋 JSON",
        "start_hint": "👈 Başlamak için sol taraftan bir PDF dosyası yükleyin",
        "model_not_started": "⚠️ Model başlatılamadı. Lütfen Gemini API Key'inizi kontrol edip PDF'i tekrar işleyin.",
        "chat_placeholder": "PDF hakkında bir soru sorun...",
        "gemini_thinking": "Gemini düşünüyor...",
        "error_prefix": "❌ Hata oluştu:",
        "quota_suggestions": "Quota aşıldı — lütfen bekleyin veya daha az token kullanan modeli deneyin.",
        "invalid_key_suggestion": "API Key'iniz geçersiz olabilir. Yeni bir key alın.",
        "safety_blocked": "Gemini güvenlik filtresi içeriği engelledi. Sorunuzu farklı şekilde ifade edin.",
        "model_not_found": "Model bulunamadı. gemini-1.5-flash-8b modelini deneyin.",
        "footer_html": "<div style='text-align: center; color: gray; font-size: 0.8em; margin-top: 10px;'>📄 PDF Belge Asistanı v2.1 (Optimize Edilmiş) | Powered by Google Gemini<br><small>Token tasarrufu için optimize edildi • <a href=\"https://aistudio.google.com/app/apikey\" target=\"_blank\">API Key Al</a></small></div>"
    },
    "en": {
        "title": "📄 PDF Document Assistant",
        "description": "Upload a PDF and ask questions about its content! *(Works with Google Gemini)*",
        "settings": "⚙️ Settings",
        "language_label": "Dil / Language",
        "api_key_input": "Google Gemini API Key",
        "api_key_help": "You can put your API key in the .env file or enter it here",
        "api_key_loaded": "✅ Gemini API Key loaded",
        "api_key_missing": "⚠️ Please enter your Gemini API Key",
        "model_selection": "Model",
        "selected_model_info": "ℹ️ Selected: **{model}**",
        "optimization_notes": "⚡ Optimization Notes",
        "optimization_content": "**Token saving techniques used:**\n- ✅ Smart text chunking\n- ✅ Searching for relevant parts\n- ✅ Sending only last 2 chat turns\n- ✅ 2s rate limiting\n- ✅ Shortened prompt format\n- ✅ Max 3500 character context\n\n**Suggestions:**\n- Ask short, clear questions\n- Use gemini-1.5-flash-8b for lower tokens\n- Make questions specific for very long PDFs",
        "how_to_get_key": "🔑 How to get Gemini API Key",
        "how_to_get_key_steps": "**How to get an API key:**\n1. Go to Google AI Studio\n2. Sign in with Google account\n3. Create/Get API key and copy it\n4. Add `GEMINI_API_KEY=your_key_here` to your `.env`",
        "upload_pdf": "Select PDF File",
        "upload_help": "You can upload PDFs up to 10MB",
        "file_too_large": "❌ File size cannot exceed 10MB!",
        "file_size_info": "📊 File size: {size} MB",
        "process_pdf": "📖 Process PDF",
        "document_info": "📋 Document Info",
        "file_label": "File:",
        "pages_label": "Pages:",
        "word_count": "Word Count:",
        "chunks_label": "Text Chunks:",
        "estimated_tokens": "Estimated Tokens:",
        "preview_label": "👁️ Text Preview",
        "first_500_chars": "First 500 characters",
        "chat_control": "💬 Chat Controls",
        "chat_count_info": "📊 {count} messages",
        "clear_chat": "🗑️ Clear Chat",
        "download_txt": "📄 TXT",
        "download_json": "📋 JSON",
        "start_hint": "👈 Upload a PDF from the left to get started",
        "model_not_started": "⚠️ Model could not be started. Check your Gemini API Key and reprocess the PDF.",
        "chat_placeholder": "Ask a question about the PDF...",
        "gemini_thinking": "Gemini is thinking...",
        "error_prefix": "❌ Error:",
        "quota_suggestions": "Quota exceeded — please wait or try a lower-token model.",
        "invalid_key_suggestion": "Your API key may be invalid. Create a new key.",
        "safety_blocked": "Gemini safety filter blocked the content. Rephrase your question.",
        "model_not_found": "Model not found. Try gemini-1.5-flash-8b.",
        "footer_html": "<div style='text-align: center; color: gray; font-size: 0.8em; margin-top: 10px;'>📄 PDF Document Assistant v2.1 (Optimized) | Powered by Google Gemini<br><small>Optimized for token savings • <a href=\"https://aistudio.google.com/app/apikey\" target=\"_blank\">Get API Key</a></small></div>"
    }
}


def get_translation(lang, key, **kwargs):
    # Fallback to 'tr' then to key
    txt = translations.get(lang, {}).get(key)
    if txt is None:
        txt = translations.get('tr', {}).get(key, key)
    try:
        return txt.format(**kwargs)
    except Exception:
        return txt

__all__ = ["translations", "get_translation"]
