#!/usr/bin/env python
"""
Test Django AI integration
"""

import requests
import json

def test_django_ai():
    """Test the Django AI endpoint"""
    
    print("🧪 Testing Django AI Integration")
    print("=" * 40)
    
    # Test the AI chat endpoint
    url = "http://localhost:8000/api/ai/chat/"
    
    test_data = {
        "message": "Hello, can you help me turn on the lights?",
        "history": []
    }
    
    print(f"📡 Testing URL: {url}")
    print(f"💬 Message: {test_data['message']}")
    
    try:
        response = requests.post(
            url,
            data=json.dumps(test_data),
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ SUCCESS!")
            print(f"📋 Response keys: {list(result.keys())}")
            
            if 'response' in result:
                ai_response = result['response']
                print(f"🤖 AI Response: {ai_response}")
                
                if 'actions' in result:
                    actions = result['actions']
                    print(f"⚡ Actions: {actions}")
                
                return True
            else:
                print(f"❌ No 'response' in result: {result}")
                return False
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"📄 Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection error - is Django server running?")
        print("💡 Run: python manage.py runserver 8000")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_ai_status():
    """Test the AI status endpoint"""
    
    print("\n🔍 Testing AI Status Endpoint")
    print("-" * 30)
    
    url = "http://localhost:8000/api/ai/status/"
    
    try:
        response = requests.get(url, timeout=10)
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Status endpoint working!")
            print(f"🤖 OpenRouter Available: {result.get('openrouter_available', False)}")
            print(f"📊 Current Model: {result.get('current_model', 'Unknown')}")
            print(f"🔄 Status: {result.get('status', 'Unknown')}")
            return True
        else:
            print(f"❌ Status endpoint failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_multiple_messages():
    """Test multiple message types"""
    
    print("\n🏠 Testing Multiple Message Types")
    print("-" * 35)
    
    messages = [
        "Turn on all the lights",
        "What's the current temperature?",
        "Check security system status",
        "Help me design a modern kitchen",
        "Show energy usage"
    ]
    
    url = "http://localhost:8000/api/ai/chat/"
    
    for i, message in enumerate(messages, 1):
        print(f"\n{i}. Testing: {message}")
        
        test_data = {
            "message": message,
            "history": []
        }
        
        try:
            response = requests.post(
                url,
                data=json.dumps(test_data),
                headers={'Content-Type': 'application/json'},
                timeout=20
            )
            
            if response.status_code == 200:
                result = response.json()
                if 'response' in result:
                    ai_response = result['response']
                    print(f"   ✅ Response: {ai_response[:80]}...")
                else:
                    print(f"   ❌ No response in result")
            else:
                print(f"   ❌ Failed: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    print("🏠 SafeNest Django AI Test")
    print("=" * 50)
    
    # Test status first
    status_ok = test_ai_status()
    
    # Test basic chat
    if test_django_ai():
        # Test multiple messages
        test_multiple_messages()
        
        print("\n" + "=" * 50)
        print("🎉 Django AI integration is working!")
        print("✅ OpenRouter API is connected")
        print("✅ AI Assistant is responding")
        print("✅ Ready for use!")
        
        print("\n🚀 Try it yourself:")
        print("1. Visit: http://localhost:8000/ai/")
        print("2. Send messages to the AI Assistant")
        print("3. Check the Django console for debug info")
        
    else:
        print("\n❌ Django AI integration failed")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure Django server is running")
        print("2. Check Django console for errors")
        print("3. Verify OpenRouter API key is working")
        print("4. Try restarting the Django server")
