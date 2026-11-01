# 長い日本語ラベルの横はみ出し

導入手順用に作成した合成例です。実際の利用者から報告された障害や、AI生成の成功率比較ではありません。既存のv0.2.0必須fixtureとは別の、検査器の検出力を確かめる回帰例です。

## 同じ画面を比べる

- `before.html`：折り返しを禁止したボタンと、折り返さない横並び
- `after.html`：同じ内容・文字サイズで、ボタンとその配置の折り返しを許可
- `styles.css`：共通CSSと、`.after`にだけ適用する修正

リポジトリのルートで`python -m http.server 8000 --bind 127.0.0.1`を実行し、ブラウザで`http://127.0.0.1:8000/examples/overflow-walkthrough/before.html`と`after.html`を開きます。

## 検出と修正

別ターミナルでもリポジトリのルートへ移動します。初回セットアップは[導入手順](../../docs/getting-started.md)を参照してください。

```bash
npm run check:ui -- --url http://127.0.0.1:8000/examples/overflow-walkthrough/before.html
npm run check:ui -- --url http://127.0.0.1:8000/examples/overflow-walkthrough/after.html
```

最初のコマンドはFAIL（終了コード1）が期待結果です。二つのコマンドは一つずつ実行してください。`&&`でつなぐと最初のFAILで止まります。

修正は以下だけです。文字の縮小や内容の非表示は使いません。

```css
.after .actions { flex-wrap: wrap; }
.after .action {
  white-space: normal;
  min-width: 0;
  max-width: 100%;
  overflow-wrap: anywhere;
}
```

## 判定条件

- PASS：修正前の412pxで横はみ出しを検出し、修正後の412pxと1440pxで同じ検査が通る。レポートと画像が保存される。
- WARN：自動検査は通るが、実フォントでの折り返しやボタンの読みやすさを目視確認していない。
- FAIL：修正前の不具合を検出できない、修正後にも横はみ出しが残る、または実行エラーをPASS扱いする。

今回は実装の折り返し指定に帰属する失敗です。共通契約を変更する必要はありません。レポートのPASSは横はみ出しだけを示します。

`tests/rendered/adoption.spec.mjs`はCLIを実際に起動して終了コードとEvidenceを確認します。修正前を通常の「すべて成功すべき画面」に加えるのではなく、FAILを検出できることをテストします。
