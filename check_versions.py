import sys
print(f"Python version: {sys.version}")
print("\nInstalled packages:")

try:
    import langchain
    print(f"✓ langchain: {langchain.__version__}")
except Exception as e:
    print(f"✗ langchain: {e}")

try:
    import langchain_core
    print(f"✓ langchain-core: {langchain_core.__version__}")
except Exception as e:
    print(f"✗ langchain-core: {e}")

try:
    import langchain_community
    print(f"✓ langchain-community: {langchain_community.__version__}")
except Exception as e:
    print(f"✗ langchain-community: {e}")

try:
    import langchain_google_genai
    print(f"✓ langchain-google-genai: {langchain_google_genai.__version__}")
except Exception as e:
    print(f"✗ langchain-google-genai: {e}")

try:
    import duckduckgo_search
    print(f"✓ duckduckgo-search: {duckduckgo_search.__version__}")
except Exception as e:
    print(f"✗ duckduckgo-search: {e}")
