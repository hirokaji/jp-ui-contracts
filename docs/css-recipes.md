# css-recipes

`recipes/` は、何でも貼る場所ではありません。  
契約で決めた方針を、再利用しやすいCSS断片にしたものです。

---

## 基本方針

- 契約に書くべきことは `DESIGN.md` に残す
- recipe は implementation の再利用単位に留める
- recipe は万能化しすぎない
- 特に `word-break` は乱暴に全体へ広げない

---

## 代表的な recipe

### `ja-text.css`
日本語本文の基本です。  
`line-break`、`overflow-wrap`、`font-kerning` の安定化に使います。

### `mixed-script.css`
日本語 + 英語混在時の安全策です。  
見出しや product name の扱いで役立ちます。

### `headings.css`
見出し専用の折り返しと `line-height` をまとめます。  
本文ルールと分けたいときに使います。

### `forms.css`
フォーム、ラベル、エラー表示の窮屈さを防ぎます。  
業務UIや設定画面で効きます。

---

## 使い方の考え方

次の順で考えると扱いやすいです。

1. まず `DESIGN.md` に方針を書く
2. その方針を何度も実装するなら recipe に切り出す
3. 画面ごとの例外は recipe ではなく component 側で処理する

つまり、recipe は「全部入りの魔法のCSS」ではなく、**契約を実装へ運ぶための薄い部品** として扱います。
