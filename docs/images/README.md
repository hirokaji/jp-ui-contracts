# 比較画像の出典と更新

`overflow-before.png`と`overflow-after.png`は実際のブラウザ描画です。生成画像や手作業で数値を付けたモックではありません。

- 取得元：[contract-validation run 41280827328](https://github.com/hirokaji/jp-ui-contracts/actions/runs/41280827328)
- 対象コミット：`5a11d14845ee589ce195d5589877f25b80a33994`
- テスト：`tests/rendered/adoption.spec.mjs`のwalkthrough検査
- 対象：`examples/overflow-walkthrough/before.html`と`after.html`
- 実行条件：デスクトップChromiumの表示領域を412 × 839 CSS pxに変更。Pixel 7実機の画面ではありません。
- 測定値・時刻・ブラウザバージョン・元artifactと画像のSHA256：[overflow-measurements.json](overflow-measurements.json)

JSON中の`screenshot: viewport.png`は取得時の各runディレクトリ内の名前です。ここに保存した名前との対応は`provenance.images`にあります。

## 再取得

`npm run test:rendered`を実行すると、walkthroughテストの出力ディレクトリに`walkthrough/before.png`、`after.png`、`measurements.json`が生成されます。CIでは`rendered-validation-evidence`から同じファイルを取得できます。

例やCSSを変更した場合は、同じ実行から取得した3ファイルをまとめて更新し、出典コミット・実行URL・ハッシュも更新します。READMEの表示値が測定記録と一致することを確認してください。画像は目視確認用で、ピクセル一致の合格基準にはしません。

CI artifactは14日で失効しますが、ここに保存した画像と測定記録はGitで保持します。
