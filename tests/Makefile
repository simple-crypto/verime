test: build-pack compile-pack
	@echo "############"
	@echo "# Run test #" 
	@echo "############"
	@echo ""
	./my_funky_exec

build-pack:
	@echo "#################"
	@echo "# Build package #" 
	@echo "#################"
	@echo ""
	python3 -m verime.verilator_me -y srcs -top srcs/top.v --pack my_funky_lib

compile-pack:
	@echo "###################"
	@echo "# Compile package #" 
	@echo "###################"
	@echo ""
	python3 -m verime.verilator_me --pack my_funky_lib -cpp test_main.cpp --exec my_funky_exec

clean:
	if [ -d my_funky_lib ]; then rm -r my_funky_lib; fi
	if [ -e my_funky_exec ]; then rm my_funky_exec; fi
	if [ -e test.save ]; then rm test.save; fi
