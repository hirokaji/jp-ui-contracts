# jp-ui-contracts

> Japanese UI design contracts for AI builders.  
> `DESIGN.md` templates, CSS recipes, and validation rules for Japanese interfaces.

`jp-ui-contracts` は、日本語UI向けの **design contract kit** です。  
公開サイトの見た目を収集する「見本集」ではなく、AIエージェントやコード生成ツールが **日本語本文・見出し・和欧混植・改行・フォーム密度** を壊しにくくするための、**契約テンプレート / CSS recipe / review rule** をまとめたリポジトリです。

---

## このrepoがやること

- 日本語UI向け `DESIGN.md` テンプレートを提供する
- 用途別の profile を提供する
  - `base`
  - `media`
  - `saas`
  - `docs`
  - `dashboard`
- 日本語組版向けの CSS recipe を提供する
- AI生成UIを見直す validator を提供する
- `DESIGN.md` と preview を往復しやすくするサンプルを提供する

## このrepoがやらないこと

- 公開サイトの完全模写
- ブランド見本帳の拡張
- 日本語組版の唯一絶対ルールの断定
- プロンプトだけで画面品質を保証すること

---

## なぜ必要か

日本語UIは、色・角丸・余白だけでは品質が出ません。  
問題になりやすいのは、むしろ次の層です。

- 和文フォントの fallback が曖昧
- 和欧混植時の違和感
- 本文と見出しで分けるべき line-height の未分離
- 本文への過剰な letter-spacing
- `word-break: break-all` の乱用
- URL や英単語のはみ出し
- 表やフォームが本文ルールをそのまま引きずること

このrepoは、それらを「感覚」ではなく、**AIが読める契約**として扱います。

---

## 設計原則

### 1. Contract first
毎回のプロンプトで見た目を説明するのではなく、プロジェクト側に契約を置きます。

### 2. Context-aware defaults
日本語UIは一枚岩ではありません。  
記事メディア、SaaS、技術文書、ダッシュボードでは、密度も行間も改行戦略も変わります。

### 3. Mixed-script safety
日本語だけ、英語だけではなく、**日本語と英語が混ざった状態で成立すること**を重視します。

### 4. Progressive enhancement
新しいCSS機能は活かしつつ、未対応環境で壊れない設計を優先します。

### 5. Human review before canonization
スクリーンショットがきれいでも終わりません。  
実際に読む、詰める、入力する、折り返す、を確認してから採用します。

---

## Profiles

| Profile | 向いているもの | 重点 |
|---|---|---|
| `base` | 最小共通契約 | locale / typography / validation の基礎 |
| `media` | note、ブログ、オウンドメディア | 段落の呼吸、記事のリズム |
| `saas` | 管理画面、設定画面、B2Bツール | 密度、ラベル、フォーム安定 |
| `docs` | 技術文書、ヘルプ、ナレッジ | 本文とコードの両立 |
| `dashboard` | KPI画面、監視画面、分析UI | 走査性、表、数値、カード密度 |

---

## Directory structure

```text
jp-ui-contracts/
├─ README.md
├─ LICENSE
├─ CONTRIBUTING.md
├─ docs/
├─ templates/
├─ recipes/
├─ validators/
├─ schema/
└─ examples/
```

- `templates/`: 複製して使う `DESIGN.md`
- `recipes/`: 日本語UI向け CSS 断片
- `validators/`: AI生成UIの見直しルール
- `docs/`: 設計思想と使い分け
- `schema/`: 将来の機械検証向けスキーマ
- `examples/`: サンプル `DESIGN.md` と `preview.html`

---

## Quick start

### 1. template を選ぶ

最初は次のどれかを複製します。

- `templates/base/DESIGN.md`
- `templates/media/DESIGN.md`
- `templates/saas/DESIGN.md`
- `templates/docs/DESIGN.md`
- `templates/dashboard/DESIGN.md`

### 2. ブランド情報を埋める

- 色
- フォント
- 余白
- コンポーネント方針
- 禁止事項
- validation target

を埋めます。

### 3. recipe を追加する

`recipes/` の CSS を必要なものだけ導入します。

### 4. validator で見る

