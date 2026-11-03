# 日本語UIを、自分の画面で確かめる

最初は、同じ画面の「不具合を検出する」「直して再検査する」を試します。その後、自分のアプリのローカルURLに切り替えます。

契約ファイルの検査と、実画面の検査は別々です。片方のPASSで、もう片方も確認できたことにはなりません。

## 1. 準備する

Git、Node.js 22、Python 3.12を使用し、公開済みv0.3.1を取得する手順です。Windows PowerShellとmacOS/Linuxのターミナルで、以下を一行ずつ実行できます。初回の依存関係・Chromium取得にはインターネット接続が必要です。

```bash
git clone --branch v0.3.1 https://github.com/hirokaji/jp-ui-contracts.git
cd jp-ui-contracts
npm install --ignore-scripts --no-audit --no-fund
npx playwright install chromium
```

タグを取得するため、Gitが`detached HEAD`と表示することがあります。この版を試すだけなら問題ありません。検査ツール自体を変更する場合は、作業ブランチを作成してください。

Linuxでブラウザの共有ライブラリ不足になる場合は、管理者がシステム依存を用意するか、`npx playwright install --with-deps chromium`を使用します。管理者権限を使えない環境で無理にインストールしないでください。Pythonの契約検査には追加パッケージは不要です。

以下のターミナル操作は、特記がない限り、このリポジトリのルートで行います。

## 2. 動く例を開く

ターミナルAでローカルサーバーを起動し、そのまま動かしておきます。

```bash
python -m http.server 8000 --bind 127.0.0.1
```

ブラウザで次の二つを開き、幅を412pxにして比較します。

- 修正前：<http://127.0.0.1:8000/examples/overflow-walkthrough/before.html>
- 修正後：<http://127.0.0.1:8000/examples/overflow-walkthrough/after.html>

同じ日本語ラベルのボタンを使っています。修正前は折り返し禁止で横にはみ出し、修正後はボタンの文言と配置を折り返します。これは導入用の合成例です。

## 3. 不具合を検出し、修正後を確かめる

ターミナルBを開き、同じリポジトリのルートへ移動します。

```bash
npm run check:ui -- --url http://127.0.0.1:8000/examples/overflow-walkthrough/before.html
```

期待結果は`FAIL document-horizontal-overflow`、終了コードは1です。故意に崩した例を検出できたことを示します。次のコマンドを別に実行します。

```bash
npm run check:ui -- --url http://127.0.0.1:8000/examples/overflow-walkthrough/after.html
```

こちらは`PASS document-horizontal-overflow`、終了コード0が期待結果です。出力の`clientWidth`と`scrollWidth`も確認してください。両コマンドを`&&`でつなぐと、最初のFAILで止まります。

実行ごとに`ui-evidence/run-*/report.json`と`viewport.png`が保存されます。JSONはテキストエディタ、画像は画像ビューアで開けます。出力された`Evidence:`のパスを使えば、今回の結果を特定できます。

**ERROR（終了コード2）は検査未成立です。** サーバー未起動、404、Chromium未導入などを直してから再実行してください。

## 4. 自分の案件の契約を作る

例として、`jp-ui-contracts`と同じ親フォルダに`my-app`という既存のアプリがある場合を示します。アプリにすでにDESIGN.mdがある場合は上書きせず、必要な項目を統合してください。

SaaS・管理画面なら`templates/saas/DESIGN.md`を、アプリ側の`my-app/DESIGN.md`へコピーします。エディタやファイルマネージャーでコピーできます。

最初に以下を編集します。

- `[Project Name]`を実際のプロジェクト名にする
- 利用者と画面の用途をProduct Useへ記載する
- Typography Defaultsの初期値を採用するか、用途に合わせて調整する
- Validation Targetsへ、今回確認する画面・幅・状態を具体的に記載する
- 実際にレビューするまではReview statusをdraftのままにする

日本語本文の禁則やフォント指定など、より詳しい項目が必要な場合は`templates/base/DESIGN.md`から取り込みます。profileファイルへbaseの全規則が自動継承される仕組みはありません。

