#!/usr/bin/env python
"""
Simple OpenRouter API test without Django
"""

import requests
import json

def test_openrouter():
    """Test OpenRouter API directly"""
    
    print("🧪 Simple OpenRouter Test")
    print("=" * 30)
    
    # Your API key from .env file
    api_key = "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"
    
    print(f"🔑 API Key: ***{api_key[-4:]}")
    
    # Test URL and headers
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8000",
        "X-Title": "SafeNest AI Assistant"
    }
    
    # Simple test payload
    payload = {
        "model": "z-ai/glm-4.5-air:free",
        "messages": [
            {
                "role": "user",
                "content": "Hello! Say 'Test successful' if you can hear me."
            }
        ],
        "max_tokens": 50,
        "temperature": 0.7
    }
    
    print(f"🤖 Testing model: {payload['model']}")
    print(f"💬 Message: {payload['messages'][0]['content']}")
    
    try:
        print("\n📡 Sending request...")
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ SUCCESS!")
            
            if 'choices' in result and result['choices']:
                ai_response = result['choices'][0]['message']['content']
                print(f"🤖 AI Response: {ai_response}")
                return True
            else:
                print(f"❌ No choices in response")
                print(f"📄 Full response: {result}")
                return False
        else:
            print(f"❌ FAILED!")
            print(f"📄 Error: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Connection error")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_different_messages():
    """Test with different message types"""
    
    api_key = "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"
    
    print("\n🏠 Testing Smart Home Messages")
    print("-" * 35)
    
    messages = [
        "Turn on the lights",
        "What's the temperature?",
        "Check security status"
    ]
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8000",
        "X-Title": "SafeNest AI Assistant"
    }
    
    for i, msg in enumerate(messages, 1):
        print(f"\n{i}. Testing: {msg}")
        
        payload = {
            "model": "z-ai/glm-4.5-air:free",
            "messages": [
                {
                    "role": "system",
                    "content": "You are SafeNest AI Assistant for smart home control."
                },
                {
                    "role": "user",
                    "content": msg
                }
            ],
            "max_tokens": 100,
            "temperature": 0.7
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=20)
            
            if response.status_code == 200:
                result = response.json()
                if 'choices' in result and result['choices']:
                    ai_response = result['choices'][0]['message']['content']
                    print(f"   ✅ Response: {ai_response[:80]}...")
                else:
                    print(f"   ❌ No response")
            else:
                print(f"   ❌ Failed: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    print("🏠 SafeNest OpenRouter Simple Test")
    print("=" * 50)
    
    if test_openrouter():
        test_different_messages()
        print("\n🎉 OpenRouter is working!")
        print("✅ Your API key is valid")
        print("✅ GLM-4.5-air model is accessible")
        print("✅ Ready for SafeNest integration")
    else:
        print("\n❌ OpenRouter test failed")
        print("\n🔧 Troubleshooting steps:")
        print("1. Check your internet connection")
        print("2. Verify API key is correct")
        print("3. Try a different model")
        print("4. Check OpenRouter status page")
    
    print(f"\n📝 Next steps:")
    print("1. If this test works, restart your Django server")
    print("2. Visit http://localhost:8000/ai/ to test in SafeNest")
    print("3. Check Django console for debug messages")
