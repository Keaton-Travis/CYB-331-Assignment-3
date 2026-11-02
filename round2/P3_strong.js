const express = require('express');
const { execFile } = require('child_process');

const app = express();
app.use(express.json());

// Strict regex matching valid hostnames and IPv4 characters, rejecting all shell metacharacters
const HOST_REGEX = /^[a-zA-Z0-9.-]{1,253}$/;

app.post('/api/ping', (req, res) => {
  const { host } = req.body;

  // 1. Input Validation: Check type and compliance with the allowed character set
  if (!host || typeof host !== 'string' || !HOST_REGEX.test(host)) {
    console.error(`[Security Log] Invalid ping target rejected: ${JSON.stringify(host)}`);
    return res.status(400).json({ error: 'Invalid host or IP address format.' });
  }

  // 2. Safe Execution: execFile runs the binary directly without a shell.
  // Arguments are passed as an array, neutralizing any command injection attempts.
  // Note: Use '-c 1' for Linux/macOS systems. For Windows, change to '-n' '1'.
  const args = ['-c', '1', host];

  execFile('ping', args, (error, stdout, stderr) => {
    if (error) {
      // Log the full technical error internally for debugging/monitoring
      console.error(`[Execution Error] Ping failed for host "${host}":`, error.message);
      if (stderr) console.error(`[Stderr]: ${stderr}`);

      // Return a sanitized, generic 400 Bad Request to the client
      return res.status(400).json({ 
        error: 'Ping execution failed or the target host is unreachable.' 
      });
    }

    // Return successful output
    return res.json({
      success: true,
      output: stdout
    });
  });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});