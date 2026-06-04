"""Script to test the PetDiagnosisAgent."""
import asyncio
import os
import sys

# Add communication-ai path to python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.agents.pet_diagnosis_agent import PetDiagnosisAgent


async def main():
    print("🐾 Initializing PetDiagnosisAgent...")
    agent = PetDiagnosisAgent()
    
    print("\n--- TEST CASE 1: Parvovirus symptoms ---")
    query1 = "Chó nhà em bị nôn mửa liên tục ra bọt vàng, đi ngoài ra máu có mùi tanh hôi lắm bác sĩ ơi, bé bỏ ăn lờ đờ nằm một góc. Bé bị làm sao ạ?"
    context1 = {
        "customer_name": "Nguyễn Văn A",
        "phone": "0987654321"
    }
    history1 = []
    
    print(f"User: {query1}")
    print("Generating AI response...")
    response1 = await agent.generate_response(query1, context1, history1)
    print("\nAI:")
    print(response1)
    
    print("\n--- TEST CASE 2: Cat panleukopenia symptoms ---")
    query2 = "Mèo con nhà em sốt cao rồi tự nhiên hạ thân nhiệt nằm gục bên bát nước mà không uống, đi ngoài tiêu chảy lỏng tanh lắm. Có cách nào sơ cứu tại nhà không bác sĩ?"
    context2 = {
        "customer_name": "Trần Thị B",
        "phone": "0912345678"
    }
    history2 = [
        {"role": "user", "content": "Chào bác sĩ thú y"},
        {"role": "assistant", "content": "Chào anh/chị Trần Thị B, tôi là Bác sĩ Thú y Ảo PetCare. Tôi có thể giúp gì cho sức khỏe thú cưng của bạn?"}
    ]
    
    print(f"User: {query2}")
    print("Generating AI response...")
    response2 = await agent.generate_response(query2, context2, history2)
    print("\nAI:")
    print(response2)


if __name__ == "__main__":
    asyncio.run(main())
