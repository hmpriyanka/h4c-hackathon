pip install -r requirements.txt
uvicorn main:app --reload
go to https://platform.openai.com/account/api-keys
craete openai key
create a .env with OPENAI_API_KEY=dummykey

curl -fsSL https://ollama.com/install.sh | sh
ollama --version
ollama pull llama2
ollama list