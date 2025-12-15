# AI Communication Service 🤖

Dịch vụ AI chatbot đa kênh với kiến trúc 3 tầng (Gateway - Core - Integrations) để xử lý tin nhắn từ CRM và các kênh truyền thông.

## 🏗️ Kiến trúc

```
ai-service/
│
├── 🚪 gateway/                  # Layer 1: API Gateway
│   ├── app.py                  # FastAPI application
│   ├── routes/                 # API endpoints
│   ├── middleware/             # Auth, rate limit, logging
│   ├── schemas/                # Request/Response models
│   └── utils/                  # Validators
│
├── 🧠 core/                     # Layer 2: Business Logic
│   ├── agent_manager.py        # Quản lý agents
│   ├── agents/                 # AI agents
│   ├── processors/             # Message processing
│   ├── memory/                 # Conversation memory
│   └── config/                 # Settings & prompts
│
├── 🔌 integrations/             # Layer 3: External APIs
│   ├── database_api/           # Database endpoints
│   ├── ai_models/              # OpenAI, Claude, Gemini
│   └── external_services/      # Zalo, Facebook APIs
│
├── 🔧 shared/                   # Shared utilities
│   ├── exceptions.py
│   ├── logger.py
│   └── constants.py
│
├── 📊 data/                     # Runtime data
│   └── conversations.db
│
├── 🧪 tests/                    # Unit tests
│
└── main.py                      # Entry point
```

## ✨ Tính năng

- ✅ **Multi-Agent System**: Customer Service, Sales, Technical Support
- ✅ **Intent Classification**: Tự động phân loại ý định khách hàng
- ✅ **Conversation Memory**: Lưu trữ lịch sử hội thoại
- ✅ **Multi-Channel**: Zalo, Facebook Messenger
- ✅ **API Gateway**: Auth, rate limiting, logging
- ✅ **Flexible AI Models**: Gemini (free), OpenAI, Claude

## 🚀 Cài đặt

### 1. Clone và cài đặt dependencies

```bash
pip install -r requirements.txt
```

### 2. Cấu hình môi trường

Tạo file `.env` từ template:

```bash
cp .env.example .env
```

Chỉnh sửa `.env` với các thông tin cần thiết:

```env
# Bắt buộc
GOOGLE_API_KEY=your-google-api-key-here
API_KEYS=your-api-key-1,your-api-key-2

# Tùy chọn
MONGODB_URL=mongodb://localhost:27017
OPENAI_API_KEY=your-openai-key (optional)
ANTHROPIC_API_KEY=your-claude-key (optional)
```

### 3. Chạy ứng dụng

```bash
python main.py
```

Hoặc với uvicorn:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 📖 API Documentation

Sau khi chạy ứng dụng, truy cập:

- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/v1/health

## 🔐 API Usage

### Chat Endpoint

```bash
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_123",
    "message": "Tôi muốn tư vấn sản phẩm",
    "context": {
      "customer_name": "Nguyễn Văn A"
    }
  }'
```

### Response

```json
{
  "user_id": "user_123",
  "message": "Chào anh/chị! Em có thể tư vấn sản phẩm cho anh/chị...",
  "agent_type": "sales_agent",
  "metadata": {
    "intent": "product_inquiry",
    "confidence": 0.95
  },
  "timestamp": "2025-12-14T10:30:00"
}
```

## 🐳 Docker

### Build image

```bash
docker build -t ai-service:latest .
```

### Run container

```bash
docker run -d \
  -p 8000:8000 \
  --env-file .env \
  --name ai-service \
  ai-service:latest
```

## 🧪 Testing

```bash
# Chạy tất cả tests
pytest

# Với coverage
pytest --cov=. --cov-report=html

# Chạy test cụ thể
pytest tests/test_gateway/test_chat.py
```

## 📝 Development

### Code formatting

```bash
black .
```

### Linting

```bash
flake8 .
```

### Type checking

```bash
mypy .
```

## 🤝 Contributing

1. Fork repository
2. Tạo feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Tạo Pull Request

## 📄 License

MIT License

## 📧 Contact

Email: your-email@example.com
