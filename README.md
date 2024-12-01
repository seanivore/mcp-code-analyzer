# MCP Code Analyzer

A Model Context Protocol server that analyzes Python code for:
- Code structure (functions, classes, methods)
- Code complexity (cyclomatic complexity, decision points)
- Dependencies (imports)

## Installation

```bash
# Create and activate a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On macOS/Linux
.\venv\Scripts\activate  # On Windows

# Install the package
pip install mcp-code-analyzer
```

## Usage with Claude

Add to your `claude_desktop_config.json`:

```json
"code-analyzer": {
  "command": "npx",
  "args": [
    "-y",
    "@modelcontextprotocol/server-code-analyzer",
    "/path/to/allowed/directory"  # e.g., "/Users/username/Projects"
  ]
}
```

## Features

Supports three types of analysis:
1. `structure` - Lists all functions, classes, and methods
2. `complexity` - Calculates cyclomatic complexity and code metrics
3. `dependencies` - Shows all module imports and dependencies

## Example Usage

Ask Claude questions like:
- "Analyze the complexity of file.py"
- "Show me the structure of file.py"
- "What dependencies does file.py use?"