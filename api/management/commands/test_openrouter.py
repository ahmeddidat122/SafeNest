from django.core.management.base import BaseCommand
from django.conf import settings
from api.views import AIChatView
import json

class Command(BaseCommand):
    help = 'Test OpenRouter API integration'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🤖 Testing OpenRouter API Integration')
        )
        
        # Check configuration
        api_key = getattr(settings, 'OPENROUTER_API_KEY', None)
        if not api_key:
            self.stdout.write(
                self.style.ERROR('❌ OPENROUTER_API_KEY not found in settings')
            )
            self.stdout.write('📝 Add OPENROUTER_API_KEY to your .env file')
            return
        
        self.stdout.write(f'✅ API Key configured: ***{api_key[-4:]}')
        
        # Test AI chat view
        view = AIChatView()
        
        test_messages = [
            "Hello, this is a test",
            "Turn on the lights",
            "What's the temperature?"
        ]
        
        for i, message in enumerate(test_messages, 1):
            self.stdout.write(f'\n🧪 Test {i}: "{message}"')
            
            try:
                response = view.get_openrouter_response(message, [])
                
                if response:
                    self.stdout.write(
                        self.style.SUCCESS(f'✅ Success: {response[:100]}...')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING('⚠️  No response from OpenRouter, using fallback')
                    )
                    fallback = view.generate_fallback_response(message.lower(), [])
                    self.stdout.write(f'🔄 Fallback: {fallback[:100]}...')
                    
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'❌ Error: {e}')
                )
        
        self.stdout.write(
            self.style.SUCCESS('\n✅ Test completed!')
        )
