# Simple curl commands for testing

# Test 1: Sales Agent - Product inquiry
curl -X POST "http://localhost:8000/api/v1/chat" ^
  -H "Content-Type: application/json" ^
  -H "X-API-Key: test-key-123" ^
  -d "{\"message\": \"Toi muon mua dien thoai iPhone 15\", \"user_id\": \"user123\"}"

# Test 2: Customer Service - Complaint
curl -X POST "http://localhost:8000/api/v1/chat" ^
  -H "Content-Type: application/json" ^
  -H "X-API-Key: test-key-123" ^
  -d "{\"message\": \"Toi muon doi tra san pham\", \"user_id\": \"user456\"}"

# Test 3: Technical Support
curl -X POST "http://localhost:8000/api/v1/chat" ^
  -H "Content-Type: application/json" ^
  -H "X-API-Key: test-key-123" ^
  -d "{\"message\": \"Dien thoai bi loi khong bat duoc may\", \"user_id\": \"user789\"}"

# Test 4: Health check
curl http://localhost:8000/api/v1/health
