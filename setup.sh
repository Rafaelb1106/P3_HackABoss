mkdir -p ~/.streamlit/

echo "\
[browser]\n\
backend = \"playwright\"\n\
browser = \"chromium\"\n\
chromiumExecutable = \"$(playwright-ffmpeg --print-chromium-executable)\"\n\
" > ~/.streamlit/config.toml

playwright install chromium
