const form = document.getElementById('signupForm');

form.addEventListener('submit', async (event) => {
  event.preventDefault();

  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;

  try {
    const response = await fetch('/signup', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ username, password })
    });

    if (response.ok) {
      const { message } = await response.json();
      alert(message);
      window.location.href = 'login.html';
    } else {
      const { error } = await response.json();
      alert(error);
    }
  } catch (error) {
    console.error(error);
    alert('An error occurred. Please try again later.');
  }
});