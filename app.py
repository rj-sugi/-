import random
import time
import streamlit as st

st.set_page_config(page_title="野生動物 位置情報入力（ランダム）", layout="centered")

# ---- セッション状態 ----
if "records" not in st.session_state:
    # [{"animal": "...", "lat": ..., "lon": ..., "ts": ...}, ...]
    st.session_state.records = []
if "sent" not in st.session_state:
    st.session_state.sent = False

st.title("野生動物の位置情報入力（位置情報はランダム生成）")
st.caption("動物アイコンを押す → ランダム座標を生成して記録 → 「データを送信」")

st.divider()

# ---- ランダム座標の生成範囲（例：日本付近）----
# 緯度: 24〜46（沖縄〜北海道あたり）
# 経度: 123〜146（日本の西〜東あたり）
LAT_MIN, LAT_MAX = 24.0, 46.0
LON_MIN, LON_MAX = 123.0, 146.0

with st.expander("ランダム生成の範囲（必要なら変更）", expanded=False):
    st.write(f"- 緯度: {LAT_MIN} ～ {LAT_MAX}")
    st.write(f"- 経度: {LON_MIN} ～ {LON_MAX}")

def generate_random_location():
    lat = random.uniform(LAT_MIN, LAT_MAX)
    lon = random.uniform(LON_MIN, LON_MAX)
    return lat, lon

def add_record(animal: str):
    lat, lon = generate_random_location()
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.records.append({
        "animal": animal,
        "lat": round(lat, 6),
        "lon": round(lon, 6),
        "timestamp": ts,
    })
    st.session_state.sent = False
    st.toast(f"{animal} を記録しました：({lat:.6f}, {lon:.6f})", icon="✅")

st.subheader("動物を記録（押した瞬間にランダム座標を生成）")
cols = st.columns(4)

with cols[0]:
    if st.button("🦌 鹿", use_container_width=True):
        add_record("鹿")
with cols[1]:
    if st.button("🐗 いのしし", use_container_width=True):
        add_record("いのしし")
with cols[2]:
    if st.button("🐒 ニホンザル", use_container_width=True):
        add_record("ニホンザル")
with cols[3]:
    if st.button("❓ その他", use_container_width=True):
        add_record("その他")

st.divider()

st.subheader("記録一覧（送信前）")
if len(st.session_state.records) == 0:
    st.write("まだ記録がありません。")
else:
    st.dataframe(st.session_state.records, use_container_width=True, hide_index=True)

left, right = st.columns([1, 1])

with left:
    if st.button("記録をクリア", use_container_width=True):
        st.session_state.records = []
        st.session_state.sent = False
        st.success("記録をクリアしました。")

with right:
    if st.button("データを送信", use_container_width=True, type="primary"):
        # 今回は外部送信は未定：送信処理はせず完了表示だけ
        if len(st.session_state.records) == 0:
            st.warning("送信するデータがありません。")
        else:
            st.session_state.sent = True

if st.session_state.sent:
    st.success("送信完了")
    # 将来の外部送信を想定して payload を確認したい場合は有効化
    # st.json({"payload": st.session_state.records})
