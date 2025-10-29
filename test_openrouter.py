#!/usr/bin/env python
"""
Test script for OpenRouter AI integration
Run this script to test the OpenRouter API connection
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'safenest.settings')
django.setup()

from api.views import AIChatView
import json

def test_openrouter_integration():
    """Test OpenRouter API integration"""
    
    print("🤖 Testing SafeNest OpenRouter AI Integration")
    print("=" * 50)
    
    # Create view instance
    view = AIChatView()
    
    # Test messages
    test_messages = [
        "Hello, I'm testing the AI assistant",
        "Turn on the living room lights",
        "What's the current temperature?",
        "Help me design a modern kitchen",
        "Show me the security status"
    ]
    
    print("\n📝 Testing AI Responses:")
    print("-" * 30)
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n{i}. User: {message}")
        
        try:
            # Test OpenRouter response
            response = view.get_openrouter_response(message, [])
            
            if response:
                print(f"   🟢 OpenRouter: {response[:100]}{'...' if len(response) > 100 else ''}")
            else:
                print("   🟡 OpenRouter: Not available, testing fallback...")
                fallback = view.generate_fallback_response(message.lower(), [])
                print(f"   🔄 Fallback: {fallback[:100]}{'...' if len(fallback) > 100 else ''}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 50)
    
    # Test configuration
    print("\n⚙️  Configuration Status:")
    print("-" * 25)
    
    from django.conf import settings
    
    api_key = getattr(settings, 'OPENROUTER_API_KEY', None)
    if api_key:
        print(f"   🟢 API Key: Configured (***{api_key[-4:]})")
    else:
        print("   🟡 API Key: Not configured (using fallback mode)")
    
    ai_settings = getattr(settings, 'AI_ASSISTANT_SETTINGS', {})
    print(f"   📊 Model: {ai_settings.get('DEFAULT_MODEL', 'Not set')}")
    print(f"   🎛️  Max Tokens: {ai_settings.get('MAX_TOKENS', 'Not set')}")
    print(f"   🌡️  Temperature: {ai_settings.get('TEMPERATURE', 'Not set')}")
    
    print("\n🔧 Setup Instructions:")
    print("-" * 20)
    if not api_key:
        print("   1. Get API key from: https://openrouter.ai/keys")
        print("   2. Add to .env file: OPENROUTER_API_KEY=your-key-here")
        print("   3. Restart Django server")
    else:
        print("   ✅ OpenRouter is properly configured!")
    
    print("\n📚 Documentation:")
    print("-" * 15)
    print("   📖 Setup Guide: docs/OPENROUTER_SETUP.md")
    print("   🌐 OpenRouter Docs: https://openrouter.ai/docs")
    print("   🏠 SafeNest AI: /ai/ (in your browser)")

def test_api_endpoint():
    """Test the API endpoint directly"""
    
    print("\n\n🔌 Testing API Endpoint:")
    print("-" * 25)
    
    try:
        from django.test import Client
        client = Client()
        
        # Test AI status endpoint
        response = client.get('/api/ai/status/')
        if response.status_code == 200:
            data = json.loads(response.content)
            print(f"   🟢 Status Endpoint: Working")
            print(f"   📊 OpenRouter Available: {data.get('openrouter_available', False)}")
            print(f"   🤖 Current Model: {data.get('current_model', 'Unknown')}")
        else:
            print(f"   ❌ Status Endpoint: Failed ({response.status_code})")
        
        # Test chat endpoint
        chat_data = {
            'message': 'Hello, this is a test',
            'history': []
        }
        
        response = client.post(
            '/api/ai/chat/',
            data=json.dumps(chat_data),
            content_type='application/json'
        )
        
        if response.status_code == 200:
            data = json.loads(response.content)
            print(f"   🟢 Chat Endpoint: Working")
            print(f"   💬 Response: {data.get('response', 'No response')[:50]}...")
        else:
            print(f"   ❌ Chat Endpoint: Failed ({response.status_code})")
            
    except Exception as e:
        print(f"   ❌ API Test Error: {e}")

if __name__ == "__main__":
    try:
        test_openrouter_integration()
        test_api_endpoint()
        
        print("\n" + "=" * 50)
        print("🎉 Test completed! Check the results above.")
        print("💡 Visit http://localhost:8000/ai/ to try the AI Assistant")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        print("🔧 Make sure Django is properly configured and running")
