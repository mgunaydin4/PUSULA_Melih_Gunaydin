# Pusula Talent Academy Documentation - Melih Günaydın

Bu proje, Talent Academy Case 2025 veri seti için kapsamlı bir veri ön işleme ve özellik mühendisliği pipeline’ı sağlar. 
Kod, veri temizleme, eksik değer impute etme, kategorik ve numerik değişken analizi, TF-IDF feature oluşturma ve hasta bazlı özet veri üretimi adımlarını içerir ve
modelleme için hazır hale getirir.

## Veri Yükleme
- Verilen excel dosyasından veriler yüklendi.
- Yüklenen veri df isimli bir değişkene atandı.

## String - Integer Dönüşümü
- TedaviSuresi ve UygulamaSuresi sütunlarından "Seans" ve "Dakika" gibi birimler temizlenip integer’a çevrildi.
- Hasta numarası kategorik olarak tanımlandı.

## Veri Setinin İncelenmesi
- Veri seti 2235 satır ve 13 sütundan oluşmaktadır.
- Toplamda 2706 eksik değer bulunmaktadır.
- Duplicate olan kayıt sayısı 928'dir.
- Summary_dataframe fonksiyonu ile;
  - Veri setinin ilk/son 5 yada girilen parametre kadar satırını gösterir.
  - Sütun isimleri, veri tipleri, özet istatistikler, veri setinin boyutu, eksik değerler, duplicate olan veri sayısı bilgileri öğrenilir.
- Categorical_variable_summary fonksiyonu ile;
  - Kategorik değişkenlerin frekansları ve veri seti içerisindeki yüzdelik değerleri öğrenilir. 
  - Plot_categorical = True parametresi ile kategorik değişkenlerin bar plotları çizdirilir.
- Numerical_variable_summary fonksiyonu ile;
    - Numerik değişkenlerin özet istatistikleri öğrenilir.
    - Seçilen nümerik değişkenin bilgileri gösterilir.
    - Plot_numerical = True parametresi ile numerik değişkenlerin histogramları çizdirilir.
    - Korelasyon matrisi(Heatmap) çizdirilir.
- Feature_visualization fonksiyonu ile;
    - Seçilen değişken kategorik ise bar plot ve pie chart, numerik ise histogram ve box plot çizdirilir.
- Y-Data Profiling ile hızlı veri analizi yapılabilir. Gözden kaçan detaylar bu rapor ile ortaya çıkabilir.

## Veri Ön İşleme
- Tüm string ifadeler küçük harfe çevrildi çünkü analiz bölümünde aynı kelimenin farklı yazımları tespit edildi 
(örn: Polen, polen, POLEN). 
- **deneme, onur, xx** gibi gürültülü veriler temizlendi.
- Tanilar değişkenindeki analizler sonucu "," kullanımı standart hale getirildi ve boşluklar kaldırıldı.
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
  - olarak dolduruldu. Veride yanlılık yaratmamak ve veri setinin örüntüsü korunması amaçlandı.
- Regulation_tanilar_first_per_hasta fonksiyonu ile;
  - rapidfuzz kütüphanesi kullanılarak benzerlik oranı %70 ve üzeri olan Tanilar standardize edildi.
- Veri analiz edilirken Alerji değişkenindeki yazım yanlışları tespit edilerek aynı standarda getirildi.

## Feature Engineering
- Hasta bazında unique KronikHastalikları veri setine eklendi. (KronikHastaliklar_Total)
- Hasta bazında unique Alerjileri veri setine eklendi. (Alerjiler_Total)
- Hasta bazında unique Tanıları veri setine eklendi. (Tanilar_Total)
- Hasta bazında UygulamaYerleri unique olarak veri setine eklendi. (UygulamaYerleri_Total)
- Hasta bazında TedaviAdi unique olarak veri setine eklendi.Yani hasta kaç farklı tedavi görmüş. (TedaviAdi_Count)
- Hasta bazında Bolum unique olarak veri setine eklendi. Yani hasta kaç farklı bölüme gitmiş. (Bolum_Total)
- Hasta kaç kere görüşme yapmış. (HASTA_SEESION_COUNT)
- Hastaya uygulanan uygulama süresi ortalaması. (AVERAGE_UYGULAMA_SURESI_DURATION)
- Hastaya kaç tane tanı konulmuş. (TANI_COUNT)
- Hastaya kaç farklı uygulama yeri yapılmış. (UYGULAMA_YERI_COUNT)
- YAS_BIN değişkeni istatistiksel yöntem olan IQR yöntemi ile oluşturuldu.
  - 0-11 
  - 12-38 
  - 39-47 
  - 48-56 
  - 56+
- Kronik hastalıkların sayısını ifade eden KRONIK_HASTALIK_COUNT değişkeni oluşturuldu. Eğer kişinin kronik hastalığı yok ise 0 var ise kaç tane ise o sayı yazıldı.
- Alerjilerin sayısını ifade eden ALERJI_COUNT değişkeni oluşturuldu. Eğer kişinin alerjisi yok ise 0, var ise kaç tane ise o sayı yazıldı.

## KNN Imputer ile Eksik Değer Doldurma
Veri setinde diğer eksik değerler ile veri kaybı yaşamadan dolduruldu. Bolum değişkenini veride yanlılık yaratmamak ve verinin
örüntüsünü korumak için **KNN Imputer** yöntemi ile dolduruldu.

## Gereksiz Değişkenlerin Çıkarılması
- KronikHastalik, Alerji, Tanilar, UygulamaYerleri, KronikHastalik_Total, Alerji_Total değişkenleri model için hazırlanan 
veride gereksiz olduğu için çıkarıldı.

## One-Hot Encoding
- Cinsiyet, KanGrubu, Uyruk, Bolum ve YAS_BIN değişkenleri `nominal` değişkenler olduğu için, yani değişkendeki değerler
arasında bir alt-üst, büyüklük küçüklük gibi bir ayrım olmadığı için **one-hot encoding** uygulandı. 
**Çoklu bağlantı sorunu yaşanmaması için drop_first=True** parametresi kullanıldı.

## Modele Hazırlık
- HastaNo bazlı model kurulacağı için değerler tekilleştirildi.
- Tanilar, UygulamaYerleri ve TedaviAdi değişkenlerine **TF-IDF** uygulanarak yeni özellikler oluşturuldu. TF-IDF kullanılmasının 
sebebi ise metin verilerinden anlamlı özellikler çıkarabilmek amaçlanmıştır.
- Son olarak df_final isimli değişken modele hazır hale getirildi.

## STREAMLIT WEB UYGULAMASI VE CHATBOT
- Streamlit ile web uygulaması oluşturuldu.Veri seti hakkında bilgi alabilmek için 
`create_pandas_dataframe_agent` ile **llm tabanlı bir soru-cevap chatbotu** geliştirildi.
