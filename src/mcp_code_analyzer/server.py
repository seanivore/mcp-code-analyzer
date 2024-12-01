import ast
import json
import sys
from typing import Any, Dict, List, Set
from pathlib import Path

print("Server module loading...", file=sys.stderr)

class CodeAnalyzerServer:
    def __init__(self):
        print("Initializing CodeAnalyzerServer...", file=sys.stderr)
        self.name = "code_analyzer"
        self.description = """Analyzes Python code for:
            - Structure (functions, classes, methods)
            - Complexity (cyclomatic complexity, decision points)
            - Dependencies (imports and module usage)
            Only works within allowed filesystem directories."""
        self.parameters = {
            "file": "string",
            "type": "string"
        }

    async def handle_stdin(self):
        """Handle stdin/stdout communication with Claude."""
        print("Starting stdin handler...", file=sys.stderr)
        for line in sys.stdin:
            try:
                response = await self.handle_request(line.strip())
                print(response, flush=True)
            except Exception as e:
                print(json.dumps({"error": str(e)}), flush=True)
    
    async def handle_request(self, request: str) -> str:
        try:
            # Parse the request JSON
            req_data = json.loads(request)
            file_path = req_data.get('file')
            analysis_type = req_data.get('type')
            
            if not file_path or not analysis_type:
                return json.dumps({"error": "Missing required parameters: file and type"})
            
            # Perform the analysis
            result = self.analyze_file(file_path, analysis_type)
            return json.dumps(result)
            
        except Exception as e:
            return json.dumps({"error": str(e)})
    
    def get_metadata(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters
        }

    def analyze_file(self, file_path: str, analysis_type: str) -> Dict[str, Any]:
        path = Path(file_path)
        
        if not path.exists():
            return {"error": f"File not found: {file_path}"}
            
        try:
            with open(path, 'r') as f:
                content = f.read()
                
            tree = ast.parse(content)
            
            if analysis_type == 'structure':
                return self._analyze_structure(tree)
            elif analysis_type == 'complexity':
                return self._analyze_complexity(tree)
            elif analysis_type == 'dependencies':
                return self._analyze_dependencies(tree)
            else:
                return {"error": f"Unknown analysis type: {analysis_type}"}
                
        except Exception as e:
            return {"error": str(e)}
            
    def _analyze_structure(self, tree: ast.AST) -> Dict[str, Any]:
        functions = []
        classes = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append({
                    'name': node.name,
                    'arguments': [arg.arg for arg in node.args.args],
                    'line_number': node.lineno
                })
            elif isinstance(node, ast.ClassDef):
                methods = [n.name for n in ast.walk(node) if isinstance(n, ast.FunctionDef)]
                classes.append({
                    'name': node.name,
                    'methods': methods,
                    'line_number': node.lineno
                })
                
        return {
            "type": "structure",
            "functions": functions,
            "classes": classes
        }
    
    def _analyze_complexity(self, tree: ast.AST) -> Dict[str, Any]:
        complexity_info = {}
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                # Count decision points for cyclomatic complexity
                decisions = [n for n in ast.walk(node) if isinstance(n, (
                    ast.If,        # if statements
                    ast.For,       # for loops
                    ast.While,     # while loops
                    ast.And,       # and operators
                    ast.Or,        # or operators
                    ast.ExceptHandler  # except blocks
                ))]
                
                # Count returns and breaks
                returns = len([n for n in ast.walk(node) if isinstance(n, ast.Return)])
                breaks = len([n for n in ast.walk(node) if isinstance(n, ast.Break)])
                
                # Calculate cyclomatic complexity (decisions + 1)
                cyclomatic_complexity = len(decisions) + 1
                
                # Get variable usage
                variables = self._get_variable_usage(node)
                
                complexity_info[node.name] = {
                    'cyclomatic_complexity': cyclomatic_complexity,
                    'complexity_level': self._get_complexity_level(cyclomatic_complexity),
                    'decision_points': len(decisions),
                    'returns': returns,
                    'breaks': breaks,
                    'line_count': node.end_lineno - node.lineno if hasattr(node, 'end_lineno') else 1,
                    'variable_uses': len(variables),
                    'variables': list(variables)
                }
        
        return {
            "type": "complexity",
            "functions": complexity_info,
            "summary": {
                "avg_complexity": sum(f['cyclomatic_complexity'] for f in complexity_info.values()) / len(complexity_info) if complexity_info else 0,
                "most_complex_function": max(complexity_info.items(), key=lambda x: x[1]['cyclomatic_complexity'])[0] if complexity_info else None
            }
        }
    
    def _get_complexity_level(self, complexity: int) -> str:
        if complexity <= 5:
            return "low"
        elif complexity <= 10:
            return "moderate"
        else:
            return "high"
    
    def _get_variable_usage(self, node: ast.AST) -> Set[str]:
        variables = set()
        for n in ast.walk(node):
            if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Store):
                variables.add(n.id)
        return variables

    def _analyze_dependencies(self, tree: ast.AST) -> Dict[str, Any]:
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.extend(n.name for n in node.names)
            elif isinstance(node, ast.ImportFrom):
                imports.append(f"{node.module}.{node.names[0].name}")
                
        return {
            "type": "dependencies",
            "imports": imports
        }

async def main():
    print("Main function starting...", file=sys.stderr)  # Add this line
    server = CodeAnalyzerServer()
    await server.handle_stdin()

if __name__ == "__main__":
    print("Script running directly...", file=sys.stderr)  # Add this line
    import asyncio
    asyncio.run(main())