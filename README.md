 # FIGHTER BALL_Z
## Video Demo: <https://youtu.be/zGy9yJKzDJk>

**Introduction:** Dragon Ball is a Japanese media franchise created by Akira Toriyama in 1984.
The initial manga, written and illustrated by Akira Toriyama, was serialized in Weekly Shōnen Jump from 1984 to 1995.
Since its release, Dragon Ball has become one of the most successful manga and anime series of all time.
It was the one we have watched and were inspired by during our childhood and hence we decided to make a game dedicated 
to the series using pygame.

**Description:** We have used pygame to make a Player versus Player(PvP) Fighting game featuring the 2 most beloved
dragon ball characters from the series _Goku and Vegeta_.
Our project has 4 files.

### Start_Screen.py
It contains the code for the start screen of our game. In it, we initialized pygame, set the screen size, 
loaded some assets like background music and image. Then a class called `Text` was created to display and select the
text on the start screen i.e. _Start, Options and Exit_. Then a sprite list and a function called `animate`is created 
for the transition effect on pressing enter on the aforementioned buttons. Then another list is created to contain the 
images of dragon balls(another prevalent item from the series and are 7 in number). Then a class called `LinearMovement` 
is created to handle the movement of the dragon balls on the start screen. It handles the spawning, movement and 
respawning and error checking of the dragon balls. The lines of code _87 to 97_ handle the randomisation of the sizes 
of the 7 dragon balls. The background is also loaded and animated in the following lines of code.

Finally, after all this the game loop is initialized with the `while` loop. The `while` loop contains the code for the 
drawing of the background on the game window along with the dragon balls and more importantly the code to exit the program 
as needed so that the loop doesn't remain running endlessly.

### player.py
It is the file that contains all the code for the functioning of the game.

#### Class `Player`
A class aptly named `Player` was created to basically handle everything concerning both the players. Firstly the keyboard 
keys used to control both the players are added to a list. After that the sounds related to the player actions were loaded 
and put into a list. These were the class variables for the `Player` class. A class method called `target_setter` was then 
created to set the targets of player to its respective opponent. Another class method called `check_hit` is defined to well 
check if the player was hit by using masks and collision detection and what to do if it was indeed hit.

Now, the class was initialized with many arguments containing various aspects of the player like the position data, length, 
breadth etc. for the player. Then within the initialisation the sprites of the various actions and movements of the player 
were stored in a dictionary called `sprite_dict` having the action name as key and the action frames/ images as values 
to be used later.

Various functions were created within the class to formulate and control the functioning of the player. The instance method 
`move` handled the movement of the player along with the jumping too. Then the method `move_and_keys` was defined to check 
if a mapped key is pressed and what to do if it is actually pressed. The method `attacks` changes the current state of player 
based on the key combination(s) pressed. It also contains the damage values of different attacks along with the energy meter 
depletion rate for the special attacks(The energy meter is called ki_bar in our file). The method `drawer` draws all images 
and sprites on the game window and the method `animate` utilizes the sprite_dict's keys and current index to determine the 
player image and animates it as per the current iteration of the loop. The `reset` method brings the player back to its "idle" 
state after each action is finished. `turn` ensures that the players and their attacks always face each other. The `blast` 
method creates an energy projectile(ki_blast as in the game terms) and adds it to the list of projectiles for each player. 
Then finally the `loop` method calls all the aforementioned methods in every iteration of the while loop.

#### Class `KiBlast`
This class handles all the ki_blast projectile related attacks. It handles their creation, movement, collision and type.
It follows a similar pattern as the `Player` class but specialized towards projectile attacks. This also handles the players' 
special attacks using the `special` method.

The rest of the code contains the game loop and its requirements as in the start_screen.py file.

### project.py
This file calls the files mentioned above in a seamless fashion bringing together the start screen and the actual game itself.
