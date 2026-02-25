import gradio as gr
import os
import whisper
from gtts import gTTS
from groq import Groq
import tempfile
import warnings

# Suppress warnings for a clean console
warnings.filterwarnings("ignore")

# 1. Initialize Clients securely
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

print("Initializing Whisper model...")
model = whisper.load_model("base") 
print("System Ready.")

# The core instructions for the AI
SYSTEM_PROMPT = {"role": "system", "content": "You are a professional, intelligent AI assistant demonstrating a low-latency voice architecture. Provide concise, highly accurate, and polite responses."}

# Helper function to format the memory for the new Gradio UI
def get_ui_chat(state):
    # Returns all messages except the hidden system prompt
    return [msg for msg in state if msg["role"] != "system"]

# 2. Main Processing Logic
def process_voice_conversation(audio_path, llm_state):
    if not audio_path:
        return get_ui_chat(llm_state), llm_state, None, None

    try:
        # Step A: Speech-to-Text
        transcription = model.transcribe(audio_path)
        user_text = transcription["text"].strip()
        
        if not user_text:
            return get_ui_chat(llm_state), llm_state, None, None

        # Add user prompt to internal memory
        llm_state.append({"role": "user", "content": user_text})

        # Step B: LLM Processing via Groq
        chat_completion = client.chat.completions.create(
            messages=llm_state,
            model="llama-3.3-70b-versatile",
        )
        ai_text = chat_completion.choices[0].message.content
        
        # Add AI response to internal memory
        llm_state.append({"role": "assistant", "content": ai_text})

        # Step C: Text-to-Speech
        tts = gTTS(text=ai_text, lang='en', slow=False)
        temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(temp_audio.name)

        # Return the strictly formatted dict list, memory state, output audio, and clear input
        return get_ui_chat(llm_state), llm_state, temp_audio.name, None

    except Exception as e:
        error_msg = f"System Error: {str(e)}"
        llm_state.append({"role": "assistant", "content": error_msg})
        return get_ui_chat(llm_state), llm_state, None, None

# Function to completely wipe the session memory and UI
def reset_conversation():
    return [], [SYSTEM_PROMPT], None, None

# 3. Professional UI Design
custom_theme = gr.themes.Monochrome(
    font=[gr.themes.GoogleFont("Inter"), "ui-sans-serif", "system-ui", "sans-serif"],
    primary_hue="slate",
    secondary_hue="gray",
)

with gr.Blocks(title="VocaFree AI - Research Prototype", theme=custom_theme) as demo:
    
    # Hidden state variable to hold the LLM's memory securely
    llm_state = gr.State([SYSTEM_PROMPT])
    
    # Header
    gr.Markdown(
        """
        # VocaFree AI: Zero-Cost, Low-Latency Voice Interface
        **Research & Development Prototype** | Demonstrating real-time voice synthesis utilizing Groq LPUs.
        ---
        """
    )
    
    with gr.Tabs():
        
        # TAB 1: The Live App
        with gr.Tab("🎙️ Live Interaction"):
            with gr.Row():
                with gr.Column(scale=2):
                    # Chatbot component specifically ready for dict-format
                    chatbot = gr.Chatbot(
                        label="Conversation Transcript", 
                        height=450,
                        avatar_images=(None, "⚙️") 
                    )
                
                with gr.Column(scale=1):
                    gr.Markdown("### Input / Output Controls")
                    
                    audio_input = gr.Audio(
                        sources=["microphone"], 
                        type="filepath", 
                        label="1. Record Voice Prompt"
                    )
                    submit_btn = gr.Button("Submit Audio", variant="primary")
                    
                    gr.Markdown("---")
                    audio_output = gr.Audio(
                        label="2. System Voice Response", 
                        autoplay=True, 
                        interactive=False
                    )
                    clear_btn = gr.Button("🗑️ Reset Session")

        # TAB 2: Architecture & Documentation
        with gr.Tab("📊 System Architecture"):
            gr.Markdown(
                """
                ### Architectural Overview
                This prototype demonstrates a high-efficiency pipeline for voice-to-voice AI interaction, designed to bypass traditional paid APIs by leveraging open-weights and free-tier infrastructure.

                **Data Flow & Technologies:**
                1. **Input (Speech-to-Text):** User audio is captured and processed locally/in-container using **OpenAI's Whisper (Base)** model.
                2. **Processing (LLM):** The transcribed text is sent to **Meta's LLaMA 3.3 (70B)**. To ensure near-zero latency, inference is handled via **Groq's LPU** (Language Processing Unit) API.
                3. **Output (Text-to-Speech):** The resulting text is synthesized back into human-like audio using **Google TTS (gTTS)**.
                4. **Interface:** The frontend is built utilizing **Gradio**, deployed via a Dockerized Hugging Face Space.

                *This pipeline achieves comparable conversational latency to premium subscription services at zero operating cost.*
                """
            )

    # Footer
    gr.Markdown(
        """
        ---
        <div style="text-align: center; color: gray; font-size: 0.8em;">
            Developed for demonstration purposes. Powered by Whisper, LLaMA 3.3, Groq, and Gradio.
        </div>
        """
    )

    # Event Wiring: Notice how we derive the UI Chatbot purely from the llm_state now
    submit_btn.click(
        fn=process_voice_conversation,
        inputs=[audio_input, llm_state],
        outputs=[chatbot, llm_state, audio_output, audio_input]
    )
    
    # Event Wiring: Clear Session 
    clear_btn.click(
        fn=reset_conversation,
        inputs=[],
        outputs=[chatbot, llm_state, audio_input, audio_output]
    )

if __name__ == "__main__":
    # 0.0.0.0 binds to all interfaces, required for Docker/Hugging Face
    demo.launch(server_name="0.0.0.0", server_port=7860)
