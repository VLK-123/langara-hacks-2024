app.post('/login', (req, res) => {
  const { username, password } = req.body;
  console.log(`Login attempt for username: ${username}`); // Log the username

  db.get('SELECT * FROM users WHERE username = ? AND password = ?', [username, password], (err, row) => {
      if (err) {
          console.error(err);
          return res.status(500).json({ error: 'Internal server error' });
      }

      if (!row) {
          console.log('Invalid username or password'); // Log invalid attempt
          return res.status(401).json({ error: 'Invalid username or password' });
      }

      console.log('Login successful'); // Log successful login
      res.status(200).json({ message: 'Login successful', redirectUrl: '/main.html' });
  });
});