main:
	verilator -y work/an-srcs/ --cc --exe --build work/an-srcs/top.v test_main.cpp build/my_funky_lib.cpp 

clean:
	if [ -d obj_dir ]; then rm -r obj_dir; fi
	if [ -d build ]; then rm -r build; fi
	if [ -d work ]; then rm -r work; fi
