#!/usr/bin/env python
"""
Debug script for OpenRouter API issues
This script tests the OpenRouter API directly to identify problems
"""

import os
import requests
import json
from pathlib import Path

def test_openrouter_api():
    """Test OpenRouter API directly"""
    
    print("🔍 OpenRouter API Debug Test")
    print("=" * 40)
    
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
        print("🔗 Get your key from: https://openrouter.ai/keys")
        return False
    
    print(f"✅ API Key found: ***{api_key[-4:]}")
    
    # Test 1: Simple API call
    print("\n🧪 Test 1: Basic API Call")
    print("-" * 25)
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8000",
        "X-Title": "SafeNest AI Assistant"
    }
    
    # Simple test payload with GLM-4.5-air
    payload = {
        "model": "z-ai/glm-4.5-air:free",
        "messages": [
            {
                "role": "user",
                "content": "Hello, please respond with 'API test successful'"
            }
        ],
        "max_tokens": 50,
        "temperature": 0.7
    }
    
    try:
        print(f"📡 Sending request to: {url}")
        print(f"🤖 Model: {payload['model']}")
        print(f"💬 Message: {payload['messages'][0]['content']}")
        
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"⏱️  Response Time: {response.elapsed.total_seconds():.2f}s")
        
        if response.status_code == 200:
            result = response.json()
            ai_response = result['choices'][0]['message']['content']
            print(f"✅ Success! Response: {ai_response}")
            return True
        else:
            print(f"❌ Failed! Status: {response.status_code}")
            print(f"📄 Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out (30s)")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Connection error - check internet connection")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_different_models():
    """Test different models to see which ones work"""
    
    print("\n🧪 Test 2: Model Availability")
    print("-" * 30)
    
    api_key = os.getenv('OPENROUTER_API_KEY')
    if not api_key:
        return
    
    models_to_test = [
        "z-ai/glm-4.5-air:free",  # Primary free model
        "meta-llama/llama-3.1-8b-instruct:free",  # Backup free model
        "anthropic/claude-3-haiku",
        "openai/gpt-3.5-turbo",
        "anthropic/claude-3.5-sonnet"
    ]
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8000",
        "X-Title": "SafeNest AI Assistant"
    }
    
    for model in models_to_test:
        print(f"\n🤖 Testing model: {model}")
        
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": "Hi"}],
            "max_tokens": 20,
            "temperature": 0.7
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=15)
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result['choices'][0]['message']['content']
                print(f"   ✅ Works! Response: {ai_response[:30]}...")
            else:
                print(f"   ❌ Failed: {response.status_code} - {response.text[:100]}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")

def test_api_key_validity():
    """Test if the API key is valid"""
    
    print("\n🧪 Test 3: API Key Validation")
    print("-" * 30)
    
    api_key = os.getenv('OPENROUTER_API_KEY')
    if not api_key:
        return
    
    # Test with models endpoint
    url = "https://openrouter.ai/api/v1/models"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            models = response.json()
            print(f"✅ API key is valid!")
            print(f"📊 Available models: {len(models.get('data', []))}")
        elif response.status_code == 401:
            print("❌ API key is invalid or expired")
            print("🔗 Get a new key from: https://openrouter.ai/keys")
        else:
            print(f"❌ Unexpected response: {response.status_code}")
            print(f"📄 Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error testing API key: {e}")

def check_common_issues():
    """Check for common configuration issues"""
    
    print("\n🔧 Common Issues Check")
    print("-" * 22)
    
    # Check .env file
    env_file = Path('.env')
    if not env_file.exists():
        print("❌ .env file not found")
        print("📝 Create .env file with: OPENROUTER_API_KEY=your-key-here")
    else:
        print("✅ .env file exists")
    
    # Check API key format
    api_key = os.getenv('OPENROUTER_API_KEY')
    if api_key:
        if api_key.startswith('sk-or-'):
            print("✅ API key format looks correct")
        else:
            print("⚠️  API key format might be wrong (should start with 'sk-or-')")
    
    # Check internet connection
    try:
        response = requests.get('https://openrouter.ai', timeout=5)
        if response.status_code == 200:
            print("✅ Internet connection to OpenRouter works")
        else:
            print("⚠️  OpenRouter website returned unexpected status")
    except:
        print("❌ Cannot reach OpenRouter website")

if __name__ == "__main__":
    print("🤖 SafeNest OpenRouter Debug Tool")
    print("=" * 50)
    
    # Run all tests
    check_common_issues()
    
    if test_openrouter_api():
        test_different_models()
    
    test_api_key_validity()
    
    print("\n" + "=" * 50)
    print("🎯 Debug Summary:")
    print("1. If API key is invalid, get new one from https://openrouter.ai/keys")
    print("2. If connection fails, check internet and firewall")
    print("3. If model fails, try a different model (see test results above)")
    print("4. Check Django logs for more detailed error messages")
    print("\n💡 Run this script again after making changes to test fixes")
