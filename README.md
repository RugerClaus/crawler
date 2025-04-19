LICENSE: 

Hello one and all. 

To play, you'll need to be running at the very least python 3.10, but you'll get some errors with the way I'm handling strings

The f strings only use "" double quotes even on the inside. You'll have to find and replace all of that if you want to use 3.10.

Python 3.12 couldn't care less

So be on 3.12 probably.

Anyway, you'll need to ensure you have pygame-ce installed and then running from the root directory ``` python main.py ``` or if you're using python3 on 
linux ``` python3 main.py ```.

Control keys are WASD. You can't interact with any objects besides bumping into walls. You can take damage from the spike that spawns below the player however.
So that's fun. I'm finally pulling some mechanics together. 

Press F9 for debug

Press F5 to damage the player by 1 HP