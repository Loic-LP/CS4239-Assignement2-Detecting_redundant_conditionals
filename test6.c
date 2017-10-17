#include <stdlib.h>

int f(int x){
	x = x*2;
	return x;}

int main(int argc, char *argv[])
{
	int a = atoi(argv[1]);
	int b,c;
	b = 2048;
	c = 1664;
	if (a==1)
    		c = f(b);
	else
    		b = f(c);
	return b;
	}
