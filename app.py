import streamlit as st
from google import genai
from google.genai import types
import base64

# --- CẤU HÌNH TRANG WEB ---
st.set_page_config(page_title="Gemini AI Voice", page_icon="🎙️", layout="centered")

st.title("🎙️ Gemini AI - Giọng Đọc Cảm Xúc")
st.markdown("Sử dụng mô hình **Gemini 2.0 Flash** để tạo giọng đọc tự nhiên như người thật.")

# --- CỘT TRÁI: CÀI ĐẶT ---
with st.sidebar:
    st.header("⚙️ Cài đặt")
    # Nhập API Key
    api_key_input = st.text_input("Nhập Google API Key:", type="password", help="Lấy tại aistudio.google.com")
    
    # Kiểm tra Key trong hệ thống (dành cho lúc deploy lên mạng)
    if "GEMINI_API_KEY" in st.secrets:
        api_key_to_use = st.secrets["GEMINI_API_KEY"]
        st.success("✅ Đã tìm thấy API Key trong hệ thống")
    else:
        api_key_to_use = api_key_input

    st.divider()
    st.info("💡 **Mẹo:** Các giọng đọc này (Puck, Kore...) là AI thế hệ mới, có khả năng diễn xuất theo cảm xúc bạn chọn.")

# --- DANH SÁCH GIỌNG GEMINI ---
GEMINI_VOICES = {
    "Puck (Nam - Trầm ấm, Kể chuyện)": "Puck",
    "Charon (Nam - Già dặn, Nghiêm túc)": "Charon",
    "Kore (Nữ - Nhẹ nhàng, Thư giãn)": "Kore",
    "Fenrir (Nam - Mạnh mẽ, Năng lượng)": "Fenrir",
    "Aoede (Nữ - Sang trọng, Tin tức)": "Aoede"
}

# --- GIAO DIỆN CHÍNH ---
col1, col2 = st.columns([2, 1])

with col1:
    text_input = st.text_area("Nhập văn bản cần đọc:", height=200, placeholder="Ví dụ: Xin chào, tôi là Gemini. Hôm nay bạn muốn nghe kể chuyện gì không?")

with col2:
    voice_choice = st.selectbox("Chọn giọng đọc:", list(GEMINI_VOICES.keys()))
    selected_voice_id = GEMINI_VOICES[voice_choice]
    
    st.write("---")
    st.write("**🎭 Chỉ đạo diễn xuất:**")
    style_guide = st.selectbox("Phong cách:", ["Bình thường", "Vui vẻ/Hào hứng", "Buồn bã/Trầm ngâm", "Thì thầm/Bí ẩn"])

# --- HÀM XỬ LÝ ---
def generate_audio(text, voice, style, api_key):
    try:
        client = genai.Client(api_key=api_key)
        
        # Tạo câu lệnh nhắc (Prompt) để chỉnh cảm xúc
        prompt_text = text
        if style == "Vui vẻ/Hào hứng":
            prompt_text = f"Hãy đọc đoạn văn sau với giọng cực kỳ vui vẻ, hào hứng: '{text}'"
        elif style == "Buồn bã/Trầm ngâm":
            prompt_text = f"Hãy đọc đoạn văn sau với giọng buồn bã, chậm rãi: '{text}'"
        elif style == "Thì thầm/Bí ẩn":
            prompt_text = f"Hãy đọc đoạn văn sau bằng giọng thì thầm, bí ẩn: '{text}'"
        
        # Gọi Gemini
        response = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents=prompt_text,
            config=types.GenerateContentConfig(
                response_modalities=["AUDIO"],
                speech_config=types.SpeechConfig(
                    voice_config=types.VoiceConfig(
                        prebuilt_voice_config=types.PrebuiltVoiceConfig(
                            voice_name=voice
                        )
                    )
                )
            )
        )
        return response
    except Exception as e:
        return str(e)

# --- NÚT BẤM ---
if st.button("🔊 Đọc Ngay", type="primary", use_container_width=True):
    if not text_input:
        st.warning("Vui lòng nhập văn bản!")
    elif not api_key_to_use:
        st.error("Chưa có API Key. Hãy nhập ở cột bên trái!")
    else:
        with st.spinner("Đang tạo giọng nói..."):
            result = generate_audio(text_input, selected_voice_id, style_guide, api_key_to_use)
            
            if isinstance(result, str): # Nếu lỗi
                st.error(f"Lỗi: {result}")
            elif result.candidates and result.candidates[0].content.parts:
                audio_bytes = result.candidates[0].content.parts[0].inline_data.data
                decoded_audio = base64.b64decode(audio_bytes)
                
                st.audio(decoded_audio, format="audio/wav")
                
                st.download_button(
                    label="📥 Tải về máy (.wav)",
                    data=decoded_audio,
                    file_name="gemini_voice.wav",
                    mime="audio/wav"
                )
                st.success("Thành công!")
            else:
                st.error("Không nhận được âm thanh từ Gemini.")


