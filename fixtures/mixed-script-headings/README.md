# mixed-script-headings

## Purpose

日本語見出しに英語の製品名、略語、ファイル名、スラッシュ区切りが混ざったときの折り返しと視覚リズムを確認します。

Open [`index.html`](index.html) and resize from desktop to narrow mobile widths.

## Profiles affected

- `media`
- `docs`
- `saas`
- `base`

## Test surface

- 日本語 + English product name
- `DESIGN.md` のようなfile token
- `API / CLI / Browser` のslash-separated tokens
- `LLM / RAG / MCP` の短い略語
- 業務語 + English action label

## PASS criteria

- 英単語や略語の直前・直後で不自然な孤立行を作らない
- 見出し階層がdesktop/mobileの両方で維持される
- 英語だけを詰める調整が日本語側のリズムを壊さない
- 長いtokenに対するoverflow対策が見出し全体へ過剰な副作用を出さない

## WARN criteria

- 意味は読めるが、狭幅で英語tokenだけが視覚的に浮く
- 一部の見出しで折り返し位置が不自然
- browser依存の新しいline-break機能に強く依存している

## FAIL criteria

- 見出しがcontainerを横にはみ出す
- global `word-break: break-all` で日本語を文字単位に乱暴に分断する
- 英数字を守るために見出し全体が極端に小さくなる
- mobileで見出しと本文の階層が判別できない

## Contract return

WARN / FAILは `mixed-script rule`、`line-breaking rule`、`responsive rule`、またはimplementation bugへ帰属させます。
