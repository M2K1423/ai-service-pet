"""
Khởi động AgentOS với Web UI
Chạy: python start_server.py
"""
import uvicorn
from src.config.settings import settings

if __name__ == "__main__":
    print("=" * 80)
    print("🚀 STARTING AGNO AGENT OS")
    print("=" * 80)
    print(f"🌐 Server: http://localhost:8000")
    print(f"📊 API Docs: http://localhost:8000/docs")
    print(f"🔗 Store API: {settings.STORE_API_BASE_URL}")
    print()
    print("🎨 ĐỂ MỞ WEB UI:")
    print("   1. Vào: https://os.agno.com")
    print("   2. Click 'Connect your AgentOS'")
    print("   3. Chọn 'Local'")
    print("   4. Nhập: http://localhost:8000")
    print("   5. Click 'CONNECT'")
    print("=" * 80)
    
    uvicorn.run(
        "src.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
