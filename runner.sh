##rm -rf node_modules package-lock.json
#npm install
#npm install -D tailwindcss postcss autoprefixer
#npx tailwindcss init -p
#


# From project root
docker build -t creole-chatbot .
docker run -p 8000:8000 creole-chatbot



# curl --request GET  \
#     --url 'http://0.0.0.0:8000/api/hello/world'
#
#
echo
echo
curl -X 'POST' \
  'http://127.0.0.1:8000/api/chat' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "message": "pen"
}'