# ============ Stage 1: Build Frontend ============
FROM node:20 AS frontend-builder

WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend ./
RUN npm run build

# ============ Stage 2: Build Backend ============
FROM python:3.11-slim AS backend

# Install dependencies
WORKDIR /app
COPY requirements.txt .
COPY resources/haitian_creole_monolingual_dictionary.json ./resources/
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend ./backend

# Copy frontend build output
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# Expose port and run server
WORKDIR /app/backend
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
