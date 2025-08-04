import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# --- ここからマイグレーション自動実行 ---
MIGRATION_FLAG = os.path.join(os.path.dirname(__file__), 'migrated.flag')

if not os.path.exists(MIGRATION_FLAG):
    try:
        import django
        django.setup()
        from django.core.management import call_command
        call_command('migrate', interactive=False)
        # フラグファイルを作成して2回目以降は実行しない
        with open(MIGRATION_FLAG, 'w') as f:
            f.write('migrated')
    except Exception as e:
        print(f"Migration failed: {e}")
# --- ここまで ---

application = get_wsgi_application()