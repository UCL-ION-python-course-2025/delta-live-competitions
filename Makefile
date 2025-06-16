pretty: black

pc:
	pre-commit run --all

black:
	black .

test:
	PYTHONPATH=`pwd`/src pytest .

connect-4:
	PYTHONPATH=`pwd`/src python src/connect4/main.py

pong:
	PYTHONPATH=`pwd`/src python src/pong/main.py

snake:
	PYTHONPATH=`pwd`/src python src/snake/main.py

tictactoe:
	PYTHONPATH=`pwd`/src python src/tictactoe/main.py

pathfinder:
	PYTHONPATH=`pwd`/src python src/pathfinder/main.py

2048:
	PYTHONPATH=`pwd`/src python src/twenty_forty_eight/main.py

wordle:
	PYTHONPATH=`pwd`/src python src/wordle/main.py

stock-market:
	PYTHONPATH=`pwd`/src python src/stock_market/main.py

wild-tic-tac-toe:
	PYTHONPATH=`pwd`/src python src/wild_tictactoe/main.py

wttt : wild-tic-tac-toe

othello:
	PYTHONPATH=`pwd`/src python src/othello/main.py

poker:
	PYTHONPATH=`pwd`/src python src/poker/main.py

tron:
	PYTHONPATH=`pwd`/src python src/tron/main.py

go:
	PYTHONPATH=`pwd`/src python src/go/main.py

space-shooter:
	PYTHONPATH=`pwd`/src python src/shooter/main.py