契約だけを確認します。

```bash
python validators/contract.py validate --strict ../my-app/DESIGN.md
```

PASSは、メタデータなどの静的チェックに通ったという意味です。UIの検査実施やレビュー履歴を検証したわけではありません。WARNの内容も読み、不要なplaceholderは記入してください。

## 5. AIに実装を依頼する

以下は、自分のアプリ側でコーディングエージェントへ渡す依頼例です。対象画面名と起動方法は案件に合わせて記入します。

```text
このプロジェクトのDESIGN.mdを読み、通知設定画面を実装・修正してください。
長い日本語ラベルを使い、幅412pxと1440pxの両方で確認してください。
文字を小さくする、必要な内容を隠す、契約や検査を弱める方法で修正しないでください。
問題が出たら、契約・実装・検査のどこに原因があるかを説明してから修正してください。
最後に、変更内容、起動コマンド、対象のローカルURL、実行した検査、未確認の点を報告してください。
実行していない検査をPASSと書かないでください。
```

CSS recipesは必要なものを選び、アプリのスタイル構成へ組み込みます。DESIGN.mdを渡すだけでCSSが適用されるわけではありません。

## 6. 自分の画面を検査する

自分のアプリを通常の方法で起動します。以下の`http://127.0.0.1:3000/settings`は例なので、実際のURLへ置き換えてください。コマンドは検査ツール側の`jp-ui-contracts`ルートで実行します。

```bash
npm run check:ui -- --url http://127.0.0.1:3000/settings --width 412
npm run check:ui -- --url http://127.0.0.1:3000/settings --width 1440
```

SPAで非同期データを待つ場合は、画面が準備できたときにだけ表示する要素を指定します。

```bash
npm run check:ui -- --url http://127.0.0.1:3000/settings --ready-selector "[data-ui-ready]" --timeout 30000
```

新規ブラウザなので普段のログイン状態は引き継ぎません。認証が必要な画面は、実データを含まないローカルの再現画面を用意するなど、検証可能な状態を明示してください。

この検査は指定URLの画面全体の横はみ出しだけを測ります。DESIGN.mdの文字サイズや行間との自動照合は行いません。

## 7. 目視確認して記録する

自動検査後も、次を確認します。

- 文字・ラベル・表の内容が切り落とされていないか
- 日本語の改行、和欧混植、実際のフォントが読みやすいか
- IME変換中、エラー表示中、キーボード操作中に困らないか
- 必要な実機・ブラウザ・画面状態を確認したか

レビュー記録には、契約ファイル、対象URL、画面幅と状態、実行コマンド、結果、Evidenceのパス、未確認項目を残します。[scorecard](../validators/scorecard.md)と[検証範囲](validation-coverage.md)を併用してください。

## つまずいたとき

| 症状 | 確認すること |
|---|---|
| npm scriptやvalidatorが見つからない | ターミナルBがjp-ui-contractsのルートにいるか |
| ブラウザ実行ファイルがない | `npx playwright install chromium`が成功したか |
| 接続失敗・404 | サーバーが動いているか、ポートとパスが合っているか |
| 待機タイムアウト | 指定selectorが目的画面で可視になるか、データ読み込みが終わるか |
| PASSなのに文字が欠ける | 横はみ出しと内容の切り落としは別。目視と部品別検査が必要 |
| 別originへの移動でERROR | リダイレクト先と、検査したいローカルURLが一致しているか |

## リポジトリ自体を検証する場合

コントリビューター向けの検証は別に実行します。

```bash
python -m unittest discover -s tests -p "test_*.py" -v
npm run test:cli
npm run test:rendered
```

ブラウザテスト内のサーバー起動には`python3`を使用します。Windowsでそのコマンドがない場合、別ターミナルで`python -m http.server 4173 --bind 127.0.0.1`を起動してから、ローカルで`npm run test:rendered`を実行できます。CIはUbuntuで同じテストを実行します。

固定fixtureの成功は、あなたのアプリも検査済みという意味ではありません。アプリへの適用には手順6を使います。
