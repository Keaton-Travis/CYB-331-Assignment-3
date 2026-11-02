const express = require('express');
const { exec } = require('child_process');

const app = express();
app.use(express.json());

app.get('/admin/ping', (req, res) => {
  const { host } = req.query;

  if (!host) {
    return res.status(400).json({ error: 'Host parameter is required.' });
  }

  // Determine command flag based on OS (-c for Linux/Mac, -n for Windows)
  const isWindows = process.platform === 'win32';
  const pingFlag = isWindows ? '-n 1' : '-c 1';

  // Execute the system ping command
  exec(`ping ${pingFlag} ${host}`, (error, stdout, stderr) => {
    if (error) {
      return res.status(200).json({
        host,
        reachable: false,
        details: 'Host unreachable or request timed out.'
      });
    }

    return res.status(200).json({
      host,
      reachable: true,
      output: stdout
    });
  });
});

app.listen(3000, () => {
  console.log('Server running on port 3000');
});