# Python_Project

Pacman Replica Game

MEMBERS: James Kerrigan, Artir Hyseni, Ike George, Abigail Mortensen

PROJECT: We have created a pacman replica game. We picked pacman because it allowed us to explore a variety of interesting elements while also helping us develop our Python coding skills.
These elements are: Functional player controls, fully generated 2D graphical-board using matrixes, functional AI, a graphical user interface, using input/output functions for scoring, and game-level creation.

LIBRARIES & RESOURCES: Pygame is used throughout the whole project including the user interface. Other then that, we stuck to Python's default libraries such as Python Math.

DIRECTIONS: Player controlling requires using the keyboard. Using the arrow keys; up, down, left and right will guide Pac-Man through the maze. 
Collect the dots and avoid the ghosts to complete each level and obtain a highscore. When the player loses all their lives, the game ends and the player is brought back to the beginning of the game.

HOW THE WORK WAS SPLIT:

James Kerrigan: Worked on the base framework of the game. Developed the board, the in-game graphics (board, player, enemies), the player controller and player logic. Overall, worked on many different
elements of the project up till the game was in a playable-state, which allowed other members to easily append their code to. Primarily worked within game.py

Abigail Mortensen: Worked on enemy AI and pathing. Developed two complex ghost behaviors which chased the player controller character, thus adding difficulty to the overall game. Primarily worked
within ghosts.py with some additions to game.py

Artir Hyseni: Worked on the graphical user interface; the start and game-over screen. Encapsulated the primary class into a class of its own, allowing ease of control when creating new game instances.
Primarily worked within introScreen.py & gameOver.py

Ike George: Worked on the graphical user interface, as well as many different elements including level design. Polished the game by adding score display, level design/colors , and placed together scoring
output to file. Primarily worked within introScreen.py & gameOver.py & game.py

