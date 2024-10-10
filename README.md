# Space Shooter - A Pygame Space Shooter Game

## Description

**Space Shooter** is an action-packed space shooter game built using Pygame. Players control a spaceship to navigate through space, avoid meteors, and shoot them down using lasers. The game features exciting mechanics such as power-ups, enemy collisions, and an ever-increasing difficulty as time progresses.

## Features

- **Player Control**: Navigate the spaceship using keyboard inputs.
- **Shooting Mechanics**: Fire lasers at incoming meteors.
- **Power-ups**: Collect special items that enhance player speed or shooting rate.
- **Dynamic Difficulty**: As the player progresses, the game speed increases, making it more challenging.
- **Explosions and Visual Effects**: Experience visually appealing explosions when destroying meteors.
- **Game Over Screen**: View statistics such as the number of meteors crashed and final score upon game over.

## How to Play
- Start the Game: Press F to start the game from the main menu.
- Controls:
  - Use W, A, S, D to move the spaceship.
  - Press SPACE to shoot lasers.
- Collect Power-ups: Shoot down meteors to collect special items that enhance your abilities.
- Avoid Collisions: Avoid colliding with meteors to prevent game over.
- Game Over: View your score and statistics upon crashing.
## Code Structure
### Classes:  
- Player: Manages player actions including movement and shooting.
- Laser: Represents the laser shot by the player.
- Meteor: Represents the meteors falling from the top of the screen.
- Explosion: Handles explosion animations upon meteor destruction.
- Special_item: Manages the special power-up items.
- Star: Background stars for enhanced visual effects.
### Functions:
- collisions(): Checks for collisions between player, meteors, and special items.
- display_score(): Renders the current score on the screen.
- game_over(): Displays the game over screen with statistics.
- menu(): Displays the main menu.
- speeding_game(): Increases the game speed as time progresses.
## Acknowledgments
This project is based on the YouTube tutorial series "Master Python by Making 5 Games [The New Ultimate Introduction to Pygame]".  
A special thanks to the creator for providing valuable resources and guidance.  
Special thanks to the Pygame community for their resources and support.  
Game assets (images, sounds) used in the project are sourced from various free resources.  
