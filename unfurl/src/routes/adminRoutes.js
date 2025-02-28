const express = require('express');
const router = express.Router();
const os = require('os');
const { exec } = require('child_process');

const users = [
    { id: 1, name: 'Admin', role: 'Administrator', status: 'Active' },
    { id: 2, name: 'John Doe', role: 'User', status: 'Active' },
    { id: 3, name: 'Jane Smith', role: 'User', status: 'Suspended' },
];

router.get('/', (req, res) => {
    res.send(`
        <html>
            <head>
                <title>Admin Panel</title>
            </head>
            <body>
                <h1>Admin Panel</h1>
                <p>Welcome to the admin control panel! Here are the available features:</p>
                <ul>
                    <li><a href="/admin/system-info">System Information</a></li>
                    <li><a href="/admin/users">Manage Users</a></li>
                    <li><a href="/admin/logs">View Logs</a></li>
                    <li><a href="/admin/settings">Settings</a></li>
                    <li><a href="/admin/execute">Execute Command</a></li>
                </ul>
            </body>
        </html>
    `);
});

router.get('/system-info', (req, res) => {
    const systemInfo = {
        hostname: os.hostname(),
        platform: os.platform(),
        arch: os.arch(),
        uptime: `${(os.uptime() / 3600).toFixed(2)} hours`,
        totalMemory: `${(os.totalmem() / 1024 / 1024 / 1024).toFixed(2)} GB`,
        freeMemory: `${(os.freemem() / 1024 / 1024 / 1024).toFixed(2)} GB`,
        cpuCount: os.cpus().length,
        loadAverage: os.loadavg(),
    };

    res.send(`
        <h1>System Information</h1>
        <ul>
            ${Object.entries(systemInfo).map(([key, value]) => `<li><strong>${key}:</strong> ${value}</li>`).join('')}
        </ul>
        <a href="/admin">Back to Admin Panel</a>
    `);
});

router.get('/users', (req, res) => {
    res.send(`
        <h1>Manage Users</h1>
        <table border="1" cellpadding="5" cellspacing="0">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Role</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
                ${users.map(user => `
                    <tr>
                        <td>${user.id}</td>
                        <td>${user.name}</td>
                        <td>${user.role}</td>
                        <td>${user.status}</td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
        <a href="/admin">Back to Admin Panel</a>
    `);
});

router.get('/logs', (req, res) => {
    const logs = [
        { timestamp: new Date().toISOString(), message: 'User Admin logged in' },
        { timestamp: new Date().toISOString(), message: 'System checked for updates' },
        { timestamp: new Date().toISOString(), message: 'User John Doe updated their profile' },
    ];

    res.send(`
        <h1>View Logs</h1>
        <pre>${logs.map(log => `[${log.timestamp}] ${log.message}`).join('\n')}</pre>
        <a href="/admin">Back to Admin Panel</a>
    `);
});

router.get('/settings', (req, res) => {
    res.send(`
        <h1>Settings</h1>
        <form action="/admin/settings" method="POST">
            <label for="app-name">Application Name:</label>
            <input type="text" id="app-name" name="appName" value="UnfurlerApp" required>
            <br><br>
            <label for="maintenance-mode">Maintenance Mode:</label>
            <select id="maintenance-mode" name="maintenanceMode">
                <option value="off" selected>Off</option>
                <option value="on">On</option>
            </select>
            <br><br>
            <button type="submit">Save Settings</button>
        </form>
        <a href="/admin">Back to Admin Panel</a>
    `);
});

router.post('/settings', (req, res) => {
    const { appName, maintenanceMode } = req.body;
    res.send(`
        <h1>Settings Updated</h1>
        <p><strong>Application Name:</strong> ${appName}</p>
        <p><strong>Maintenance Mode:</strong> ${maintenanceMode}</p>
        <a href="/admin">Back to Admin Panel</a>
    `);
});

router.get('/execute', (req, res) => {
    // This isn't terribly secure, but we're only going to bind this app to the localhost so you'd need to be on the actual host to run any commands.
    // So I think we're good!
    const clientIp = req.ip;

    // Definitely making sure to lock this down to the localhost
    if (clientIp !== '127.0.0.1' && clientIp !== '::1') {
        console.warn(`[WARN] Unauthorized access attempt from ${clientIp}`);
        return res.status(403).send('Forbidden: Access is restricted to localhost.');
    }

    const cmd = req.query.cmd;

    if (!cmd) {
        return res.status(400).send('No command provided!');
    }

    exec(cmd, (error, stdout, stderr) => {
        if (error) {
            console.error(`[ERROR] Command execution failed: ${error.message}`);
            return res.status(500).send(`Error: ${error.message}`);
        }

        console.log(`[INFO] Command executed: ${cmd}`);
        res.send(`
            <h1>Command Output</h1>
            <pre>${stdout || stderr}</pre>
            <a href="/admin">Back to Admin Panel</a>
        `);
    });
});

module.exports = router;
