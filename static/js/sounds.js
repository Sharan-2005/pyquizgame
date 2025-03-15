/**
 * Sound effects manager for Quiz Game
 */
class SoundManager {
  constructor() {
    this.sounds = {};
    this.muted = false;
    this.initialized = false;
  }

  /**
   * Initialize with default sounds
   */
  init() {
    if (this.initialized) return;

    // Register default sounds
    this.register('click', '/static/sounds/click.mp3');
    this.register('timer', '/static/sounds/timer.mp3');
    this.register('victory', '/static/sounds/victory.mp3');
    this.register('tryagain', '/static/sounds/tryagain.mp3');
    this.register('complete', '/static/sounds/complete.mp3'); // fallback to existing files if these don't exist
    this.register('success', '/static/sounds/success.mp3'); // fallback to existing files if these don't exist
    
    // Check if sound should be muted based on user preference
    const soundEnabled = document.body.getAttribute('data-sound-enabled');
    this.muted = soundEnabled === 'false';
    
    this.initialized = true;
  }

  /**
   * Register a new sound
   */
  register(name, src) {
    const audio = new Audio(src);
    audio.preload = 'auto';
    this.sounds[name] = audio;
    return audio;
  }

  /**
   * Play a sound by name
   */
  play(name, options = {}) {
    if (this.muted) return;
    
    const sound = this.sounds[name];
    if (!sound) return;
    
    // Clone the audio to allow multiple plays
    const soundInstance = sound.cloneNode();
    
    // Apply options
    if (options.volume !== undefined) {
      soundInstance.volume = options.volume;
    }
    
    if (options.loop) {
      soundInstance.loop = true;
    }
    
    soundInstance.play().catch(err => {
      console.log('Error playing sound:', err);
    });
    return soundInstance;
  }

  /**
   * Stop a currently playing sound
   */
  stop(soundInstance) {
    if (soundInstance && typeof soundInstance.pause === 'function') {
      soundInstance.pause();
      soundInstance.currentTime = 0;
    }
  }

  /**
   * Toggle mute state
   */
  toggleMute() {
    this.muted = !this.muted;
    return this.muted;
  }

  /**
   * Set mute state
   */
  setMuted(muted) {
    this.muted = muted;
  }
}

// Create a global instance
window.soundManager = new SoundManager();

// Initialize the sound manager when the page loads
document.addEventListener('DOMContentLoaded', () => {
  // Initialize the global soundManager instance
  window.soundManager.init();
  
  // Setup sound toggle button if it exists
  const soundToggle = document.getElementById('sound-toggle');
  if (soundToggle) {
    soundToggle.addEventListener('click', () => {
      const muted = window.soundManager.toggleMute();
      
      // Update icon
      const soundIcon = soundToggle.querySelector('.sound-icon');
      if (soundIcon) {
        // Replace the icons using Bootstrap icons
        if (muted) {
          soundIcon.innerHTML = '<i class="bi bi-volume-mute-fill"></i>';
        } else {
          soundIcon.innerHTML = '<i class="bi bi-volume-up-fill"></i>';
        }
      }
      
      // Save preference via AJAX
      fetch('/toggle-sound', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ muted })
      });
    });
  }
  
  // Add sound effects to buttons
  document.querySelectorAll('button:not(.no-sound), .btn:not(.no-sound)').forEach(button => {
    button.addEventListener('click', () => {
      window.soundManager.play('click', { volume: 0.5 });
    });
  });
});
