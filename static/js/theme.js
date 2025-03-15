/**
 * Theme manager for Quiz Game
 */
document.addEventListener('DOMContentLoaded', () => {
  // Get the theme toggle button
  const themeToggle = document.getElementById('theme-toggle');
  
  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      // Get current theme
      const currentTheme = document.body.getAttribute('data-theme') || 'light';
      const newTheme = currentTheme === 'light' ? 'dark' : 'light';
      
      // Update icon
      const themeIcon = themeToggle.querySelector('.theme-icon');
      if (themeIcon) {
        // Replace the icons using Bootstrap icons
        if (newTheme === 'dark') {
          themeIcon.innerHTML = '<i class="bi bi-moon-fill"></i>';
        } else {
          themeIcon.innerHTML = '<i class="bi bi-sun-fill"></i>';
        }
      }
      
      // Save preference via AJAX
      fetch('/toggle-theme', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ theme: newTheme })
      }).then(response => {
        if (response.ok) {
          // Update the body attribute
          document.body.setAttribute('data-theme', newTheme);
        }
      }).catch(error => {
        console.error('Error toggling theme:', error);
      });
    });
  }
});
