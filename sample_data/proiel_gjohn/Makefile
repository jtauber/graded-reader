all: programme

text: parse-proiel.py gnt-greeknt.xml
	./parse-proiel.py gnt-greeknt.xml JOHN > text

targets: build-targets.py text
	./build-targets.py text > targets

target-item: make-target-item.py targets
	./make-target-item.py targets > target-item

programme: ../../code/next-best.py ../../code/optimize-order.py add-back-targets.py target-item targets
	../../code/next-best.py target-item > tmp1
	../../code/optimize-order.py tmp1 target-item > tmp2
	./add-back-targets.py targets tmp2 > programme
	rm tmp1 tmp2

clean:
	rm -f text targets tmp1 tmp2 target-item