name: Update Playlist

on:
  schedule:
    - cron: '0 */2 * * *'  # Her 2 saatte bir çalışır
  workflow_dispatch:        # Manuel tetikleme desteği

jobs:
  update:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install requests beautifulsoup4

      - name: Run scraper
        run: python scraper.py

      - name: Commit and push changes
        env:
          PAT_TOKEN: ${{ secrets.PAT_TOKEN }}
        run: |
          git config --global user.name "seyityavuz"
          git config --global user.email "youremail@example.com"
          git remote set-url origin https://x-access-token:${PAT_TOKEN}@github.com/${{ github.repository }}

          if [[ -f "playlist.m3u8" ]]; then
            git add playlist.m3u8
            if ! git diff --cached --quiet; then
              git commit -m "Auto-update playlist"
              git push origin HEAD:main
              echo "✅ Playlist güncellendi ve push edildi."
            else
              echo "ℹ️ Değişiklik yok, commit atlanıyor."
            fi
          else
            echo "⚠️ playlist.m3u8 dosyası bulunamadı, işlem iptal edildi."
            exit 1
          fi
