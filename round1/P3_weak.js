const express = require('express');
const { execFile } = require('child_process');
const router = express.Router();

// Middleware placeholder for your admin authentication check
const requireAdmin = (req, res, next) => {
  // Replace with your actual admin validation logic
  if (!req.user || !req.user.isAdmin) {
    return res.status(403).json({ error: 'Access denied. Admin privileges required.' });
  }
  next();
};

/**
 * GET /api/admin/ping?host=example.com
 */
router.get('/ping', requireAdmin, (req, res) => {
  const { host } = req.query;

  if (!host) {
    return res.status(400).json({ error: 'Host parameter is required.' });
  }

  // Basic validation: ensure host format is an IP address or a valid hostname
  const hostnameRegex = /^([a-zA-Z0-9-]{1,63}\.)+[a-zA-Z]{2,63}$|^[a-zA-Z0-9-]{1,63}$|^(\d{1,3}\.){3}\d{1,3}$/;
  if (!hostnameRegex.test(host)) {
    return res.status(400).json({ error: 'Invalid host format.' });
  }

  // Adjust ping flags based on Operating System (-c for Linux/macOS, -n for Windows)
  const isWindows = process.platform === 'win32';
  const args = isWindows ? ['-n', '2', host] : ['-c', '2', host];

  // execFile avoids running in a shell, preventing shell injection attacks
  execFile('ping', args, { timeout: 5000 }, (error, stdout, stderr) => {
    if (error) {
      // Command failed, timed out, or host was unreachable
      return res.status(200).json({
        host,
        reachable: false,
        details: stderr || error.message
      });
    }

    return res.status(200).json({
      host,
      reachable: true,
      output: stdout
    });
  });
});

module.exports = router;