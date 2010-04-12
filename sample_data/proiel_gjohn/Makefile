all: programme

text: parse-proiel.py gnt-greeknt.xml
	./parse-proiel.py gnt-greeknt.xml > text

clauses: build-clauses.py text
	./build-clauses.py text > clauses

target-item: make-target-item.py clauses
	./make-target-item.py clauses > target-item

programme: ../../code/next-best.py ../../code/optimize-order.py add-back-clauses.py target-item clauses
	../../code/next-best.py target-item > tmp1
	../../code/optimize-order.py tmp1 target-item > tmp2
	./add-back-clauses.py clauses tmp2 > programme
	rm tmp1 tmp2

clean:
	rm -f text clauses tmp1 tmp2 target-item