`validators/` のチェックリストと lint ルールで見直します。

### 5. preview を作る

契約だけで終わらせず、最小の `preview.html` を作って確認します。

---

## Recommended workflow

1. `DESIGN.md` を書く  
2. AIにUIを生成させる  
3. preview を見る  
4. validator で差分を記録する  
5. 契約へ戻して修正する  
6. 再生成する  

このrepoは、1回で当てるためのものではありません。  
**契約 → 生成 → 目視 → 契約修正** のループを速くするためのものです。

---

## Example usage

- 記事メディアなら `templates/media/DESIGN.md`
- 管理画面なら `templates/saas/DESIGN.md`
- 技術文書なら `templates/docs/DESIGN.md`
- 高密度BI画面なら `templates/dashboard/DESIGN.md`

サンプルは `examples/` に入っています。  
ブラウザで直接 `preview.html` を開くか、ローカルサーバーを立てて確認してください。

```bash
python -m http.server 8000
```

その後、`http://localhost:8000/examples/sample-media/preview.html` のように開けます。

---

## Roadmap

- `design-contract.schema.json` の拡充
- preview サンプルの増加
- validator の半自動化
- mixed-script review の強化
- mobile / desktop の別基準追加
- 日本語フォームUI、表UI、ナビゲーションUIの細分化

---

- ## What to improve next

`jp-ui-contracts` is not just a template collection.  
The next step is to make the contract more testable, more comparable, and easier to improve from real-world failures.

In the short term, this repository will evolve in four directions:

1. **Stronger contract structure**  
   Make `DESIGN.md` easier to lint and compare by clarifying required fields, validation targets, and profile-specific overlays.

2. **Validation-first workflow**  
   Treat generated UI as reviewable output. The goal is not one-shot perfection, but a stable loop of contract → generation → review → contract update.

3. **Reusable fixtures**  
   Build a shared set of failure-prone Japanese UI cases such as long paragraphs, mixed-script headings, long URLs, tables, forms, and mobile wrapping.

4. **Community feedback intake**  
   Convert stars and reactions into actionable issue reports and profile gap requests.

---

## Validation model

This repository uses a two-layer validation model.

### 1. Static validation
Check whether the contract itself is sufficiently specified.

Examples:
- Is the locale explicit?
- Is the profile selected?
- Is Japanese font fallback declared?
- Is `word-break: break-all` avoided as a global default?
- Are validation targets written down?

### 2. Visual validation
Check whether the generated UI still respects the contract once rendered.

Examples:
- Long Japanese paragraphs remain readable
- Mixed Japanese-English headings do not break awkwardly
- Long URLs do not destroy paragraph rhythm
- Tables and forms do not inherit article spacing blindly
- Mobile width remains stable

---

## Validator scorecard

We score validation results using three levels.

- **PASS**: acceptable for current profile
- **WARN**: usable, but contract or implementation should be tightened
- **FAIL**: violates contract or breaks readability / usability

See [`validators/scorecard.md`](validators/scorecard.md) for the detailed review sheet.

---

## Fixtures

The repository will grow around reusable fixtures rather than brand imitation.

Initial fixture families:
- long paragraphs
- mixed-script headings
- long URL overflow
- forms with helper and error text
- dense tables
- mobile wrapping
- docs-style prose + code coexistence

See [`fixtures/fixture-matrix.md`](fixtures/fixture-matrix.md).

---

## Feedback channels

To keep improvements grounded in real use cases, issue intake is split into two tracks.

- **Broken output report**  
  For cases where the current contract produced unstable or poor Japanese UI.

- **Profile gap request**  
  For cases where an existing profile is too weak or a new profile / overlay is needed.

Issue forms live in `.github/ISSUE_TEMPLATE/`.

---

## Recommended next commit order

1. Add Issue Forms and config
2. Add validator scorecard
3. Add fixture matrix
4. Add `profile-selector.md`
5. Add real fixture samples
6. Start collecting broken outputs from users

---

## License

MIT

---

## Start here

まずは `templates/base/DESIGN.md` をコピーし、  
`Locale / Profile / Typography / Validation Targets` を埋めてください。
