import streamlit as st
import edge_tts
import asyncio
import os

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="AI Đọc Văn Bản Pro", page_icon="🎛️", layout="centered")

st.title("🎛️ Studio Giọng Nói AI")
st.markdown("Tùy chỉnh tốc độ, cao độ và tạo file âm thanh chuyên nghiệp.")

# --- DANH SÁCH GIỌNG ---
# Edge-TTS chủ yếu cung cấp 2 giọng Việt chuẩn. 
# Mẹo: Chỉnh Cao độ (Pitch) sẽ giúp tạo ra các biến thể giọng khác nhau (trẻ hơn, trầm hơn).
VOICES = {
    "👩 Nữ - Hoài My (Truyền cảm)": "vi-VN-HoaiMyNeural",
    "👨 Nam - Nam Minh (Tin tức)": "vi-VN-NamMinhNeural"
}

# --- GIAO DIỆN NGƯỜI DÙNG ---

# 1. Khu vực nhập liệu
text_input = st.text_area("Nhập văn bản:", height=150, placeholder="Nhập nội dung bạn muốn chuyển đổi...")

# 2. Khu vực tùy chỉnh (Chia làm 2 cột cho đẹp)
col1, col2 = st.columns(2)

with col1:
    voice_choice = st.selectbox("Chọn giọng đọc:", list(VOICES.keys()))
    
    # Tốc độ đọc: Từ -50% (rất chậm) đến +50% (rất nhanh)
    speed = st.slider("Tốc độ đọc (Rate):", min_value=-50, max_value=50, value=0, step=10, format="%d%%")

with col2:
    # Cao độ: Giúp giọng trầm ấm hơn hoặc trẻ con hơn
    pitch = st.slider("Cao độ (Pitch):", min_value=-20, max_value=20, value=0, step=5, format="%dHz")
    st.caption("Mẹo: Tăng cao độ để giọng trẻ hơn, giảm để giọng trầm hơn.")

# --- HÀM XỬ LÝ TTS ---
async def text_to_speech(text, voice_key, rate, pitch):
    voice_id = VOICES[voice_key]
    output_file = "output.mp3"
    
    # Định dạng tham số cho edge-tts
    # Nếu rate > 0 thì thêm dấu +, ngược lại giữ nguyên
    rate_str = f"{rate:+d}%" 
    pitch_str = f"{pitch:+d}Hz"

    # Giao tiếp với API
    communicate = edge_tts.Communicate(text, voice_id, rate=rate_str, pitch=pitch_str)
    await communicate.save(output_file)
    return output_file

# --- NÚT XỬ LÝ ---
if st.button("🚀 Chuyển đổi ngay", type="primary"):
    if text_input:
        with st.spinner("AI đang đọc... vui lòng đợi"):
            try:
                # Gọi hàm async
                output_mp3 = asyncio.run(text_to_speech(text_input, voice_choice, speed, pitch))
                
                # Thành công
                st.success("Đã xong! Nghe thử bên dưới:")
                
                # Audio Player
                st.audio(output_mp3, format="audio/mp3")
                
                # Nút tải về
                with open(output_mp3, "rb") as file:
                    st.download_button(
                        label="📥 Tải xuống MP3",
                        data=file,
                        file_name="tts_audio.mp3",
                        mime="audio/mp3"
                    )
            except Exception as e:
                st.error(f"Có lỗi xảy ra: {e}")
    else:
        st.warning("Bạn chưa nhập văn bản nào cả!")

# --- FOOTER ---
st.markdown("---")
st.markdown("Made with ❤️ by Streamlit & Edge-TTS")
