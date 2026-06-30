# Baret Kullanımı İzleme Sistemi

Kamera görüntüleri üzerinden iş yerinde baret (kask) kullanımını izlemeye yönelik bir bilgisayarlı görü projesidir. Sistem, çalışma alanlarından alınan görüntüleri analiz ederek kişisel koruyucu donanım (KKD) kullanımını otomatik olarak değerlendirir ve baret kullanımına ilişkin tespitleri kayıt altına alır.

Proje; iş yeri güvenliği uygulamalarında karar destek aracı olarak kullanılmak üzere tasarlanmış olup, Windows masaüstü ortamında çalıştırılabilen bir izleme çözümünün görü ve çıkarım bileşenlerini sağlar. Modelin çekirdeğinde [YOLOv8](https://docs.ultralytics.com/) nesne tespiti mimarisi yer alır; çıkarım hizmeti ise hafif bir [FastAPI](https://fastapi.tiangolo.com/) servisi aracılığıyla sunulur.

Model, iş yeri güvenliği açısından önem taşıyan beş sınıfı tanıyacak şekilde eğitilmiştir: `helmet` (baret var), `no-helmet` (baret yok), `no-vest` (yelek yok), `person` (kişi) ve `vest` (yelek var). Bu sınıflar sayesinde, baret veya yelek kullanmayan kişilere ilişkin uygunsuzluk durumları tespit edilerek uyarı kaydı oluşturulabilir.

## Özellikler

- **Görüntü tabanlı tespit hizmeti** — Yüklenen bir görüntü üzerinde çıkarım yapar; tespit edilen nesneleri sınıf etiketleri, güven skorları ve sınırlayıcı kutu koordinatları ile birlikte döndürür.
- **KKD odaklı sınıflandırma** — Baret ve yelek kullanan ya da kullanmayan kişileri birbirinden ayırt eder.
- **Uygunsuzluk tespiti** — Baret veya yelek bulunmayan durumları belirleyerek uyarı kaydı oluşturmaya elverişli çıktılar üretir.
- **Yeniden üretilebilir eğitim** — Hiperparametreleri yapılandırılabilen, YOLOv8 tabanlı bir eğitim betiği içerir.
- **Veri kümesi indirme yardımcısı** — Eğitimde kullanılan veri kümesi dışa aktarımını indiren bir betik sunar.
- **Sade ve bağımlılık odaklı kurulum** — Tüm gereksinimler `requirements.txt` dosyasında belirtilmiştir.

## Teknoloji Yığını

- **Programlama dili:** Python 3
- **Model / Bilgisayarlı görü:** Ultralytics YOLOv8, OpenCV, NumPy
- **Derin öğrenme altyapısı:** PyTorch, TorchVision
- **API:** FastAPI, Uvicorn, python-multipart
- **Veri kümesi araçları:** Roboflow

## Klasör Yapısı

```
.
├── main.py               # /detect uç noktasını sunan FastAPI uygulaması
├── train.py              # Veri kümesi üzerinde YOLOv8 modelini eğitir
├── download_dataset.py   # Veri kümesi dışa aktarımını indirir (YOLOv8 biçimi)
├── data.yaml             # Veri kümesi yapılandırması: yollar ve sınıf adları
├── requirements.txt      # Python bağımlılıkları
├── .gitignore
└── README.md
```

Üretilen veya indirilen dosyalar (sürüm denetimine dâhil edilmez):

- `best.pt` — API tarafından yüklenen, eğitilmiş model ağırlıkları.
- `construction-safety-2/` — Eğitimde kullanılan veri kümesi dışa aktarımı.
- `runs/` — Eğitim çıktıları ve başarım metrikleri.

## Kurulum

1. Depoyu klonlayın:

```bash
git clone <depo-adresi>
cd <depo-dizini>
```

2. Bir sanal ortam oluşturup etkinleştirin:

```bash
python -m venv .venv
.venv\Scripts\activate        # Linux/macOS için: source .venv/bin/activate
```

3. Bağımlılıkları yükleyin:

```bash
pip install -r requirements.txt
```

## Ortam Değişkenleri

Proje, yapılandırma bilgilerini ortam değişkenlerinden okur. Bir `.env` dosyası oluşturarak (veya değişkenleri kabuk ortamında tanımlayarak) aşağıdaki gibi yalnızca placeholder (yer tutucu) değerler kullanın:

```env
# Veri kümesi sağlayıcısına ait API anahtarı (download_dataset.py tarafından kullanılır)
ROBOFLOW_API_KEY=<roboflow-api-anahtariniz>
```

> Gerçek kimlik bilgilerini hiçbir zaman depoya eklemeyin. Dokümantasyonda yalnızca yer tutucu değerler kullanın ve gerçek `.env` dosyanızı sürüm denetiminin dışında tutun.

## Çalıştırma

### 1. Veri kümesini indirme (eğitim için, isteğe bağlı)

```bash
python download_dataset.py
```

Bu betik, veri kümesini YOLOv8 biçiminde indirir. Oluşan klasörün `data.yaml` dosyasındaki `path` ayarıyla uyumlu olduğundan emin olun.

### 2. Modeli eğitme (isteğe bağlı)

```bash
python train.py
```

Eğitim sonucunda model ağırlıkları `runs/` dizini altında üretilir. API'nin ağırlıkları yükleyebilmesi için elde edilen en iyi ağırlık dosyasını proje kök dizinine `best.pt` adıyla kopyalayın veya yeniden adlandırın.

### 3. API sunucusunu çalıştırma

Proje kök dizininde `best.pt` dosyasının bulunduğundan emin olduktan sonra sunucuyu başlatın:

```bash
uvicorn main:app --reload
```

API, `http://127.0.0.1:8000` adresinde kullanılabilir hâle gelir. Etkileşimli API belgelerine `http://127.0.0.1:8000/docs` adresinden erişebilirsiniz.

## Kullanım

Bir görüntü üzerinde tespit yapmak için görüntüyü `/detect` uç noktasına yükleyin:

```bash
curl -X POST "http://127.0.0.1:8000/detect" \
  -F "file=@goruntu/yolu.jpg"
```

Örnek yanıt:

```json
[
  {
    "class": "helmet",
    "conf": 0.92,
    "box": [34, 58, 120, 140]
  }
]
```

Her tespit sonucu; belirlenen sınıfı (`class`), güven skorunu (`conf`) ve sınırlayıcı kutuyu (`box`) piksel koordinatları `[x1, y1, x2, y2]` biçiminde içerir. Baret kullanılmayan durumlara (`no-helmet`) ilişkin sonuçlar, iş yeri güvenliği takibi için uyarı kaydı oluşturmak amacıyla değerlendirilebilir.



