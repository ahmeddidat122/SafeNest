#!/usr/bin/env python
"""
Quick test for GLM-4.5-air model
"""

import os
import requests
import json
from pathlib import Path

def test_glm_model():
    """Test GLM-4.5-air model specifically"""
    
    print("🤖 Testing GLM-4.5-air Model")
    print("=" * 35)
    
    # Load environment variables
    env_file = Path('.env')
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value
    
    # Get API key
    api_key = os.getenv('OPENROUTER_API_KEY')
    
    if not api_key:
        print("❌ No API key found!")
        print("📝 Please add OPENROUTER_API_KEY to your .env file")
        return False
    
    print(f"✅ API Key: ***{api_key[-4:]}")
    
    # Test GLM-4.5-air model
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8000",
        "X-Title": "SafeNest AI Assistant"
    }
    
    # Test with SafeNest-specific prompt
    payload = {
        "model": "z-ai/glm-4.5-air:free",
        "messages": [
            {
                "role": "system",
                "content": "You are SafeNest AI Assistant, a smart home and architecture expert."
            },
            {
                "role": "user", 
                "content": "Hello! I'm testing the SafeNest AI assistant. Can you help me control my smart home lights?"
            }
        ],
        "max_tokens": 200,
        "temperature": 0.7
    }
    
    try:
        print(f"\n📡 Testing model: {payload['model']}")
        print(f"💬 Test message: Smart home lights control")
        
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            ai_response = result['choices'][0]['message']['content']
            print(f"✅ SUCCESS!")
            print(f"🤖 GLM Response: {ai_response}")
            print(f"📏 Response length: {len(ai_response)} characters")
            return True
        else:
            print(f"❌ FAILED! Status: {response.status_code}")
            print(f"📄 Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_smart_home_scenarios():
    """Test GLM model with smart home scenarios"""
    
    api_key = os.getenv('OPENROUTER_API_KEY')
    if not api_key:
        return
    
    print("\n🏠 Testing Smart Home Scenarios")
    print("-" * 32)
    
    scenarios = [
        "Turn on all the lights in the living room",
        "What's the current temperature in my house?",
        "Check the security system status",
        "Help me design a modern kitchen layout",
        "How can I optimize my home's energy usage?"
    ]
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8000",
        "X-Title": "SafeNest AI Assistant"
    }
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n🧪 Test {i}: {scenario}")
        
        payload = {
            "model": "z-ai/glm-4.5-air:free",
            "messages": [
                {
                    "role": "system",
                    "content": "You are SafeNest AI Assistant. Help with smart home control and architecture. Be concise and helpful."
                },
                {
                    "role": "user", 
                    "content": scenario
                }
            ],
            "max_tokens": 150,
            "temperature": 0.7
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=20)
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result['choices'][0]['message']['content']
                print(f"   ✅ Response: {ai_response[:100]}...")
            else:
                print(f"   ❌ Failed: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    print("🏠 SafeNest GLM-4.5-air Model Test")
    print("=" * 50)
    
    if test_glm_model():
        test_smart_home_scenarios()
        
        print("\n" + "=" * 50)
        print("🎉 GLM-4.5-air model is working!")
        print("💡 Benefits of using GLM-4.5-air:")
        print("   • Completely FREE to use")
        print("   • Good performance for smart home tasks")
        print("   • No usage limits or costs")
        print("   • Perfect for SafeNest development")
        print("\n🚀 Your SafeNest AI Assistant is ready!")
        print("   Visit: http://localhost:8000/ai/")
    else:
        print("\n❌ GLM-4.5-air model test failed")
        print("🔧 Troubleshooting:")
        print("   1. Check your API key is valid")
        print("   2. Verify internet connection")
        print("   3. Try running: python debug_openrouter.py")
