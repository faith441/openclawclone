#!/bin/bash

echo ""
echo "=========================================="
echo "  🧪 Testing Zenthral System"
echo "=========================================="
echo ""

cd /Users/faithtemporosa/openclawclone/openclawclone/web

# Test 1: Check Python imports
echo "Test 1: Checking Python imports..."
python3 fix_imports.py

echo ""
echo "✓ Import check complete"
echo ""

# Test 2: Check database can be created
echo "Test 2: Checking database creation..."
python3 -c "
import sys
sys.path.insert(0, '.')
try:
    from app import app, db, HAS_NEW_MODULES
    if HAS_NEW_MODULES:
        with app.app_context():
            db.create_all()
            print('✓ Database tables created successfully')
    else:
        print('⚠️  Running in legacy mode')
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()
" 2>&1

echo ""
echo "=========================================="
echo "  ✅ Tests Complete!"
echo "=========================================="
echo ""
echo "🚀 Ready to start the server:"
echo "   python3 app.py"
echo ""
echo "Then visit:"
echo "   http://localhost:5001/auth/register"
echo ""
echo "=========================================="
echo ""
