#!/usr/bin/env python
"""
Debug OpenRouter API issues
"""

import requests
import json
import time

def test_api_key():
    """Test the API key with detailed debugging"""
    
    print("🔍 OpenRouter API Debug Test")
    print("=" * 40)
    
    # API key from your .env
    api_key = "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"
    
    print(f"🔑 Testing API Key: ***{api_key[-8:]}")
    
    # Test 1: Check if API key is valid with models endpoint
    print("\n📋 Test 1: Checking API Key Validity")
    print("-" * 35)
    
    models_url = "https://openrouter.ai/api/v1/models"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        print("📡 Requesting models list...")
        response = requests.get(models_url, headers=headers, timeout=10)
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ API Key is VALID!")
            models_data = response.json()
            print(f"📊 Available models: {len(models_data.get('data', []))}")
        elif response.status_code == 401:
            print("❌ API Key is INVALID!")
            print(f"📄 Error: {response.text}")
            return False
        else:
            print(f"⚠️  Unexpected status: {response.status_code}")
            print(f"📄 Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error checking API key: {e}")
        return False
    
    # Test 2: Try different models
    print("\n🤖 Test 2: Testing Different Models")
    print("-" * 35)
    
    models_to_test = [
        "z-ai/glm-4.5-air:free",
        "meta-llama/llama-3.1-8b-instruct:free",
        "anthropic/claude-3-haiku",
        "openai/gpt-3.5-turbo"
    ]
    
    chat_url = "https://openrouter.ai/api/v1/chat/completions"
    
    for model in models_to_test:
        print(f"\n🧪 Testing: {model}")
        
        payload = {
            "model": model,
            "messages": [
                {"role": "user", "content": "Say 'Hello' if you can hear me"}
            ],
            "max_tokens": 20,
            "temperature": 0.7
        }
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8000",
            "X-Title": "SafeNest AI Assistant"
        }
        
        try:
            response = requests.post(chat_url, headers=headers, json=payload, timeout=15)
            
            if response.status_code == 200:
                result = response.json()
                if 'choices' in result and result['choices']:
                    ai_response = result['choices'][0]['message']['content']
                    print(f"   ✅ SUCCESS: {ai_response}")
                else:
                    print(f"   ❌ No choices: {result}")
            else:
                print(f"   ❌ Failed ({response.status_code}): {response.text[:100]}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # Test 3: Detailed GLM test
    print("\n🎯 Test 3: Detailed GLM-4.5-air Test")
    print("-" * 40)
    
    payload = {
        "model": "z-ai/glm-4.5-air:free",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful AI assistant."
            },
            {
                "role": "user",
                "content": "Hello! Please respond with exactly: 'SafeNest AI test successful'"
            }
        ],
        "max_tokens": 50,
        "temperature": 0.1,
        "top_p": 1.0
    }
    
    print(f"📡 Sending detailed request...")
    print(f"🤖 Model: {payload['model']}")
    print(f"💬 Message: {payload['messages'][1]['content']}")
    
    try:
        start_time = time.time()
        response = requests.post(chat_url, headers=headers, json=payload, timeout=30)
        end_time = time.time()
        
        print(f"⏱️  Response time: {end_time - start_time:.2f}s")
        print(f"📊 Status: {response.status_code}")
        print(f"📏 Response size: {len(response.content)} bytes")
        
        if response.status_code == 200:
            result = response.json()
            print(f"📋 Response structure: {list(result.keys())}")
            
            if 'choices' in result and result['choices']:
                choice = result['choices'][0]
                print(f"📝 Choice structure: {list(choice.keys())}")
                
                if 'message' in choice:
                    message = choice['message']
                    print(f"💬 Message structure: {list(message.keys())}")
                    
                    if 'content' in message:
                        ai_response = message['content']
                        print(f"✅ FINAL RESPONSE: '{ai_response}'")
                        return True
                    else:
                        print("❌ No 'content' in message")
                else:
                    print("❌ No 'message' in choice")
            else:
                print("❌ No 'choices' in result")
                print(f"📄 Full response: {result}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"📄 Error details: {response.text}")
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out (30s)")
    except requests.exceptions.ConnectionError:
        print("❌ Connection error")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    
    return False

if __name__ == "__main__":
    print("🏠 SafeNest OpenRouter Debug Tool")
    print("=" * 50)
    
    success = test_api_key()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 OpenRouter API is working!")
        print("✅ GLM-4.5-air model is accessible")
        print("✅ Ready for SafeNest integration")
        print("\n🚀 Next steps:")
        print("1. Restart your Django server")
        print("2. Visit http://localhost:8000/ai/")
        print("3. Test the AI Assistant")
    else:
        print("❌ OpenRouter API test failed")
        print("\n🔧 Possible solutions:")
        print("1. Check your internet connection")
        print("2. Verify API key is correct and active")
        print("3. Try a different model")
        print("4. Check OpenRouter status page")
        print("5. Contact OpenRouter support if issues persist")
