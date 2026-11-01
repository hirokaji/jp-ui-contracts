# examples

初めて試す場合は[overflow-walkthrough](overflow-walkthrough/README.md)から始めてください。
同じ画面の不具合を検出し、修正後を再検査できます。[導入手順](../docs/getting-started.md)で自分のアプリへの適用まで説明しています。

以下は設計例です。固定fixtureのCI成功を、これらの画面や導入先の適合証明として扱わないでください。

- `sample-media/`
  - 記事メディア向けの例
  - 長文、mixed-script 見出し、URL、caption を確認しやすい
- `sample-saas/`
  - SaaS / 管理画面向けの例
  - フォーム、表、ラベル、mixed navigation を確認しやすい

`preview.html` はそのままブラウザで開けます。  
相対パスのCSSを安定して読み込みたい場合は、リポジトリのルートで簡易サーバーを立ててください。

```bash
python -m http.server 8000
```
