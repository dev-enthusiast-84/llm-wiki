#bash
pgrep -fl "streamlit run wiki_query.py"
echo "Stopping the Streamlit wiki UI..."
pkill -f "streamlit run wiki_query.py"
pgrep -fl "streamlit run wiki_query.py"
echo "Streamlit wiki UI stopped."