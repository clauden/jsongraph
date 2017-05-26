

default:
	python y.py
	cat out.dot |dot -Tpng -occc.png
	open ccc.png 


