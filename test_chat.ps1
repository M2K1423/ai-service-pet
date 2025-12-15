# Test AI Chat API với các kịch bản khác nhau

Write-Host "=== Testing AI Communication Service ===" -ForegroundColor Green

# Test 1: Sales Agent
Write-Host "`n1. Testing Sales Agent..." -ForegroundColor Yellow
$body1 = @{
    message = "Tôi muốn mua điện thoại iPhone 15, giá bao nhiêu?"
    user_id = "user123"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/v1/chat" `
    -Method Post `
    -Headers @{"X-API-Key"="test-key-123"; "Content-Type"="application/json"} `
    -Body $body1

# Test 2: Customer Service Agent
Write-Host "`n2. Testing Customer Service Agent..." -ForegroundColor Yellow
$body2 = @{
    message = "Tôi muốn đổi trả sản phẩm đã mua"
    user_id = "user456"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/v1/chat" `
    -Method Post `
    -Headers @{"X-API-Key"="test-key-123"; "Content-Type"="application/json"} `
    -Body $body2

# Test 3: Technical Support Agent
Write-Host "`n3. Testing Technical Support Agent..." -ForegroundColor Yellow
$body3 = @{
    message = "Điện thoại của tôi bị lỗi không bật được máy"
    user_id = "user789"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/v1/chat" `
    -Method Post `
    -Headers @{"X-API-Key"="test-key-123"; "Content-Type"="application/json"} `
    -Body $body3

Write-Host "`n=== All tests completed ===" -ForegroundColor Green
