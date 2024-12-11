import * as fs from 'fs';
import * as path from 'path';
import * as http from 'http';

interface AnalyzeCodeArgs {
  file_path: string;
  analysis_type: 'structure' | 'complexity' | 'dependencies';
}

function analyzeCode(args: AnalyzeCodeArgs): string {
  console.log('Analyzing code:', args);
  
  const { file_path, analysis_type } = args;

  if (!fs.existsSync(file_path)) {
    return `Error: File not found: ${file_path}`;
  }

  if (path.extname(file_path) !== '.py') {
    return 'Error: Only Python files are supported';
  }

  const fileContents = fs.readFileSync(file_path, 'utf-8');
  console.log('File contents:', fileContents);

  if (analysis_type === 'structure') {
    return analyzeStructure(fileContents);
  } else {
    return `Analysis type ${analysis_type} not implemented yet`;
  }
}

function analyzeStructure(code: string): string {
  const structure = {
    functions: [] as string[],
    classes: [] as string[]
  };

  const lines = code.split('\n');
  for (const line of lines) {
    if (line.trim().startsWith('def ')) {
      const functionName = line.trim().split(' ')[1].split('(')[0];
      structure.functions.push(functionName);
    } else if (line.trim().startsWith('class ')) {
      const className = line.trim().split(' ')[1].split('(')[0];
      structure.classes.push(className);
    }
  }

  return JSON.stringify(structure, null, 2);
}

const server = http.createServer((req, res) => {
  console.log('Received request:', req.method, req.url);

  if (req.method === 'POST' && req.url === '/analyze') {
    let body = '';
    req.on('data', chunk => {
      body += chunk.toString();
    });
    req.on('end', () => {
      console.log('Received body:', body);
      try {
        const args: AnalyzeCodeArgs = JSON.parse(body);
        const result = analyzeCode(args);
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ result }));
      } catch (error) {
        console.error('Error:', error);
        res.writeHead(400, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: 'An error occurred' }));
      }
    });
  } else {
    res.writeHead(404, { 'Content-Type': 'text/plain' });
    res.end('Not Found');
  }
});

const PORT = 3000;
server.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});