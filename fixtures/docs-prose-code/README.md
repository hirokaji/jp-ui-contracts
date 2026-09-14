# docs-prose-code

## Purpose

技術文書で、日本語本文、inline code、長いcode block、callout、tableが同じ画面に共存したとき、**それぞれの密度とoverflow責任を分離できているか**を確認します。

## Profiles affected

- `docs`
- `base`

## Stress conditions

- 長い日本語本文
- 日本語文中の英語identifier / inline code
- 横幅の長いcode block
- 長いmachine-like identifier
- callout内の長文
- 日本語と英語が混在するtable
- mobile viewport

## PASS criteria

- document全体に横overflowが発生しない
- 長いcode blockはcode領域内で横スクロールできる
- code blockの正確な文字列を本文都合で強制改行しない
- calloutが本文と区別でき、過度に圧縮されない
- tableのoverflowがtable wrapper内に封じ込められる
- inline codeが日本語本文の行高を大きく乱さない

## WARN criteria

- document overflowはないが、code blockの横スクロールに気づきにくい
- calloutと本文の視覚的な差が弱い
- inline codeが多い段落で行間が不均一になる
- mobileで表やコードの走査に負荷が高い

## FAIL criteria

- code blockまたはtableがdocument全体を横へ押し広げる
- codeを無理に折り返して識別子やコピー可能性を壊す
- calloutが本文と同じ密度で潰れる
- 本文向けのspacing ruleがcode / tableへそのまま継承される

## Contract return

失敗は `prose typography / code surface / callout component / table density / overflow strategy` のどこへ戻すべきかを切り分けます。技術文書全体を一つのTypography設定だけで解決しないでください。
