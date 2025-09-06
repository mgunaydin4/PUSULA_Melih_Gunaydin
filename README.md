# PUSULA_Melih_Gunaydin - melihhgunaydinn@gmail.com

## PUSULA TALENT ACADEMY CASE - Melih Günaydın

## Proje Hakkında Genel Bakış
Bu proje, kapsamlı bir **Keşifsel Veri Analizi (EDA)** ve **Veri Ön İşleme** sürecini içeren bir case çalışmasıdır. 
Projenin ana amacı, `Talent_Academy_Case_DT_2025.xlsx` adlı veri setini incelemek, eksik ve hatalı verileri gidermek, 
kategorik ve sayısal değişkenleri analiz etmek ve veriyi modelleme için hazır hale getirmektir.


## Veri Ön İşleme ve Analiz Adımları
Proje, veri setinin temizlenmesi ve analizi için bir dizi adımdan oluşmaktadır:
1.  **Veri Yükleme**: Çalışma, `../data/` klasöründe bulunan `Talent_Academy_Case_DT_2025.xlsx` adlı Excel dosyasını okuyarak başlar.
2.  **Veri Dönüştürme**: `TedaviSuresi` ve `UygulamaSuresi` gibi bazı sütunlardaki metinsel ifadeler kaldırılıp, veri tipleri tam sayıya dönüştürülmüştür.
3.  **Veri Özetleme**: Veri setinin ilk ve son gözlemleri, sütun adları, veri tipleri, özet istatistikleri ve eksik/yinelenen değerler gibi temel bilgileri sunan özel fonksiyonlar kullanılarak incelenmiştir.
4.  **Veri Profilleme**: `ydata_profiling` kütüphanesi ile veri setinin ayrıntılı bir profili oluşturulmuştur.
5.  **Metin Verilerini Temizleme**: Sütunlardaki tüm metin verileri küçük harfe dönüştürülmüştür. Ayrıca, gürültülü veriler tespit edilip **(örneğin: "deneme", "onur", "xx")** kaldırılmıştır. `Tanilar` sütunundaki fazla virgül ve boşluklar temizlenmiştir.
6.  **Eksik Değerlerin Doldurulması**:
   - İlk olarak NaN değerlere şu şekilde müdahale edildi:
      - Bir hastaya ait KanGrubu eğer bir satırda biliniyor ise diğer satırlarda da o şekilde kabul edildi çünkü bir hastanın kan grubu değişmez.
      - Aynı şekilde Cinsiyet, KronikHastalik ve Alerji değişkenleri için de aynı mantık uygulandı. Hastanın Cinsiyeti değişmez. 
Kronik hastalığı artabilir ya da yeni bir Alerjisi olabilir ancak bu mantık ile mevcut korundu.
   - Daha sonra ise 
       - Cinsiyet değişkenindeki NaN değerler "Bilinmiyor"
       - KronikHastalik değişkenindeki NaN değerler "yok"
       - Tanilar değişkenindeki NaN değerler "bilinmiyor"
       - KanGrubu değişkenindeki NaN değerler "bilinmiyor"
       - UygulamaYerleri değişkenindeki NaN değerler "bilinmiyor"
        olarak dolduruldu. Veride yanlılık yaratmamak ve veri setinin örüntüsü korunması amaçlandı.
7.  **Benzer Değerleri Gruplama**: `Tanilar` sütunundaki benzer veriler, `rapidfuzz` kütüphanesi ile ve 
`Tanilar`,`UygulamaYerleri`,`TedaviAdi` değişkenlerine TF-IDF vektörleştirme yöntemi kullanılmıştır.

## STREAMLIT WEB UYGULAMASI VE CHATBOT
- Streamlit ile web uygulaması oluşturuldu. create_pandas_dataframe_agent ile **llm tabanlı bir soru-cevap chatbotu** geliştirildi.
<img width="1335" height="763" alt="Screenshot 2025-09-06 at 17 23 33" src="https://github.com/user-attachments/assets/7a25f2d9-c0be-4e83-bef2-e8f986c42278" />
<img width="1343" height="777" alt="Screenshot 2025-09-06 at 17 24 29" src="https://github.com/user-attachments/assets/c3810dc0-529c-4dd1-af44-c47305ef6153" />
<img width="1335" height="686" alt="Screenshot 2025-09-06 at 17 27 00" src="https://github.com/user-attachments/assets/91439c6f-f684-44c2-b7ae-e54dc6d4547e" />

## Neler Yapılabilir ?
- TF-IDF `max_features` parametresi **optimize** edilebilir.
- Model denemeleri yapılabilir örnek olarak;
    - `Pycaret`, `Flaml`, `Autgluon`, gibi otomatik makine öğrenimi kütüphaneleri kullanılabilir.
- Kurulan model sonrası `feature selection` yapılabilir.
- Data collection ile veri seti genişletilebilir.
- Encoder model denemeleri yapılabilir. (örn: Hugging face turkish-bert)


**DAHA DETAYLI BİLGİLER `Documentation.md` DOSYASINDA BULUNMAKTADIR.**

