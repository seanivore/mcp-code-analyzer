from mcp_code_analyzer.server import CodeAnalyzerServer
import json

analyzer = CodeAnalyzerServer()

# Print metadata nicely formatted
print("=== Metadata ===")
print(json.dumps(analyzer.get_metadata(), indent=2))

# Print analysis with nice formatting
print("\n=== Complexity Analysis ===")
print(json.dumps(analyzer.analyze_file('test_code.py', 'complexity'), indent=2))