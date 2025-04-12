# From project root
# Run project locally, and use for testing and development
docker build -t creole-chatbot .
docker run -p 8000:8000 creole-chatbot
