import streamlit as st
from scrape import WebScraper
from parse import ContentParser
import pandas as pd

def main():
    st.set_page_config(page_title="AI Web Scraper", layout="wide")
    
    st.title("🌐 Smart Web Scraper with AI Analysis")
    
    # Initialize session state
    if 'scraped_data' not in st.session_state:
        st.session_state.scraped_data = None
    if 'parsed_data' not in st.session_state:
        st.session_state.parsed_data = None
    if 'show_full_content' not in st.session_state:
        st.session_state.show_full_content = False
    if 'scraping_done' not in st.session_state:
        st.session_state.scraping_done = False
        
    # Sidebar settings
    st.sidebar.header("⚙️ Settings")
    wait_time = st.sidebar.slider("Page Load Wait Time (seconds)", 1, 10, 5)
    
    # URL Input Section
    url = st.text_input("🔗 Enter URL to analyze")
    
    if st.button("🔍 Scrape Website"):
        if url:
            scraper = WebScraper()
            with st.spinner("Scraping website..."):
                st.session_state.scraped_data = scraper.scrape_website(url, wait_time)
                if st.session_state.scraped_data:
                    st.session_state.scraping_done = True
                    st.success("Website scraped successfully!")
                else:
                    st.error("Failed to scrape the website. Please check the URL and try again.")
    
    # Show analysis section only after successful scraping
    if st.session_state.scraping_done and st.session_state.scraped_data:
        st.markdown("---")
        st.subheader("🤖 AI Analysis")
        
        # Preview of scraped content
        with st.expander("📄 View Scraped Content Preview"):
            preview_text = ' '.join(st.session_state.scraped_data['text_content'].split())[:500]
            st.write(f"{preview_text}...")
        
        # Question input and analysis
        st.markdown("### ❓ What would you like to know about this page?")
        user_question = st.text_area(
            "",
            placeholder="Examples:\n- What are the main topics discussed?\n- Can you summarize the key points?\n- What products or services are mentioned?",
            help="Be specific with your question for better results"
        )
        
        if st.button("🚀 Analyze with AI"):
            if user_question:
                parser = ContentParser()
                with st.spinner("Processing with AI..."):
                    st.session_state.parsed_data = parser.parse_content(
                        st.session_state.scraped_data,
                        user_question
                    )
                    
                if st.session_state.parsed_data:
                    # Display AI Analysis
                    st.markdown("### 📊 Analysis Results")
                    st.write(st.session_state.parsed_data['summary'])
                    
                    # Additional information in expandable sections
                    col1, col2 = st.columns(2)
                    with col1:
                        with st.expander("🔍 Related Links"):
                            df = pd.DataFrame(
                                st.session_state.parsed_data['extracted_links'], 
                                columns=['URLs']
                            )
                            st.dataframe(df)
                    
                    with col2:
                        with st.expander("📑 Page Headers"):
                            for header in st.session_state.parsed_data['headers']:
                                st.write(f"- {header}")
            else:
                st.warning("Please enter a question about the content.")

if __name__ == "__main__":
    main()
