# Agno Multi-Agent System 🤖

AI chatbot CRM với kiến trúc **Agno Framework** - đơn giản, mạnh mẽ, dễ mở rộng.

## 🏗️ Kiến trúc Agno

```
┌─────────────────────────────────────────────────────────┐
│  AgentOS (Framework Layer)                              │
│  ├─ Auto-generated FastAPI app                          │
│  ├─ Built-in API docs (/docs)                           │
│  └─ Agent orchestration                                 │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  Multi-Agent System                                     │
│  ├─ 🛎️  Customer Service Agent                          │
│  ├─ 💼 Sales Agent                                       │
│  └─ 🔧 Technical Support Agent                           │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  Custom Tools (@tool decorator)                         │
│  ├─ get_customer_info()                                 │
│  ├─ search_products()                                   │
│  ├─ get_all_products()                                  │
│  ├─ get_categories()                                    │
│  ├─ get_promotions()                                    │
│  └─ get_order_status()                                  │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  External APIs (httpx async calls)                      │
│  └─ CRM Database API (http://localhost:9000)            │
└─────────────────────────────────────────────────────────┘

**File structure:**
```

ai-service/
├── agno_refactored.py # 🎯 Main file (350 lines)
├── .env # Configuration
├── requirements.txt # 5 dependencies
└── README.md # This file

````

## ✨ Tính năng

- ✅ **3 Specialized Agents**: Customer Service, Sales, Technical Support
- ✅ **Auto Agent Routing**: Keyword-based intent detection
- ✅ **Built-in Memory**: Conversation history (10-15 messages)
- ✅ **CRM Database Integration**: Products, categories, promotions
- ✅ **Custom Tools**: @tool decorator for easy API integration
- ✅ **Auto API Docs**: Swagger UI tự động
- ✅ **Google Gemini**: Fast, free AI model

## 🚀 Quickstart (5 phút)

### 1. Install dependencies

```bash
pip install -r requirements.txt
````

### 2. Configure `.env`

```env
GOOGLE_API_KEY=your-google-api-key-here
API_KEYS=test-key-123,dev-key-456
DATABASE_API_URL=http://localhost:9000
```

### 3. Run service

```bash
python agno_refactored.py
```

🎉 Service chạy tại: http://localhost:8000

## 📖 API Endpoints

### Auto-generated (Agno)

- `GET  /docs` - Swagger UI
- `POST /agents/{agent_name}/run` - Run specific agent

### Custom endpoints

- `POST /api/v1/chat` - Smart chat with auto agent selection
- `GET  /api/v1/health` - Health check

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

**Response:**

```json
{
  "user_id": "user123",
  "message": "Chào anh/chị! Em có thể tư vấn sản phẩm cho anh/chị...",
  "agent_used": "Sales Agent",
  "agent_type": "sales"
}
```

## 🤖 Agents & Tools

### Available Agents

| Agent             | Intent Keywords                | Tools                                                             |
| ----------------- | ------------------------------ | ----------------------------------------------------------------- |
| Customer Service  | đơn hàng, giao hàng, khiếu nại | get_customer_info, get_order_status                               |
| Sales             | sản phẩm, giá, mua, rẻ, đắt    | search_products, get_all_products, get_categories, get_promotions |
| Technical Support | lỗi, bug, sự cố, hướng dẫn     | get_customer_info                                                 |

### Custom Tools

Tools được define bằng async functions và tự động integrate với agents:

```python
async def search_products(query: str = "", sort_by: str = "price") -> List[Dict]:
    """Tìm kiếm sản phẩm theo giá."""
    response = await http_client.get(f"{DATABASE_API_URL}/odeli/products")
    return response.json()
```

## 🐳 Docker

```bash
# Build
docker build -t agno-multi-agent .

# Run
docker run -d -p 8000:8000 --env-file .env agno-multi-agent
```

## 🧪 Testing

```bash
# Health check
curl http://localhost:8000/api/v1/health

# Test sales agent
curl -X POST http://localhost:8000/api/v1/chat \
  -H "X-API-Key: test-key-123" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"test","message":"sản phẩm rẻ nhất","session_id":"s1"}'

# Test customer service agent
curl -X POST http://localhost:8000/api/v1/chat \
  -H "X-API-Key: test-key-123" \
  -d '{"user_id":"test","message":"kiểm tra đơn hàng","session_id":"s1"}'
```

## 📊 Comparison: Custom vs Agno

| Aspect           | Custom (main branch)                | Agno (agno branch)    |
| ---------------- | ----------------------------------- | --------------------- |
| **Files**        | 45+ files                           | 1 file                |
| **Lines**        | ~2000                               | ~350                  |
| **Setup Time**   | 2-3 days                            | 5 minutes             |
| **Architecture** | 3-layer (Gateway-Core-Integrations) | AgentOS framework     |
| **Middleware**   | Custom (dedup, logging, rate limit) | None (basic)          |
| **AI Model**     | Ollama (local, free)                | Gemini (cloud, quota) |
| **Intent**       | Custom classifier                   | Keyword routing       |
| **Memory**       | SessionManager                      | Built-in (10-15 msgs) |
| **Control**      | Full control                        | Framework-based       |
| **Maintenance**  | Custom code                         | Framework updates     |

**Trade-offs:**

- ✅ Agno: Nhanh, đơn giản, ít code
- ❌ Agno: Mất control, mất Ollama, mất custom middleware
- ✅ Custom: Full control, Ollama local, production features
- ❌ Custom: Nhiều code, setup lâu, maintain phức tạp

## 🔄 Migration Guide

Xem [MIGRATION.md](MIGRATION.md) để biết chi tiết migrate từ custom architecture sang Agno.

**Quick summary:**

1. Backup: `git checkout -b backup-custom`
2. Create `agno_refactored.py` (1 file)
3. Delete: gateway/, core/, integrations/, shared/, main.py
4. Update: requirements.txt, .env, Dockerfile
5. Test: python agno_refactored.py

## 📄 License

MIT License

## 📧 Contact

GitHub: [your-username]
Email: your-email@example.com
