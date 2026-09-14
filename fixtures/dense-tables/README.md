# dense-tables

## Purpose

日本語ラベル、数値、状態チップ、長い備考が同居する高密度テーブルで、**表の密度調整がページ全体のoverflowや走査性崩壊へ伝播しないか**を確認します。

## Profiles affected

- `saas`
- `dashboard`
- `docs`

## Stress conditions

- 長い日本語案件名
- 日本語と英語が混じる列
- 桁数の大きい数値
- 状態チップ
- 長い備考
- mobile widthでテーブル幅がviewportを超える状態

## PASS criteria

- ページ全体に横スクロールが発生しない
- 横幅が必要な場合、table wrapper内だけでスクロールできる
- 数値列の桁とラベルの対応を追える
- 状態ラベルが潰れない
- 本文向けの広い行間を表へそのまま継承していない

## WARN criteria

- wrapper内スクロールは成立しているが、重要列の対応が追いにくい
- 行高が過度に高い、または低い
- 長い日本語ラベルが頻繁に3行以上へ折り返す

## FAIL criteria

- document全体が横overflowする
- tableがcontainerを突き破る
- 数値・状態・案件名の対応が視覚的に追えない
- mobileで表が操作不能になる

## Contract return

失敗した場合は、まず `table density / overflow strategy / mobile fallback` を見直します。表だけの問題を本文Typographyの変更で解決しないでください。
