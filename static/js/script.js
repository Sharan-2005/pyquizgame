// Global variable for sound manager reference
let globalSoundManager;

document.addEventListener('DOMContentLoaded', function() {
    // Initialize global sound manager reference
    if (window.soundManager) {
        globalSoundManager = window.soundManager;
    }
    
    // Initialize timer if on quiz page
    initQuizTimer();
    
    // Initialize settings page functionality
    initSettingsPage();
});

// Quiz timer initialization
function initQuizTimer() {
    const timerDisplay = document.getElementById('time-display');
    if (!timerDisplay) return;
    
    const progressBar = document.getElementById('progress-bar');
    const timeLimit = parseInt(timerDisplay.getAttribute('data-time-limit') || 300); // Default 5 minutes
    let timeLeft = timeLimit;
    
    function updateTimer() {
        const minutes = Math.floor(timeLeft / 60);
        const seconds = timeLeft % 60;
        
        // Format the time display (adding leading zeros if needed)
        timerDisplay.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        
        // Update progress bar
        if (progressBar) {
            const progressPercent = ((timeLimit - timeLeft) / timeLimit) * 100;
            progressBar.style.width = `${progressPercent}%`;
            
            // Change progress bar color based on time left
            if (timeLeft <= 60) { // Last minute
                progressBar.style.backgroundColor = 'var(--danger-color)';
            }
        }
        
        // Change color and add pulse effect in last minute
        if (timeLeft <= 60) { // Last minute
            timerDisplay.style.color = 'var(--danger-color)';
            timerDisplay.classList.add('pulse');
            
            // Play tick sound in last 10 seconds
            if (timeLeft <= 10 && globalSoundManager) {
                globalSoundManager.play('timer', { volume: 0.2 });
            }
        }
        
        if (timeLeft <= 0) {
            clearInterval(timerInterval);
            if (globalSoundManager) globalSoundManager.play('tryagain');
            
            // Auto-submit the quiz when time is up
            const quizForm = document.getElementById('quiz-form');
            if (quizForm) {
                setTimeout(() => quizForm.submit(), 500);
            }
        } else {
            timeLeft--;
        }
    }
    
    // Initial call to set up display
    updateTimer();
    
    // Update timer every second
    const timerInterval = setInterval(updateTimer, 1000);
}

// Settings page functionality
function initSettingsPage() {
    // Check if we're on the settings page
    const settingsContainer = document.querySelector('.settings-container');
    if (!settingsContainer) return;
    
    // Handle toggle switches
    const toggleSwitches = document.querySelectorAll('.toggle-switch input[type="checkbox"]');
    toggleSwitches.forEach(toggle => {
        // Update toggle status text on initialization
        updateToggleStatus(toggle);
        
        // Add event listener for change
        toggle.addEventListener('change', function() {
            updateToggleStatus(this);
        });
    });
    
    // Password validation
    const newPasswordInput = document.getElementById('new_password');
    const confirmPasswordInput = document.getElementById('confirm_password');
    
    if (newPasswordInput && confirmPasswordInput) {
        // Check password match on input
        confirmPasswordInput.addEventListener('input', function() {
            validatePasswordsMatch(newPasswordInput, confirmPasswordInput);
        });
        
        // Also check when new password changes
        newPasswordInput.addEventListener('input', function() {
            if (confirmPasswordInput.value) {
                validatePasswordsMatch(newPasswordInput, confirmPasswordInput);
            }
        });
        
        // Form validation before submit
        const passwordForm = confirmPasswordInput.closest('form');
        if (passwordForm) {
            passwordForm.addEventListener('submit', function(e) {
                // Check if passwords match
                if (newPasswordInput.value !== confirmPasswordInput.value) {
                    e.preventDefault();
                    alert('Passwords do not match!');
                    return false;
                }
                
                // Check password length
                if (newPasswordInput.value.length < 8) {
                    e.preventDefault();
                    alert('Password must be at least 8 characters long!');
                    return false;
                }
                
                return true;
            });
        }
    }
}

// Update toggle status text based on checkbox state
function updateToggleStatus(toggleInput) {
    const toggleContainer = toggleInput.closest('.toggle-container');
    if (!toggleContainer) return;
    
    const statusElement = toggleContainer.querySelector('.toggle-status');
    if (statusElement) {
        statusElement.textContent = toggleInput.checked ? 'Enabled' : 'Disabled';
        statusElement.style.color = toggleInput.checked ? 'var(--success-text)' : 'var(--error-text)';
    }
}

// Validate that new password and confirm password match
function validatePasswordsMatch(newPassElem, confirmPassElem) {
    if (newPassElem.value !== confirmPassElem.value) {
        confirmPassElem.setCustomValidity('Passwords do not match');
    } else {
        confirmPassElem.setCustomValidity('');
    }
}
