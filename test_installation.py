"""
Test script to verify the installation and basic functionality.
Run this before starting the main application.
"""
import sys
import os

def test_imports():
    """Test if all required packages are installed."""
    print("Testing imports...")
    
    required_packages = [
        ('fastapi', 'FastAPI'),
        ('uvicorn', 'Uvicorn'),
        ('pydantic', 'Pydantic'),
        ('google.generativeai', 'Google Generative AI'),
        ('chromadb', 'ChromaDB'),
        ('langchain', 'LangChain'),
        ('streamlit', 'Streamlit'),
    ]
    
    missing = []
    for package, name in required_packages:
        try:
            __import__(package)
            print(f"✓ {name}")
        except ImportError:
            print(f"✗ {name} - MISSING")
            missing.append(name)
    
    if missing:
        print(f"\n❌ Missing packages: {', '.join(missing)}")
        print("Run: pip install -r requirements.txt")
        return False
    else:
        print("\n✅ All packages installed successfully!")
        return True

def test_env_file():
    """Test if .env file exists and has required variables."""
    print("\nTesting environment configuration...")
    
    if not os.path.exists('.env'):
        print("❌ .env file not found!")
        print("Create it by copying .env.example:")
        print("  cp .env.example .env")
        print("Then add your Gemini API key")
        return False
    
    with open('.env', 'r') as f:
        content = f.read()
    
    if 'GEMINI_API_KEY=your_gemini_api_key_here' in content:
        print("⚠️  .env file found but API key not configured")
        print("Please add your actual Gemini API key to .env")
        return False
    
    if 'GEMINI_API_KEY=' in content:
        print("✅ .env file configured")
        return True
    
    print("❌ .env file missing GEMINI_API_KEY")
    return False

def test_document():
    """Test if document exists."""
    print("\nTesting document...")
    
    if os.path.exists('data/innovate_inc_report.txt'):
        print("✅ Document found")
        return True
    else:
        print("❌ Document not found at data/innovate_inc_report.txt")
        return False

def test_project_structure():
    """Test if all required directories exist."""
    print("\nTesting project structure...")
    
    required_dirs = [
        'src',
        'src/config',
        'src/data',
        'src/retrieval',
        'src/agents',
        'src/api',
        'data',
    ]
    
    missing = []
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"✓ {dir_path}/")
        else:
            print(f"✗ {dir_path}/ - MISSING")
            missing.append(dir_path)
    
    if missing:
        print(f"\n❌ Missing directories: {', '.join(missing)}")
        return False
    else:
        print("\n✅ All directories present")
        return True

def main():
    """Run all tests."""
    print("=" * 60)
    print("AI Market Analyst Agent - Installation Test")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_env_file,
        test_document,
        test_project_structure,
    ]
    
    results = [test() for test in tests]
    
    print("\n" + "=" * 60)
    if all(results):
        print("✅ ALL TESTS PASSED!")
        print("\nYou're ready to run the application:")
        print("1. Start backend: uvicorn src.main:app --reload")
        print("2. Start UI: streamlit run app.py")
        print("\nOr with Docker: docker-compose up --build")
    else:
        print("❌ SOME TESTS FAILED")
        print("\nPlease fix the issues above before running the application.")
    print("=" * 60)
    
    return all(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
