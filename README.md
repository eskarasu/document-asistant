# 📄 PDF Belge Asistanı

PDF dosyalarınızı yükleyip, içeriği hakkında sorular sorabileceğiniz akıllı bir asistan uygulaması.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31-red.svg)
![LangChain](https://img.shields.io/badge/LangChain-0.1-green.svg)

## 🌟 Özellikler

### Temel Özellikler
- ✅ **PDF Yükleme**: Sadece PDF dosyalarını kabul eder (max 10MB)
- ✅ **Metin Çıkarma**: PyPDF2 ile güvenilir metin çıkarma
- ✅ **Soru-Cevap Sistemi**: OpenAI ile akıllı yanıtlar
- ✅ **Konuşma Geçmişi**: Bağlam korunarak devam eden sohbet
- ✅ **Modern Arayüz**: Chat benzeri kullanıcı dostu tasarım

### Ek Özellikler
- 🎯 **Model Seçimi**: GPT-4o-mini, GPT-4o, GPT-3.5-turbo arası seçim
- 📊 **Metin İstatistikleri**: Sayfa, kelime ve karakter sayısı
- 👁️ **PDF Önizleme**: Metnin ilk kısmını görüntüleme
- 🗑️ **Sohbet Temizleme**: Konuşma geçmişini tek tıkla silme
- 💾 **Geçmiş İndirme**: TXT veya JSON formatında dışa aktarma

## 📋 Gereksinimler

```bash
Python 3.8 veya üzeri
OpenAI API Key
```

## 🚀 Kurulum

### 1. Repository'yi Klonlayın

```bash
git clone https://github.com/eskarasu/document-asistant.git
cd belge-asistani
```

### 2. Sanal Ortam Oluşturun (Önerilir)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Gerekli Paketleri Yükleyin

```bash
pip install -r requirements.txt
```

### 4. API Key Yapılandırması

`.env` dosyası oluşturun:

```bash
cp .env.example .env
```

`.env` dosyasını düzenleyip API key'inizi ekleyin:

```
OPENAI_API_KEY=your_actual_api_key_here
```

**API Key Nasıl Alınır?**
1. [OpenAI Platform](https://platform.openai.com/) adresine gidin
2. Hesap oluşturun veya giriş yapın
3. API Keys bölümünden yeni bir key oluşturun

## 💻 Kullanım

Uygulamayı başlatın:

```bash
streamlit run app.py
```

Tarayıcınızda otomatik olarak `http://localhost:8501` açılacaktır.

### Adım Adım Kullanım

1. **PDF Yükleme**
   - Sol sidebar'dan "PDF Dosyası Seçin" butonuna tıklayın
   - PDF dosyanızı seçin (max 10MB)
   - "📖 PDF'i İşle" butonuna tıklayın

2. **Soru Sorma**
   - Alt kısımdaki chat kutusuna sorunuzu yazın
   - Enter'a basın veya gönder butonuna tıklayın
   - Asistan PDF içeriğine göre yanıt verecektir

3. **Sohbet Yönetimi**
   - Geçmişi görmek için yukarı kaydırın
   - "🗑️ Sohbeti Temizle" ile yeni başlayın
   - "💾 İndir" butonları ile geçmişi kaydedin

## 📸 Ekran Görüntüleri

### Ana Arayüz
![Ana Arayüz](screenshots/main-interface.png)
*PDF yükleme ve sohbet arayüzü*

### Sohbet Örneği
![Sohbet](screenshots/chat-example.png)
*Asistan ile etkileşim*

## 🏗️ Proje Yapısı

```
belge-asistani/
├── app.py                 # Ana uygulama kodu
├── requirements.txt       # Python bağımlılıkları
├── .env.example          # API key şablonu
├── .gitignore            # Git ignore kuralları
├── README.md             # Bu dosya
└── screenshots/          # Ekran görüntüleri (opsiyonel)
```

## 🔧 Teknik Detaylar

### Kullanılan Teknolojiler

- **Streamlit**: Web arayüzü
- **LangChain**: LLM orkestrasyon framework'ü
- **OpenAI API**: Dil modeli (GPT-4o-mini, GPT-4o, GPT-3.5-turbo)
- **PyPDF2**: PDF metin çıkarma
- **Python-dotenv**: Ortam değişkeni yönetimi

### Kod Özellikleri

- ✨ Clean Code prensipleri
- 📝 Detaylı docstring'ler
- 🛡️ Kapsamlı hata yönetimi
- 🔄 Session state ile durum yönetimi
- 🎨 Modüler fonksiyon yapısı

## 🎓 Öğrenme Noktaları

Bu projede şunları öğreneceksiniz:

1. **Streamlit Temel ve İleri Seviye**
   - File uploader kullanımı
   - Session state yönetimi
   - Chat interface oluşturma
   - Sidebar ve layout düzenleme

2. **PDF İşleme**
   - PyPDF2 ile metin çıkarma
   - Dosya boyutu kontrolü
   - Hata yönetimi

3. **LangChain & LLM**
   - ConversationChain oluşturma
   - Memory yönetimi
   - Prompt engineering
   - OpenAI API entegrasyonu

4. **Python Best Practices**
   - Modüler kod yazımı
   - Docstring kullanımı
   - Ortam değişkeni güvenliği

## ⚠️ Önemli Notlar

- **API Maliyeti**: OpenAI API kullanımı ücretlidir. Token kullanımınızı takip edin.
- **Dosya Boyutu**: Büyük PDF'ler token limitini aşabilir. 10MB limiti önerilir.
- **Güvenlik**: `.env` dosyasını asla GitHub'a yüklemeyin!
- **Model Seçimi**: GPT-4o daha iyi sonuçlar verir ancak daha pahalıdır.

## 🐛 Sorun Giderme

### "OpenAI API Key not found" Hatası
- `.env` dosyasının proje kök dizininde olduğundan emin olun
- API key'in doğru kopyalandığını kontrol edin
- Uygulamayı yeniden başlatın

### "PDF okunamadı" Hatası
- PDF'in bozuk olmadığından emin olun
- Şifrelenmiş PDF'lerde sorun çıkabilir
- Başka bir PDF ile deneyin

### Yavaş Yanıtlar
- Daha küçük bir model seçin (gpt-3.5-turbo)
- PDF boyutunu küçültün
- İnternet bağlantınızı kontrol edin

## 🤝 Katkıda Bulunma

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit edin (`git commit -m 'Add amazing feature'`)
4. Push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 👤 İletişim

Proje Sahibi - [@eskarasu](https://github.com/eskarasu)

Proje Linki: [https://github.com/eskarasu/belge-asistani](https://github.com/eskarasu/belge-asistani)

---

⭐ Bu projeyi beğendiyseniz yıldız vermeyi unutmayın!