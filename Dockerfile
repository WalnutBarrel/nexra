FROM python:3.11-slim as backend

WORKDIR /app
COPY ./api /app/api
# In a real environment, we'd copy requirements.txt and pip install
# RUN pip install -r requirements.txt

ENV PYTHONPATH=/app
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]

# ---

FROM node:20-alpine as frontend

WORKDIR /app
COPY ./package.json ./package-lock.json ./
# RUN npm ci

COPY ./src ./src
COPY ./public ./public
COPY ./next.config.ts ./postcss.config.mjs ./tailwind.config.ts ./tsconfig.json ./

# RUN npm run build
CMD ["npm", "start"]
