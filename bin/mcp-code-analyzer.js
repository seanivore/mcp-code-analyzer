#!/usr/bin/env node

const { spawn } = require('child_process');
const path = require('path');

console.error('Debug: Starting Python MCP server...');

// Get the full path to the Python module
const pythonPath = process.env.VIRTUAL_ENV 
    ? path.join(process.env.VIRTUAL_ENV, 'bin', 'python')
    : 'python';

console.error('Debug: Using Python path:', pythonPath);

// Launch the Python MCP server
const pythonProcess = spawn(pythonPath, ['-m', 'mcp_code_analyzer.server'], {
    stdio: ['pipe', 'pipe', 'pipe'],
    env: { ...process.env, PYTHONUNBUFFERED: '1' }
});

// Handle Python process stdout
pythonProcess.stdout.on('data', (data) => {
    console.log(data.toString());
});

// Handle Python process stderr
pythonProcess.stderr.on('data', (data) => {
    console.error('Python stderr:', data.toString());
});

// Handle stdin
process.stdin.on('data', (data) => {
    console.error('Debug: Received stdin:', data.toString());
    pythonProcess.stdin.write(data);
});

pythonProcess.on('error', (err) => {
    console.error('Failed to start Python process:', err);
    process.exit(1);
});

pythonProcess.on('exit', (code) => {
    console.error('Server process exited with code:', code);
    process.exit(code);
});

// Handle process termination
process.on('SIGTERM', () => {
    pythonProcess.kill();
});

process.on('SIGINT', () => {
    pythonProcess.kill();
});