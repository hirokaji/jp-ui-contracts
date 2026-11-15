# motion-expand

## Purpose

展開・折りたたみパネルや、状態でラベルが変わるボタンのアニメーションが、日本語テキストを切ったり、周囲のレイアウトを動かしたりしないかを確認します。

Open [`index.html`](index.html), operate both patterns, and test at desktop width, at 420px and below, and with `prefers-reduced-motion` emulated in devtools.

外部のモーション部品集（アニメーションするボタン、カード、ドロップダウン等）向けのプロンプトをコーディングエージェントに貼る使い方が広がっています。それらの部品は短い英語ラベル前提で作られていることが多く、日本語の長いラベルと本文に差し替えると、アニメーション中と完了後に崩れます。この fixture は、その差し替えで起きる失敗を再現します。

## Profiles affected

- `saas`
- `dashboard`
- `base`

## Test surface

- 固定ピクセル高さへアニメーションする展開パネル（パターンA）
- `grid-template-rows` で展開するパネル（パターンB）
- 状態でラベルが変わり、幅がアニメーションするボタン（パターンA）
- 最長のラベル幅を予約するラベルスタック型ボタン（パターンB）
- 長い日本語の説明文（複数行）
- 420px以下のmobile layout
- `prefers-reduced-motion` 有効時の挙動

## PASS criteria

- 展開の途中・完了後とも、日本語本文の行が切れず、最終行まで読める
- 状態でラベルが変わっても、ボタンの幅と隣接要素の位置が動かない
- `prefers-reduced-motion` 有効時、アニメーションなしで同じ状態へ到達できる
- mobile幅でもパネルとボタンがviewport内に収まる

## WARN criteria

- 読めるが、アニメーション中に一時的なガタつきや行の再配置が目立つ
- reduced motion には対応するが、切り替えが唐突で現在状態が分かりにくい
- desktopでは成立するが、mobileで展開後の視線移動が増えすぎる

## FAIL criteria

- 固定高さや `overflow: hidden` で日本語本文の行が切れる
- ラベルの切り替えでボタン幅が変わり、周囲のレイアウトが移動する
- `white-space: nowrap` と幅アニメーションの組み合わせでラベルが切れる
- アニメーションが終わらないと内容や操作に到達できない
- `prefers-reduced-motion` を無視して動き続ける

## Contract return

WARN / FAILは `motion rule`（base `DESIGN.md` Section 10）、`recipes/motion.css`、component rule、またはimplementation bugへ帰属させます。
