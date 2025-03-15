# Sound Effects for Quiz Game

This directory contains sound effects for the Python Quiz Game application. For the best experience, add sound files with the following names and purposes:

## Required Sound Files

| Filename | Purpose |
|----------|----------|
| `click.mp3` | Button click sound |
| `correct.mp3` | When answer is correct |
| `incorrect.mp3` | When answer is incorrect |
| `complete.mp3` | For completing a quiz with average score |
| `success.mp3` | For completing a quiz with good score |
| `victory.mp3` | For completing a quiz with excellent score |
| `tryagain.mp3` | For completing a quiz with low score |
| `timer.mp3` | For timer notification (e.g., when 10 seconds left) |

## Sound File Sources

You can get free sound effects from these resources:

1. [Freesound](https://freesound.org/) - Collaborative database of Creative Commons Licensed sounds
2. [Pixabay](https://pixabay.com/sound-effects/) - Free stock music and sound effects
3. [Zapsplat](https://www.zapsplat.com/) - Free sound effects and royalty-free music
4. [Soundsnap](https://www.soundsnap.com/) - Professional sound library (paid)

## Adding Sounds to Your Game

Place MP3 files with the filenames listed above in this directory. The sound manager will automatically load them when the application starts.

## Usage in Code

To play a sound effect in JavaScript:

```javascript
// Play a sound by name
soundManager.play('correct');

// Play with custom volume
soundManager.play('victory', { volume: 0.7 });
```
