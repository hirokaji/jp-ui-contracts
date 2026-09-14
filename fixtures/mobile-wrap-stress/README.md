# mobile-wrap-stress

## Purpose

狭いviewportで、長い日本語見出し、和欧混植、長い識別子、フォーム、複数アクションが同時に現れたとき、**読みやすさと操作性を保ったまま折り返せるか**を確認します。

## Profiles affected

- `base`
- `media`
- `saas`
- `docs`
- `dashboard`

## Stress conditions

- 日本語 + 英語製品名を含む長い見出し
- 長いmachine-like identifier
- 長い日本語input value
- 複数ボタン
- 長い確認アクション
- 400px前後のnarrow mobile viewport（CIではPixel 7 profile）

## PASS criteria

- document全体に横overflowが発生しない
- 見出しや長いtokenがcontainerを突き破らない
- 主要操作の高さが44px以上ある
- 長い日本語ボタンラベルを省略せず操作できる
- inputがviewport幅を押し広げない

## WARN criteria

- overflowはしないが、見出しが過度に細切れになる
- ボタンの折り返しで意味のまとまりが読み取りにくい
- 主要操作と副操作の優先順位が狭幅で不明瞭になる

## FAIL criteria

- document-level horizontal overflowが発生する
- 操作対象が44px未満になる
- 長いtokenやinputがcontainer外へ飛び出す
- action labelが切れて判断できない

## Contract return

失敗は `responsive behavior / line-break strategy / component sizing / action hierarchy` のどこへ戻すべきかを切り分けます。単純な文字縮小で逃げないでください。
