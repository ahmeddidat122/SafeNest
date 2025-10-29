# OpenRouter AI Integration Setup

This guide explains how to set up OpenRouter AI integration for the SafeNest AI Assistant.

## Overview

SafeNest AI Assistant now supports OpenRouter API for enhanced conversational AI capabilities. OpenRouter provides access to multiple AI models including Claude, GPT-4, and others through a single API.

## Features

- **Multiple AI Models**: Access to Claude 3.5 Sonnet, GPT-4, and other models
- **Fallback System**: Automatic fallback to local responses if API is unavailable
- **Conversation Context**: Maintains chat history for better responses
- **Configurable Settings**: Customizable model parameters
- **Smart Home Focus**: Specialized prompts for smart home and architecture topics

## Setup Instructions

### 1. Get OpenRouter API Key

1. Visit [OpenRouter](https://openrouter.ai/)
2. Sign up for an account
3. Go to [API Keys](https://openrouter.ai/keys)
4. Create a new API key
5. Copy the API key for configuration

### 2. Configure Environment Variables

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file and add your OpenRouter API key:
   ```env
   OPENROUTER_API_KEY=your-openrouter-api-key-here
   ```

### 3. Install Dependencies

Make sure you have the required packages installed:
```bash
pip install -r requirements.txt
```

### 4. Configure AI Settings (Optional)

You can customize AI behavior in `safenest/settings.py`:

```python
AI_ASSISTANT_SETTINGS = {
    'DEFAULT_MODEL': 'z-ai/glm-4.5-air:free',       # Primary model (FREE!)
    'FALLBACK_MODEL': 'meta-llama/llama-3.1-8b-instruct:free',  # Backup model (FREE!)
    'MAX_TOKENS': 500,                               # Response length limit
    'TEMPERATURE': 0.7,                              # Creativity level (0-1)
    'TOP_P': 0.9,                                    # Response diversity
    'TIMEOUT': 30,                                   # API timeout in seconds
    'MAX_HISTORY_MESSAGES': 10,                      # Chat history limit
}
```

## Available Models

OpenRouter supports many AI models. Popular choices for SafeNest:

### Free Models (Recommended for SafeNest):
- `z-ai/glm-4.5-air:free` - **PRIMARY MODEL** - Excellent performance, completely free
- `meta-llama/llama-3.1-8b-instruct:free` - **FALLBACK MODEL** - Reliable backup, free
- `meta-llama/llama-3.1-70b-instruct:free` - More powerful free option

### Premium Models (if you want to upgrade):
- `anthropic/claude-3.5-sonnet` - Best overall performance
- `anthropic/claude-3-haiku` - Fast and cost-effective
- `openai/gpt-4-turbo` - Strong reasoning capabilities
- `openai/gpt-3.5-turbo` - Good balance of speed and quality

## How It Works

### 1. Request Flow
```
User Message → OpenRouter API → AI Response → SafeNest Processing → User
                     ↓ (if fails)
                Fallback Response → User
```

### 2. System Prompt
The AI assistant uses a specialized system prompt that focuses on:
- Smart home device control
- Architecture and design assistance
- Energy management
- Security system management
- Professional and helpful responses

### 3. Context Management
- Maintains last 10 messages for context (configurable)
- Preserves conversation flow
- Handles both user and assistant messages

## API Endpoints

### Chat Endpoint
```
POST /api/ai/chat/
Content-Type: application/json

{
    "message": "Turn on the living room lights",
    "history": [
        {
            "sender": "user",
            "message": "Hello",
            "timestamp": "2024-01-01T00:00:00Z"
        },
        {
            "sender": "bot",
            "message": "Hello! How can I help you?",
            "timestamp": "2024-01-01T00:00:01Z"
        }
    ]
}
```

### Response Format
```json
{
    "success": true,
    "response": "I'll turn on the living room lights for you...",
    "actions": [
        {
            "type": "toggle_lights",
            "value": true
        }
    ],
    "timestamp": 1704067200
}
```

## Error Handling

The system includes robust error handling:

1. **API Key Missing**: Falls back to local responses
2. **Network Errors**: Automatic fallback with user notification
3. **Rate Limiting**: Graceful degradation
4. **Invalid Responses**: Error logging and fallback

## Cost Management

OpenRouter charges based on usage. To manage costs:

1. **Set Token Limits**: Configure `MAX_TOKENS` appropriately
2. **Choose Efficient Models**: Use faster models for simple queries
3. **Monitor Usage**: Check OpenRouter dashboard regularly
4. **Implement Caching**: Consider caching common responses

## Testing

### Test API Connection
```python
# In Django shell
from api.views import AIChatView
view = AIChatView()
response = view.get_openrouter_response("Hello", [])
print(response)
```

### Test Fallback System
1. Remove or invalidate API key
2. Send chat message
3. Verify fallback responses work

## Troubleshooting

### Common Issues:

1. **"OpenRouter API key not found"**
   - Check `.env` file exists and has correct key
   - Restart Django server after adding key

2. **"API request failed"**
   - Verify internet connection
   - Check API key validity
   - Review OpenRouter status page

3. **"Response parsing failed"**
   - Check model availability
   - Verify request format
   - Review OpenRouter documentation

### Debug Mode:
Enable debug logging to see API interactions:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Security Considerations

1. **API Key Protection**: Never commit API keys to version control
2. **Rate Limiting**: Implement user-based rate limiting
3. **Input Validation**: Sanitize user inputs
4. **Error Messages**: Don't expose sensitive information in errors

## Performance Optimization

1. **Model Selection**: Choose appropriate models for different use cases
2. **Context Optimization**: Limit conversation history appropriately
3. **Caching**: Cache common responses
4. **Async Processing**: Consider async API calls for better performance

## Support

For issues with:
- **OpenRouter API**: Contact OpenRouter support
- **SafeNest Integration**: Check GitHub issues or documentation
- **Model-specific problems**: Refer to model provider documentation
