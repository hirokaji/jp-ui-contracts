// Shared content and behavior: the comparison changes CSS only. No network writes.
const state = new URLSearchParams(location.search).get('state') || 'normal';
const initialName = state === 'empty' ? '' : '品質保証チーム';
const deliveryLabel = state === 'long'
  ? '品質保証部・製造技術部・海外サービス拠点から届く、設計変更・製造条件の見直し・出荷後の対応方針に関する重要な変更通知と確認依頼をメールで受け取る'
  : '重要な変更通知をメールで受け取る';
document.querySelector('#settings').innerHTML = `
  <p class="eyebrow">ワークスペース設定 / 通知</p>
  <h1>通知設定</h1>
  <p class="intro">重要な変更の通知先と受信方法を確認します。</p>
  <p class="demo-note">検証用の合成例です。保存はこのページ内だけに反映されます。</p>
  <form novalidate>
    <div class="field">
      <label id="name-label" for="display-name">通知先の表示名</label>
      <p id="name-help" class="help">通知先を識別できる名前を入力してください。</p>
      <input id="display-name" name="displayName" aria-describedby="name-help name-error" autocomplete="off">
      <p id="name-error" class="error" role="alert" hidden>表示名を入力してください。設定は保存されていません。</p>
    </div>
    <div class="field choice">
      <input id="delivery" name="delivery" type="checkbox" checked>
      <label id="delivery-label" for="delivery"></label>
    </div>
    <div class="actions"><button id="save" type="submit">変更を保存</button><button id="reset" type="reset">元に戻す</button></div>
    <p id="result" role="status"></p>
  </form>`;
const form = document.querySelector('form');
const name = document.querySelector('#display-name');
const error = document.querySelector('#name-error');
const result = document.querySelector('#result');
name.defaultValue = initialName;
document.querySelector('#delivery-label').textContent = deliveryLabel;
function clearFeedback() {
  error.hidden = true;
  name.removeAttribute('aria-invalid');
  result.textContent = '';
}
function validate() {
  clearFeedback();
  if (!name.value.trim()) {
    error.hidden = false;
    name.setAttribute('aria-invalid', 'true');
    name.focus();
    return false;
  }
  return true;
}
form.addEventListener('submit', event => {
  event.preventDefault();
  if (validate()) result.textContent = 'このページ内に設定を保存しました。外部には送信していません。';
});
form.addEventListener('reset', clearFeedback);
form.addEventListener('input', clearFeedback);
if (state === 'error') { name.value = ''; validate(); }
document.querySelector('#settings').dataset.uiReady = 'true';
