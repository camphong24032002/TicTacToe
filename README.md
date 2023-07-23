# TicTacToe
TicTacToe game app using alpha-beta pruning algorithm to build up. `Game` class is used to process the game execution. `Screen` class uses pygame to build GUI. 
## Setting up
Create the virtual environment by the following steps
```bash
python3 -m venv <venv_name>
```

To activate
- On Window
```bash
.\venv\Scripts\activate
```

- On macOS and Linux:
```bash
source venv/bin/activate
```

Once the virtual environment is activated, install packages `requirements.txt`
```bash
pip install -r requirements.txt
```

To deactivate, use
```bash
deactivate
```

## Run
Run file `main.py` to play 
```bash
python main.py
```

## Algorithms
### Idea
-	Utilizing alpha-beta pruning algorithm to build AI Bot
-	To find max score of move function, I compute the score that makes AI’s move get highest opportunity to win. During calculating, if the alpha value is greater than or equal to beta, the alpha value is returned, vice versa.
-	To check if the game is end, I implement the winPos array to save all situation that makes the game finish and use loop to check.
-	To optimize running time, we use a heuristic to calculate the score when the step depth is 0. For efficient execution, the depth value should be even, as the heuristic function is called in the "maxValue" function to facilitate AI's moves.
-	The heuristic value is calculated by the chance AI will win minus AI will lose and priority to how many steps that are satisfied the winPos
-	For AI's next move, the value and position are derived from the "maxValue" function.
### Time/space complexity:
O(bd/2)

## Demo
https://youtu.be/Vmo-mhMpqIw
