import os
import streamlit as st
from google import genai

# Page Config
st.set_page_config(
    page_title="Microsoft Annual Report RAG Assistant",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Microsoft 2025 Annual Report Assistant")
st.markdown(
    "Ask any question based on Microsoft's 2025 Annual Report data (Revenue,"
    " Azure milestones, AI infrastructure, etc.)."
)

# Initialize Gemini Client
# (Streamlit secrets ya environment variable se API key uthay ga)
api_key = os.environ.get("GEMINI_API_KEY") or st.secrets.get(
    "GEMINI_API_KEY", ""
)

if not api_key:
    st.warning("⚠️ Please configure your Gemini API Key in Streamlit Secrets.")

# User Input
user_query = st.text_input(
    "Ask a question about Microsoft's Annual Report:",
    placeholder="e.g., What was the total revenue and Azure revenue?",
)

if st.button("Get Answer") and user_query:
  if not api_key:
    st.error("Gemini API key is missing!")
  else:
    with st.spinner("Analyzing annual report chunks..."):
      try:
        client = genai.Client(api_key=api_key)

        # Context jo humne report se extract kiya tha
        context = """
                Microsoft 2025 Annual Report Key Data:
                - Total Revenue: $281.7 billion (up 15 percent).
                - Azure Revenue: Surpassed $75 billion in revenue for the first time (up 34 percent).
                - Datacenter Capacity & Scale: The network includes more than 400 datacenters across 70 regions (more than any other cloud provider), with over two gigawatts of new capacity added this year alone.
                - AI-First Regions & Cooling: Every Azure region is now AI-first and supports liquid cooling, increasing fleet fungibility and flexibility.
                - Fairwater AI Datacenter: Announced last month in southeastern Wisconsin, Fairwater is the world's most powerful AI datacenter and will deliver 10x the performance of today's fastest supercomputer.
                """

        prompt = f"""You are a helpful AI assistant. Answer the user's question accurately using ONLY the provided context below. If the answer is not in the context, say "I could not find this information in the company documents."

                Context:
                {context}

                Question: {user_query}
                """

        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt,
        )

        st.subheader("Answer:")
        st.write(response.text)

      except Exception as e:
        st.error(f"An error occurred: {e}")
