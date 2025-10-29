from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Check OpenRouter settings and configuration'

    def handle(self, *args, **options):
        self.stdout.write('🔍 Checking SafeNest Settings')
        self.stdout.write('=' * 35)
        
        # Check API key
        api_key = getattr(settings, 'OPENROUTER_API_KEY', None)
        if api_key:
            self.stdout.write(
                self.style.SUCCESS(f'✅ API Key: ***{api_key[-4:]}')
            )
        else:
            self.stdout.write(
                self.style.ERROR('❌ API Key: Not found')
            )
        
        # Check AI settings
        ai_settings = getattr(settings, 'AI_ASSISTANT_SETTINGS', {})
        self.stdout.write(f'\n🤖 AI Settings:')
        self.stdout.write(f'   Model: {ai_settings.get("DEFAULT_MODEL", "Not set")}')
        self.stdout.write(f'   Fallback: {ai_settings.get("FALLBACK_MODEL", "Not set")}')
        self.stdout.write(f'   Max Tokens: {ai_settings.get("MAX_TOKENS", "Not set")}')
        
        # Check environment
        import os
        env_key = os.getenv('OPENROUTER_API_KEY')
        if env_key:
            self.stdout.write(
                self.style.SUCCESS(f'\n✅ Environment Key: ***{env_key[-4:]}')
            )
        else:
            self.stdout.write(
                self.style.ERROR('\n❌ Environment Key: Not found')
            )
        
        # Check .env file
        from pathlib import Path
        env_file = Path('.env')
        if env_file.exists():
            self.stdout.write(
                self.style.SUCCESS('\n✅ .env file: Found')
            )
            
            # Read .env content
            with open(env_file, 'r') as f:
                content = f.read()
                if 'OPENROUTER_API_KEY' in content:
                    self.stdout.write('✅ OPENROUTER_API_KEY: Found in .env')
                else:
                    self.stdout.write(
                        self.style.ERROR('❌ OPENROUTER_API_KEY: Not in .env')
                    )
        else:
            self.stdout.write(
                self.style.ERROR('\n❌ .env file: Not found')
            )
        
        self.stdout.write('\n' + '=' * 35)
        self.stdout.write('🎯 Summary:')
        
        if api_key and ai_settings:
            self.stdout.write(
                self.style.SUCCESS('✅ Configuration looks good!')
            )
        else:
            self.stdout.write(
                self.style.ERROR('❌ Configuration issues found')
            )
