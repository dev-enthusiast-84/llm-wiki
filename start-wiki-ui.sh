#bash
python3 -c "import streamlit, litellm" 2>&1 | grep -q "No module named 'streamlit'" && echo "Streamlit is not installed. Please install it using 'pip install streamlit'." && exit 1
streamlit run wiki_query.py