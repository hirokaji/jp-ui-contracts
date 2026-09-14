# long-paragraphs

## Purpose

長い日本語本文で、短いダミー文では見えない行間・字間・読み幅・和欧混植の破綻を再現します。

Open [`index.html`](index.html) at desktop and mobile widths. Do not judge from the heading alone; read through the full fixture.

## Profiles affected

- `media`
- `docs`
- `base`

## Test surface

- 3つの長い日本語段落
- inline English / `DESIGN.md` の和欧混植
- 引用ブロック
- キャプション
- 480px以下のモバイル幅

## PASS criteria

- 長文を連続して読んでも行間が窮屈または散漫に感じない
- body textへ強いletter-spacingを一括適用していない
- 日本語と英語が混ざっても局所的にリズムが崩れない
- 本文、引用、キャプションの役割が視覚的に区別できる
- モバイル幅でも一行長と段落間隔が破綻しない

## WARN criteria

- 読めるが、desktopかmobileのどちらかで段落密度が不安定
- 英数字の周辺だけ字面が浮く
- 引用やキャプションが本文と区別しづらい
- 実装は成立しているが、対応するcontract ruleが曖昧

## FAIL criteria

- 長文本文の既定line-heightが1.5未満で、実読上も窮屈
- 強いbody letter-spacingにより日本語本文が不自然
- 長文を収めるために文字サイズや行間を過度に圧縮している
- モバイルで横スクロール、切れ、重なりが発生する

## Contract return

WARN / FAILは、まず次のどこへ戻すかを決めます。

1. typography rule
2. profile default
3. responsive rule
4. fixture gap
5. implementation bug
