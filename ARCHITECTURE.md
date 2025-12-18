# Agno AI Agent System - Architecture & Setup

## 🏗️ Kiến trúc hệ thống (theo sơ đồ)

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│   Zalo      │────(1)──▶│             │────(2)──▶│  AI Agent   │────(3)──▶│  Store API  │
│  Messenger  │         │ CRA Backend │         │   (Agno)    │         │  (Backend)  │
└─────────────┘◀───(7)──┘             │◀───(5)──┘             │◀───(4)──┘             │
                         │             │         │ Python proj │         │ /odeli/xxx  │
                         └─────────────┘         └─────────────┘         └─────────────┘
                               │                                                  
                               │(6)                                               
                               ▼                                                  
                         ┌─────────────┐                                          
                         │  MongoDB    │                                          
                         └─────────────┘                                          
```

### Flow hoạt động:
1. **User** gửi tin nhắn qua **Zalo/Messenger**
2. **CRA Backend** nhận webhook từ platforms
3. **CRA Backend** gửi request tới **AI Agent** (project này)
4. **AI Agent** sử dụng **Tools** để gọi **Store API**
5. **Store API** trả dữ liệu về **AI Agent**
6. **AI Agent** xử lý và trả response về **CRA Backend**
7. **CRA Backend** reply lại **User** qua platform

---

## 📁 Cấu trúc thư mục mới (đã tái cấu trúc)

```
agno_python/
├── src/
│   ├── __init__.py
│   │
│   ├── config/                    # Configuration
│   │   ├── __init__.py
│   │   └── settings.py            # ⭐ API URLs, configs
│   │
│   ├── core/                      # Core business logic
│   │   ├── __init__.py
│   │   ├── agents.py              # ⭐ Agent definitions với tools
│   │   └── models.py              # ⭐ Pydantic models (Request/Response)
│   │
│   ├── integrations/              # External integrations
│   │   ├── __init__.py
│   │   └── tools.py               # ⭐ Tools gọi Store API
│   │
│   └── api/                       # API layer
│       ├── __init__.py
│       └── main.py                # ⭐ FastAPI endpoints
│
├── .env                           # Environment variables
├── .env.example                   # Template
├── requirements.txt               # Dependencies
├── Dockerfile                     # Docker build
├── README.md                      # Docs chính
├── ARCHITECTURE.md               # File này - Architecture docs
└── main.py                        # Entry point (backward compatibility)
```

---

## 🔧 Components Chi tiết

### 1. **Config Layer** (`src/config/`)

#### `settings.py`
- Quản lý toàn bộ configuration
- Store API URLs
- API Keys
- Timeout, retry settings
- Helper methods để build URLs

**Key Features:**
```python
settings.STORE_API_BASE_URL          # http://localhost:9000
settings.get_product_url(sku)        # Build product URL
settings.get_category_url()          # Build category URL
```

---

### 2. **Core Layer** (`src/core/`)

#### `models.py` 
- Pydantic models cho validation
- Request models: `ChatRequest`, `WebhookMessage`
- Response models: `ChatResponse`, `ErrorResponse`
- Internal models: `Product`, `Order`, `Customer`

#### `agents.py`
- Định nghĩa 3 agents chính
- System prompts cho mỗi agent
- Router logic (route message tới agent phù hợp)

**3 Agents:**

1. **Customer Service Agent**
   - Tools: `get_customer_info`, `get_order_status`, `create_order`
   - Xử lý: Đơn hàng, khiếu nại, hỗ trợ

2. **Sales Agent**  
   - Tools: `search_products`, `get_product_detail`, `get_all_products`, `get_categories`, `get_promotions`
   - Xử lý: Tư vấn sản phẩm, giá cả, khuyến mãi

3. **Technical Support Agent**
   - Tools: `get_customer_info`, `get_product_detail`, `get_order_status`
   - Xử lý: Hỗ trợ kỹ thuật, hướng dẫn

---

### 3. **Integrations Layer** (`src/integrations/`)

#### `tools.py` - ⭐ QUAN TRỌNG NHẤT
Chứa tất cả tools để Agent gọi Store API:

**Product Tools:**
- `search_products()` - Tìm kiếm sản phẩm với filters
- `get_product_detail(sku)` - Chi tiết 1 sản phẩm
- `get_all_products()` - Danh sách sản phẩm

**Category & Promotion Tools:**
- `get_categories()` - Danh mục sản phẩm
- `get_promotions()` - Khuyến mãi hiện tại

**Customer & Order Tools:**
- `get_customer_info(customer_id)` - Thông tin khách hàng
- `get_order_status(order_id)` - Trạng thái đơn hàng
- `create_order()` - Tạo đơn hàng mới

**Cách hoạt động:**
```python
# Agent tự động gọi tool khi cần
# User: "Tìm sản phẩm giá dưới 500k"
# → Sales Agent → search_products(max_price=500000)
# → HTTP GET http://localhost:9000/odeli/products?max_price=500000
# → Format dữ liệu → Trả về cho Agent → Agent sinh câu trả lời
```

---

### 4. **API Layer** (`src/api/`)

#### `main.py`
FastAPI application với các endpoints:

**Main Endpoints:**

1. **POST `/api/v1/chat`** - Chat endpoint chính
   ```json
   // Request từ CRA Backend
   {
     "user_id": "zalo:123456",
     "message": "Cho tôi xem sản phẩm giá rẻ",
     "session_id": "session_abc",
     "context": {}
   }
   
   // Response
   {
     "user_id": "zalo:123456",
     "message": "Em xin giới thiệu một số sản phẩm...",
     "agent_used": "Sales Agent",
     "agent_type": "sales",
     "timestamp": "2025-12-18T..."
   }
   ```

2. **POST `/api/v1/webhook`** - Alternative webhook endpoint

3. **GET `/api/v1/health`** - Health check
   ```json
   {
     "status": "healthy",
     "service": "Agno Multi-Agent System",
     "store_api": "http://localhost:9000",
     "agents": [...]
   }
   ```

4. **GET `/api/v1/agents`** - List agents và tools

---

## 🔐 Security

### API Key Authentication
- CRA Backend phải gửi header: `X-API-Key: <your-key>`
- Keys được config trong `.env`: `API_KEYS=key1,key2,key3`

### CORS
- Đã enable CORS cho CRA Backend có thể gọi
- Production nên restrict origins

---

## 🚀 Deployment

### Local Development
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Setup .env
cp .env.example .env
# Edit .env với Store API URL

# 3. Run
python -m src.api.main
# hoặc
uvicorn src.api.main:app --reload
```

