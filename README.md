# Canlı TV M3U8 Playlist Otomasyonu

Bu proje, [canlitv.me/live](https://www.canlitv.me/live) adresinden yayınları otomatik olarak çekip `playlist.m3u8` dosyası oluşturan bir sistemdir. GitHub Actions ile her 2 saatte bir güncellenir.

## Özellikler

- Yayın sayfalarını otomatik tarar
- iframe içinden M3U8 linklerini çıkarır
- Geçerli yayınları `playlist.m3u8` dosyasına yazar
- Git değişikliği varsa otomatik commit + push yapar

## Kullanım

1. Reponuzu klonlayın
2. `scraper.py` dosyasını çalıştırarak manuel test edin
3. GitHub Actions aktifse otomatik çalışır

## Edge-Case Dayanıklılığı

- iframe olmayan sayfalar atlanır
- M3U8 bulunamazsa kanal eklenmez
- Gereksiz commit engellenir (`git diff --cached --quiet`)

## Katkı

Yeni kaynaklar, kanal filtreleme veya loglama iyileştirmeleri için PR gönderebilirsiniz.
