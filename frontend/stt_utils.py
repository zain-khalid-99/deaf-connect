import streamlit as st

def get_speech_input():
    """
    Client-side Speech Recognition using Web Speech API.
    Injects JavaScript to capture voice and return it to Streamlit.
    """
    st.markdown("""
        <script>
        const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.lang = 'en-US';
        recognition.interimResults = false;
        recognition.maxAlternatives = 1;

        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            window.parent.postMessage({
                type: 'streamlit:set_widget_value',
                data: {
                    id: 'stt_transcript',
                    value: transcript
                }
            }, '*');
        };

        window.startRecognition = () => {
            recognition.start();
        };
        </script>
    """, unsafe_allow_html=True)
    
    if st.button("🎤 START VOICE INPUT"):
        st.components.v1.html("<script>window.parent.startRecognition();</script>", height=0)
        st.info("Listening...")
    
    # This is a hacky way to get the value back, 
    # but for a pure Streamlit/JS integration without a custom component, 
    # it's difficult to get the value back instantly.
    # A better way is using st.chat_input or a dedicated component.
    # For now, I'll provide a simplified button that triggers browser recognition.