### Docker
```bash
# Build
docker build -t agno-agent .

# Run
docker run -p 8000:8000 --env-file .env agno-agent
```

---

## 📊 Testing

### Test với curl
```bash
# Health check
curl http://localhost:8000/api/v1/health

# Chat request
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: test-key-123" \
  -d '{
    "user_id": "test_user",
    "message": "Cho tôi xem sản phẩm"
  }'
```

### Test Store API connection
Tools sẽ tự động log khi gọi Store API:
```
🔍 [TOOL] search_products called
   URL: http://localhost:9000/odeli/products
   Params: {'limit': 10, 'sort': 'price'}
   ✅ Response: 200
   📦 Items count: 25
```

---

## 🎯 Luồng xử lý chi tiết

### Example: User hỏi về sản phẩm

1. **User** (Zalo): "Cho tôi xem sản phẩm giá rẻ"

2. **CRA Backend** nhận webhook, gửi tới AI Agent:
   ```http
   POST /api/v1/chat
   X-API-Key: abc123
   
   {
     "user_id": "zalo:123",
     "message": "Cho tôi xem sản phẩm giá rẻ"
   }
   ```

3. **AI Agent** (`main.py`):
   - Validate API key ✓
   - Route message → **Sales Agent** (có keyword "sản phẩm", "giá rẻ")
   
4. **Sales Agent** (`agents.py`):
   - Phân tích message
   - Quyết định dùng tool: `search_products()`
   - Agent tự động gọi tool

5. **Tool** (`tools.py`):
   ```python
   search_products(
       query="",
       limit=10,
       sort_by="price",
       order="ASC",
       max_price=500000
   )
   ```
   - HTTP GET → `http://localhost:9000/odeli/products?sort=price&order=ASC&max_price=500000`

6. **Store API** trả về JSON:
   ```json
   {
     "items": [
       {"sku": "ABC", "name": "Sản phẩm A", "price": 250000},
       {"sku": "DEF", "name": "Sản phẩm B", "price": 350000},
       ...
     ]
   }
   ```

7. **Tool** format data và return về Agent

8. **Sales Agent** nhận data, sinh câu trả lời tự nhiên:
   ```
   Dạ, em xin giới thiệu một số sản phẩm giá tốt ạ:
   
   1. Sản phẩm A - 250,000đ
   2. Sản phẩm B - 350,000đ
   ...
   ```

9. **AI Agent** return response về **CRA Backend**

10. **CRA Backend** reply qua Zalo cho **User**

---

## 🔄 Mở rộng

### Thêm tool mới
1. Định nghĩa function trong `tools.py`
2. Add vào agent trong `agents.py`
3. Agent tự động biết khi nào dùng tool

### Thêm agent mới
1. Tạo agent trong `agents.py`
2. Add vào `agent_os` trong `main.py`
3. Update router keywords

### Thêm endpoint mới
1. Add endpoint trong `main.py`
2. Define model trong `models.py`

---

## 📞 Support

- Store API Backend: `http://localhost:9000`
- AI Agent API: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`

---

**Tóm tắt:** 
- ✅ Agents sử dụng Tools để gọi Store API
- ✅ CRA Backend gọi AI Agent qua REST API
- ✅ Tự động routing message tới agent phù hợp
- ✅ Clean architecture, dễ mở rộng
