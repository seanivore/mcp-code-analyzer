import * as fs from 'fs';
import * as path from 'path';

interface AnalyzeCodeArgs {
  file_path: string;
  analysis_type: 'structure' | 'complexity' | 'dependencies';
}

async function analyzeCode(args: AnalyzeCodeArgs): Promise<string> {
  const { file_path, analysis_type } = args;

  if (!fs.existsSync(file_path)) {
    throw new Error(`File not found: ${file_path}`);
  }

  if (path.extname(file_path) !== '.py') {
    throw new Error('Only Python files are supported');
  }

  const fileContents = fs.readFileSync(file_path, 'utf-8');

  switch (analysis_type) {
    case 'structure':
      return analyzeStructure(fileContents);
    case 'complexity':
      return analyzeComplexity(fileContents);
    case 'dependencies':
      return analyzeDependencies(fileContents);
    default:
      throw new Error(`Unknown analysis type: ${analysis_type}`);
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

function analyzeComplexity(code: string): string {
  return JSON.stringify({ message: "Complexity analysis not yet implemented" });
}

function analyzeDependencies(code: string): string {
  return JSON.stringify({ message: "Dependency analysis not yet implemented" });
}

// Main execution
if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.length !== 2) {
    console.error('Usage: node index.js <file_path> <analysis_type>');
    process.exit(1);
  }

  const [file_path, analysis_type] = args;
  
  analyzeCode({ file_path, analysis_type } as AnalyzeCodeArgs)
    .then(result => {
      console.log(result);
    })
    .catch(error => {
      console.error('Error:', error.message);
      process.exit(1);
    });
}