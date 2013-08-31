all: programme

target-item: make_ti.py
	./make_ti.py > target-item

targets: make_targets.py
	./make_targets.py > targets

tmp1: ../../code/next-best.py target-item
	../../code/next-best.py target-item > tmp1

tmp2: ../../code/optimize-order.py tmp1 target-item
	../../code/optimize-order.py tmp1 target-item > tmp2

programme: ./add_back_targets.py targets tmp2
	./add_back_targets.py targets tmp2 > programme

clean:
	rm -f tmp1 tmp2 targets target-item
