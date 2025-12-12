# Agno Agent với MongoDB

## Cài đặt

```bash
pip install -r requirements.txt
```

## Cấu hình

Chỉnh sửa file `.env`:
- Thêm GOOGLE_API_KEY
- Cấu hình MongoDB URL (mặc định: localhost:27017)

## Chạy

```bash
fastapi dev agno_agent.py
```

Mở http://localhost:8000/docs để xem API

