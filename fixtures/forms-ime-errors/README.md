# forms-ime-errors

## Purpose

日本語フォームで、長いラベル、補足文、エラー文、IME入力、長いbutton labelが同時に存在しても、密度と操作性が壊れないかを確認します。

Open [`index.html`](index.html) and test keyboard focus, Japanese IME input, validation errors, and mobile width.

## Profiles affected

- `saas`
- `dashboard`
- `base`

## Test surface

- 長い日本語field label
- helper text
- validation error
- textarea
- 日本語IME入力
- 長いaction label
- 420px以下のmobile layout

## PASS criteria

- label、input、help、errorの役割と順序が明確
- 日本語IME変換中でも入力領域と周辺テキストが重ならない
- error stateが色だけに依存しない
- controlは繰り返し操作できる高さと余白を保つ
- 長いbutton labelが切れず、mobileでは安全に折り返すまたは積み上がる

## WARN criteria

- 操作はできるが、help/errorが密集して読み違えやすい
- compact化のために一部ラベルやactionが窮屈
- IME確認が未実施で、実装上のリスクが残る
- desktopでは成立するがmobileで視線移動が増えすぎる

## FAIL criteria

- placeholderをlabelの代替として使う
- error/helpが入力欄や変換候補と重なる
- 長い日本語ラベルまたはbuttonがclipする
- mobileでcontrolがviewportを超える
- 密度を下げるために必要情報を隠し、入力判断ができなくなる

## Contract return

WARN / FAILは `form density rule`、component rule、responsive rule、accessibility rule、またはimplementation bugへ帰属させます。
