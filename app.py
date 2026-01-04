import streamlit as st
import edge_tts
import asyncio
import os

# Cấu hình trang web
st.set_page_config(page_title="AI Đọc Văn Bản", page_icon="🎙️")
st.title("🎙️ Chuyển Văn Bản Thành Giọng Nói")
st.write("Công cụ tạo giọng đọc AI chuyên nghiệp miễn phí.")

# Danh sách giọng đọc
VOICES = {
    "Nữ - Hoài My (Nhẹ nhàng)": "vi-VN-HoaiMyNeural",
    "Nam - Nam Minh (Tin tức)": "vi-VN-NamMinhNeural"
}

# Giao diện người dùng
text_input = st.text_area("Nhập văn bản của bạn ở đây:", height=150, placeholder="Ví dụ: Xin chào, hôm nay trời thật đẹp...")
voice_choice = st.selectbox("Chọn giọng đọc:", list(VOICES.keys()))

# Hàm xử lý TTS
async def text_to_speech(text, voice_key):
    voice_id = VOICES[voice_key]
    output_file = "output.mp3"
    communicate = edge_tts.Communicate(text, voice_id)
    await communicate.save(output_file)
    return output_file

if st.button("🔊 Tạo Giọng Nói"):
    if text_input:
        with st.spinner("Đang xử lý... vui lòng đợi giây lát"):
            # Chạy hàm async trong môi trường Streamlit
            output_mp3 = asyncio.run(text_to_speech(text_input, voice_choice))
            
            # Hiển thị trình phát nhạc
            st.audio(output_mp3, format="audio/mp3")
            
            # Nút tải xuống
            with open(output_mp3, "rb") as file:
                st.download_button(
                    label="📥 Tải file MP3",
                    data=file,
                    file_name="giong_doc_ai.mp3",
                    mime="audio/mp3"
                )
            
            # Dọn dẹp file tạm (tùy chọn)
            # os.remove(output_mp3)
    else:
        st.warning("Vui lòng nhập văn bản trước!")