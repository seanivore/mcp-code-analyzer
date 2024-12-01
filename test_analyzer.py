from src.mcp_code_analyzer.server import CodeAnalyzerServer

analyzer = CodeAnalyzerServer()

# First, test the new metadata method
print("--- METADATA ---")
print(analyzer.get_metadata())

# Then test all analysis types like before
analysis_types = ['structure', 'complexity', 'dependencies']

for analysis_type in analysis_types:
    print(f"\n--- {analysis_type.upper()} ANALYSIS ---")
    result = analyzer.analyze_file('test_code.py', analysis_type)
    print(result)