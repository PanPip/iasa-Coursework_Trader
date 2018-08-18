# iasa-Coursework_Trader
My coursework on the third year of Bachelor's studies. 

## Task:

The idea was to use this project as a foundation: https://github.com/yanpanlau/Keras-FlappyBird
And then try to learn a Neural Network architecture used by DeepMind to trade Forex.
The same architecture was used to learn NN to play Atari games using only the image output of the game.
This was a try to solve the trading task using reinforced learning.

I was not keen at NN at that time, so the project wasn't a success.
Basically, I wrote a game that was outputting a spectrogram using Fourier transformation for every new frame.
I've also added a line of pixels to the game interface, indicating the current situation on the marketplace.
So, the NN could learn the states of the game.
Only three states were possible:
- short position
- no positions open
- long position

The NN was allowed to do two actions on every new frame:
- buy
- sell
- do nothing

If the position was "short" and the NN decided to "buy", position switched to "no positions open".
This allowed to keep the program simple.

As it is a reinforcement learning model, NN relieved positive or negative points depending on the change in the money balance.

Unfortunately, the part with generating spectrograms is not available, as was developed by my peers.
Though, it's code and description is available in the Coursework file.

![sample](images/img03.PNG)

![sample](images/img02.PNG)

![sample](images/img01.PNG)

Year - 2017
