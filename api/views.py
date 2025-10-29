from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views import View
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json
import random
import time
import requests
import os

# Create your views here.

@api_view(['GET'])
def api_status(request):
    """API health check"""
    return Response({
        'status': 'healthy',
        'version': '1.0.0',
        'timestamp': '2024-01-01T00:00:00Z'
    })

@api_view(['GET'])
def api_info(request):
    """API information"""
    return Response({
        'name': 'SafeNest API',
        'version': '1.0.0',
        'description': 'Smart Home Security System API',
        'endpoints': {
            'devices': '/api/devices/',
            'security': '/api/security/',
            'ai': '/api/ai/',
            'status': '/api/status/'
        }
    })

@api_view(['GET', 'POST'])
def api_test(request):
    """API test endpoint"""
    if request.method == 'GET':
        return Response({
            'message': 'API is working correctly',
            'method': 'GET'
        })
    elif request.method == 'POST':
        return Response({
            'message': 'API is working correctly',
            'method': 'POST',
            'data_received': request.data
        })

# ===== AI CHATBOT VIEWS =====

@method_decorator(csrf_exempt, name='dispatch')
class AIChatView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            message = data.get('message', '')
            history = data.get('history', [])

            # Try OpenRouter API first, fallback to local responses
            try:
                response = self.get_openrouter_response(message, history)
                if not response:
                    print("🔄 Using fallback response system")
                    response = self.generate_fallback_response(message.lower(), history)
            except Exception as e:
                print(f"❌ OpenRouter API error: {e}")
                print("🔄 Using fallback response system")
                response = self.generate_fallback_response(message.lower(), history)

            actions = self.get_suggested_actions(message.lower())

            return JsonResponse({
                'success': True,
                'response': response,
                'actions': actions,
                'timestamp': time.time()
            })

        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)

    def get_openrouter_response(self, message, history):
        """Get response from OpenRouter API"""

        # Get API key from settings
        api_key = getattr(settings, 'OPENROUTER_API_KEY', None)

        if not api_key:
            print("❌ OpenRouter API key not found. Please set OPENROUTER_API_KEY in your .env file")
            return None

        if not api_key.startswith('sk-or-'):
            print(f"⚠️  API key format might be incorrect. Expected format: sk-or-... Got: {api_key[:10]}...")
            # Continue anyway as some keys might have different formats

        # Prepare conversation history for context
        messages = []

        # Add system prompt optimized for GLM-4.5-air model
        system_prompt = """You are SafeNest AI Assistant, a smart home and architecture expert. Help users with:

SMART HOME CONTROL:
• Control lights, temperature, security systems
• Monitor energy usage and optimization
• Manage IoT devices and automation
• Provide device status and troubleshooting

ARCHITECTURE & DESIGN:
• Generate floor plans and design suggestions
• Recommend materials and layouts
• Building code compliance assistance
• Cost estimation and project planning

COMMUNICATION STYLE:
• Be helpful, professional, and concise
• Use emojis appropriately (🏠🔒⚡🏗️)
• Provide actionable advice
• Focus on smart home and architecture topics
• When asked about device control, mention you can execute actions

Respond naturally and be ready to help with any smart home or architecture questions."""

        messages.append({"role": "system", "content": system_prompt})

        # Add recent conversation history (configurable limit)
        max_history = getattr(settings, 'AI_ASSISTANT_SETTINGS', {}).get('MAX_HISTORY_MESSAGES', 10)
        for msg in history[-max_history:]:
            role = "user" if msg.get('sender') == 'user' else "assistant"
            messages.append({"role": role, "content": msg.get('message', '')})

        # Add current user message
        messages.append({"role": "user", "content": message})

        # Get AI settings from configuration
        ai_settings = getattr(settings, 'AI_ASSISTANT_SETTINGS', {})

        # OpenRouter API request
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8000",  # Use localhost for development
            "X-Title": "SafeNest AI Assistant"
        }

        # Use the correct default model
        model = ai_settings.get('DEFAULT_MODEL', 'z-ai/glm-4.5-air:free')

        payload = {
            "model": model,
            "messages": messages,
            "max_tokens": ai_settings.get('MAX_TOKENS', 500),
            "temperature": ai_settings.get('TEMPERATURE', 0.7),
            "top_p": ai_settings.get('TOP_P', 0.9),
            "stream": False
        }

        try:
            timeout = ai_settings.get('TIMEOUT', 30)

            # Debug logging
            print(f"🔍 OpenRouter Request:")
            print(f"   Model: {payload['model']}")
            print(f"   API Key: ***{api_key[-4:] if len(api_key) > 4 else 'Invalid'}")
            print(f"   Message: {message[:50]}...")

            # Make the request
            response = requests.post(url, headers=headers, json=payload, timeout=timeout)

            print(f"   Status: {response.status_code}")

            if response.status_code == 200:
                result = response.json()

                if 'choices' in result and result['choices']:
                    ai_response = result['choices'][0]['message']['content']

                    # Handle empty responses
                    if ai_response and ai_response.strip():
                        print(f"   ✅ Success: {len(ai_response)} chars")
                        return ai_response.strip()
                    else:
                        print(f"   ⚠️  Empty response from model, using fallback")
                        return None
                else:
                    print(f"   ❌ No choices in response: {result}")
                    return None
            else:
                error_text = response.text[:200] if response.text else "No error message"
                print(f"   ❌ HTTP {response.status_code}: {error_text}")
                return None

        except requests.exceptions.Timeout as e:
            print(f"❌ OpenRouter API timeout: {e}")
            return None
        except requests.exceptions.ConnectionError as e:
            print(f"❌ OpenRouter API connection error: {e}")
            return None
        except requests.exceptions.HTTPError as e:
            print(f"❌ OpenRouter API HTTP error: {e}")
            print(f"   Response: {response.text if 'response' in locals() else 'No response'}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"❌ OpenRouter API request failed: {e}")
            return None
        except (KeyError, IndexError) as e:
            print(f"❌ OpenRouter API response parsing failed: {e}")
            print(f"   Response: {result if 'result' in locals() else 'No result'}")
            return None
        except Exception as e:
            print(f"❌ Unexpected error in OpenRouter API: {e}")
            return None

    def generate_fallback_response(self, message, history):
        """Generate fallback AI response when OpenRouter is unavailable"""

        # Smart Home Controls
        if any(word in message for word in ['light', 'lights', 'lamp']):
            if 'on' in message or 'turn on' in message:
                return "I'll turn on the lights for you. All smart lights in your home are now activated. 💡"
            elif 'off' in message or 'turn off' in message:
                return "Turning off all lights. Your home is now in energy-saving mode. 🌙"
            else:
                return "I can help you control your smart lights. Currently, you have 12 smart bulbs connected. Would you like me to turn them on, off, or adjust the brightness?"

        # Security System
        elif any(word in message for word in ['security', 'alarm', 'lock', 'safe']):
            return "🔒 Security Status: All systems operational. Your home is secure with:\n• Door locks: Engaged\n• Motion sensors: Active\n• Cameras: Recording\n• Alarm system: Armed\n\nWould you like me to show you the security dashboard?"

        # Temperature Control
        elif any(word in message for word in ['temperature', 'thermostat', 'heat', 'cold', 'warm']):
            temp = random.randint(20, 25)
            return f"🌡️ Current temperature: {temp}°C\nThermostat is set to maintain optimal comfort. I can adjust it if needed. What temperature would you prefer?"

        # Energy Management
        elif any(word in message for word in ['energy', 'power', 'electricity', 'consumption']):
            return "⚡ Energy Dashboard:\n• Current usage: 2.4 kW\n• Today's consumption: 18.5 kWh\n• Solar generation: 12.3 kWh\n• Battery level: 85%\n\nYour home is running efficiently! Would you like energy optimization suggestions?"

        # Architecture & Design
        elif any(word in message for word in ['design', 'architecture', 'room', 'space', 'layout']):
            return "🏗️ I can help with architectural design! I have access to:\n• AI-powered floor plan generation\n• 3D visualization tools\n• Material recommendations\n• Building code compliance\n\nWhat type of space are you looking to design?"

        # Device Status
        elif any(word in message for word in ['device', 'devices', 'status', 'connected']):
            return "📱 Connected Devices (24 total):\n• Smart lights: 12 online\n• Sensors: 8 active\n• Cameras: 4 recording\n• Smart plugs: 6 connected\n• Thermostat: 1 online\n• Door locks: 3 secured\n\nAll devices are functioning normally!"

        # Demo Mode
        elif 'demo' in message:
            return "🚀 Welcome to SafeNest Demo Mode!\n\nI'll show you our key features:\n1. Smart home device control\n2. AI-powered security monitoring\n3. Energy optimization\n4. Architecture design assistance\n\nTry asking me about 'lights', 'security', or 'energy' to see the system in action!"

        # Greetings
        elif any(word in message for word in ['hello', 'hi', 'hey', 'good morning', 'good evening']):
            return "Hello! 👋 Welcome to SafeNest. I'm your AI assistant ready to help with:\n\n🏠 Smart home automation\n🔒 Security management\n⚡ Energy optimization\n🏗️ Architecture design\n\nWhat can I help you with today?"

        # Help
        elif any(word in message for word in ['help', 'what can you do', 'commands']):
            return "I can assist you with:\n\n🏠 **Smart Home Control**\n• Control lights, temperature, devices\n• Monitor energy usage\n• Manage security systems\n\n🏗️ **Architecture & Design**\n• Generate floor plans\n• Recommend materials\n• 3D visualization\n• Building compliance\n\n🤖 **AI Features**\n• Voice commands\n• Automated routines\n• Predictive analytics\n• Smart suggestions\n\nJust ask me naturally about any of these topics!"

        # Default response with better AI-like responses
        else:
            # More intelligent responses based on context
            if any(word in message for word in ['hello', 'hi', 'hey']):
                return "Hello! 👋 I'm your SafeNest AI Assistant. I can help you with smart home control, security monitoring, energy optimization, and architectural design. What would you like to do today?"

            elif any(word in message for word in ['help', 'what', 'how', 'can you']):
                return "I'm here to help! 🤖 I can assist you with:\n\n🏠 **Smart Home**: Control lights, temperature, security\n⚡ **Energy**: Monitor usage and optimize efficiency\n🏗️ **Architecture**: Design advice and planning\n🔒 **Security**: System monitoring and alerts\n\nWhat specific area interests you?"

            elif any(word in message for word in ['thank', 'thanks']):
                return "You're welcome! 😊 I'm always here to help with your SafeNest smart home needs. Is there anything else you'd like to know about?"

            else:
                # Contextual responses
                responses = [
                    f"I understand you're asking about '{message[:30]}...'. I can help with smart home control, security, energy management, or architectural design. Could you be more specific about what you need?",
                    f"That's an interesting question about your smart home! I specialize in lighting control, security systems, energy optimization, and architectural planning. What specific aspect would you like to explore?",
                    f"I'm your SafeNest AI assistant, ready to help with your request. I can control devices, monitor security, optimize energy usage, or provide design advice. What would you like me to focus on?",
                    f"Let me help you with that! As your smart home AI, I can assist with automation, security, energy efficiency, and architectural design. Could you tell me more about your specific needs?"
                ]
                return random.choice(responses)

    def get_suggested_actions(self, message):
        """Get suggested actions based on message content"""
        actions = []

        if any(word in message for word in ['light', 'lights']):
            if 'on' in message:
                actions.append({'type': 'toggle_lights', 'value': True})
            elif 'off' in message:
                actions.append({'type': 'toggle_lights', 'value': False})

        elif 'security' in message:
            actions.append({'type': 'show_notification', 'message': 'Security system checked', 'level': 'success'})

        elif any(word in message for word in ['temperature', 'thermostat']):
            # Extract temperature if mentioned
            import re
            temp_match = re.search(r'(\d+)', message)
            if temp_match:
                temp = int(temp_match.group(1))
                if 15 <= temp <= 30:  # Reasonable temperature range
                    actions.append({'type': 'set_temperature', 'value': temp})

        elif 'demo' in message:
            actions.append({'type': 'show_notification', 'message': 'Demo mode activated!', 'level': 'info'})

        return actions

# ===== DEVICE CONTROL VIEWS =====

@csrf_exempt
@require_http_methods(["POST"])
def toggle_lights(request):
    """Toggle all smart lights"""
    try:
        # Simulate light control
        success = random.choice([True, True, True, False])  # 75% success rate

        if success:
            return JsonResponse({
                'success': True,
                'message': 'Lights toggled successfully',
                'lights_on': random.choice([True, False])
            })
        else:
            return JsonResponse({
                'success': False,
                'error': 'Some lights are offline'
            }, status=500)

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def activate_security(request):
    """Activate security mode"""
    try:
        # Simulate security activation
        return JsonResponse({
            'success': True,
            'message': 'Security mode activated',
            'armed': True,
            'sensors_active': 8,
            'cameras_recording': 4
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def set_temperature(request):
    """Set thermostat temperature"""
    try:
        data = json.loads(request.body)
        temperature = data.get('temperature')

        if not temperature or not (15 <= temperature <= 30):
            return JsonResponse({
                'success': False,
                'error': 'Invalid temperature range (15-30°C)'
            }, status=400)

        # Simulate temperature setting
        return JsonResponse({
            'success': True,
            'message': f'Temperature set to {temperature}°C',
            'current_temp': temperature,
            'target_temp': temperature
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

# ===== CONSULTATION VIEWS =====

@csrf_exempt
@require_http_methods(["POST"])
def submit_consultation(request):
    """Submit consultation request"""
    try:
        data = json.loads(request.body)

        required_fields = ['name', 'email', 'service']
        for field in required_fields:
            if not data.get(field):
                return JsonResponse({
                    'success': False,
                    'error': f'{field.title()} is required'
                }, status=400)

        # Here you would typically save to database
        # For now, we'll just simulate success

        return JsonResponse({
            'success': True,
            'message': 'Consultation request submitted successfully',
            'reference_id': f'SAFE-{random.randint(1000, 9999)}'
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

# ===== SYSTEM STATUS VIEWS =====

@require_http_methods(["GET"])
def system_status(request):
    """Get overall system status"""
    try:
        return JsonResponse({
            'success': True,
            'status': {
                'devices_online': random.randint(20, 24),
                'total_devices': 24,
                'security_armed': True,
                'energy_usage': round(random.uniform(2.0, 3.5), 1),
                'temperature': random.randint(20, 25),
                'last_updated': time.time()
            }
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@require_http_methods(["GET"])
def ai_status(request):
    """Get AI assistant status including OpenRouter availability"""
    try:
        # Check if OpenRouter API key is configured
        api_key = getattr(settings, 'OPENROUTER_API_KEY', None)
        openrouter_available = bool(api_key)

        # Get AI settings
        ai_settings = getattr(settings, 'AI_ASSISTANT_SETTINGS', {})

        return JsonResponse({
            'success': True,
            'openrouter_available': openrouter_available,
            'current_model': ai_settings.get('DEFAULT_MODEL', 'anthropic/claude-3.5-sonnet'),
            'fallback_model': ai_settings.get('FALLBACK_MODEL', 'openai/gpt-3.5-turbo'),
            'max_tokens': ai_settings.get('MAX_TOKENS', 500),
            'features': [
                'smart_home_control',
                'architecture_design',
                'voice_recognition',
                'conversation_context'
            ],
            'status': 'online' if openrouter_available else 'local_mode'
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
