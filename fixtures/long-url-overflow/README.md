# long-url-overflow

## Purpose

長いURL、英単語、機械的IDが日本語本文、カード、タグの幅を壊さないかを確認します。

Open [`index.html`](index.html) on desktop and mobile widths.

## Profiles affected

- `media`
- `docs`
- `saas`
- `base`

## Test surface

- 本文中の長いURL
- 狭いcard内のURL
- 長いEnglish token
- machine-like identifier
- 長いtag label

## PASS criteria

- どのtokenもcontainerを横へ押し広げない
- overflow対策が通常の日本語本文へ不要な分断を持ち込まない
- URL、code、tagなどmachine-like contentだけを必要に応じて強く折り返す
- mobile幅でも横スクロールを発生させない

## WARN criteria

- overflowは防げているが、URL周辺の段落リズムが大きく崩れる
- 一部componentだけlocal overrideが必要だがcontractに記録されていない
- token handlingがbrowser差に依存する

## FAIL criteria

- horizontal overflowまたはlayout shiftが起きる
- 対策としてpage全体へ`word-break: break-all`を適用する
- URLやIDを守るためにcontainer自体を不自然に広げる
- mobileでcardやtagがviewportを超える

## Contract return

WARN / FAILは `overflow strategy`、component-specific rule、fixture gap、またはimplementation bugへ帰属させます。
