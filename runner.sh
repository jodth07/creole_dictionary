##rm -rf node_modules package-lock.json
#npm install
#npm install -D tailwindcss postcss autoprefixer
#npx tailwindcss init -p
#




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