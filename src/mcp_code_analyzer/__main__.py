import asyncio
import json
from .server import CodeAnalyzerServer

async def main():
    server = CodeAnalyzerServer()
    # Print metadata for Claude to recognize the server
    print(json.dumps(server.get_metadata()), flush=True)
    # Handle requests
    await server.handle_stdin()

if __name__ == "__main__":
    asyncio.run(main())