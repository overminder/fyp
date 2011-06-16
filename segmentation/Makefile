LBITS := $(shell getconf LONG_BIT)
ifeq ($(LBITS),64)
test.so: c_demo.cc ICTCLAS50.h
		g++ -g c_demo.cc `pwd`/libICTCLAS50_64.so  -m64  -O3 -DOS_LINUX -fPIC -shared -o test.so
else
test.so: c_demo.cc ICTCLAS50.h
		g++ -g c_demo.cc `pwd`/libICTCLAS50_32.so  -m32  -O3 -DOS_LINUX -fPIC -shared -o test.so
	    
endif
