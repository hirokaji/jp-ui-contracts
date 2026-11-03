# 通知設定：内容を保った比較と要素検査

mainの未リリース機能です。v0.3.1タグには含まれません。これは用途を限定した合成例であり、AIが作った画面を収集した実験や利用者評価ではありません。

[DESIGN.md](DESIGN.md)を契約とし、before / afterで同じJavaScript、文言、初期値、入力制約、保存・取消処理を使用します。外部通信や永続保存はありません。

## 比較する

リポジトリのルートで起動します。

```bash
python -m http.server 8000 --bind 127.0.0.1
```

- before: <http://127.0.0.1:8000/examples/notification-settings/before.html?state=long>
- after: <http://127.0.0.1:8000/examples/notification-settings/after.html?state=long>

`state`は`normal` / `long` / `empty` / `error`。幅320、412、1440pxで比較します。主操作は「変更を保存」、補助操作は「元に戻す」です。空入力で保存すると入力欄へフォーカスが戻り、訂正後に再度保存できます。リロードすると初期状態へ戻ります。

| 観測・変更 | 判断根拠 | 保留する評価 |
|---|---|---|
| beforeの長文ラベルは箱内で切れ、afterは折り返す | 必要な文言を読めることがMUST。局所overflowで検出する | 祖先によるクリップや他要素との重なりの一般検出 |
| beforeでは二つのボタンが同じ強さ、afterでは保存を強調 | 主操作を一つにする、この例のDEFAULT | 操作時間や誤操作率の改善は未測定 |
| カードを整理し、左揃えでフォームをまとめる | 同一タスクの項目を追える配置を提案 | ブランド適合性、実利用者の好み |
| 紫やグラデーションを変更する | 比較用の選択。色自体は失敗理由にしない | 元の配色にも用途上の根拠があれば維持できる |

## 再現可能な検査

```bash
python validators/contract.py validate --strict examples/notification-settings/DESIGN.md
npx playwright test tests/rendered/notification-settings.spec.mjs
```

- PASS: afterの指定4要素が文字サイズ・行間・収まりを満たし、内容と入力値を前後で保持する。
- FAILの反例: beforeの長文ラベルは文書全体の横はみ出しがなくても要素検査でFAILになる。テスト自体はこのFAILの検出を期待する。
- WARN / 受入保留: 実IME、読み上げ、実機、200%ブラウザズーム、利用者評価は未確認。契約のReview statusはdraftのままにする。

既存の`check:ui`は文書全体の横はみ出しだけを判定し、この任意表を読みません。必須fixture7種類の内容・合格条件も変更しません。

## DESIGN.mdから測る範囲

`validators/measured-elements.mjs`を自分のPlaywrightテストから呼び出せます。

```js
import { readFile } from 'node:fs/promises';
import { parseMeasuredElements, inspectMeasuredElements } from '../../validators/measured-elements.mjs';
const targets = parseMeasuredElements(await readFile('examples/notification-settings/DESIGN.md', 'utf8'));
// pageを対象状態へ移動し、画面の準備完了とdocument.fonts.readyを待つ。
const checks = await inspectMeasuredElements(page, targets);
```

`## Measured Elements`の表が唯一の編集元です。CSS selectorは一意なブロック・flex子・ボタンなど、測定可能なボックスを指定します。表内の`|`を含むselectorには対応しません。下限値はこの例固有で、全画面へ適用する規格ではありません。

- `Min font px`: computed font-sizeの下限。
- `Min line-height`: computed line-height / font-sizeの下限（丸め許容0.001）。`normal`は数値として確認できないためFAIL。
- `fit`: 要素自身のscrollWidth/clientWidthとscrollHeight/clientHeightの差が各1 CSS px以内。
- `scroll-x`: overflow-xがauto / scrollで、縦の差が1 CSS px以内。横スクロールの操作性までは証明しない。

対象がない・複数ある・不可視ならFAIL。不正な表やselectorは例外になり、テストは失敗します。例外をPASSへ変換しないでください。これは任意DOMの完全可視性検査ではありません。子孫の個別フォント、祖先による切り落とし、重なり、透明な文字、clip-path、実際の字形、コントラストは別途確認します。

## Evidence

テストは状態ごとの前後画像、320px画像、JSON計測値をPlaywrightレポートへ添付します。JSONには対象ソースのSHA-256、URL、viewport、ブラウザ版、時刻、指定条件と実測値、未検査範囲を記録します。CIの`rendered-validation-evidence` artifactにはこのレポートと画像が入り、保存期間は14日です。

[条件付き視覚レビュー](../../docs/conditional-visual-review.md)と併用し、見た目の評価を計測結果と混同しないでください。
