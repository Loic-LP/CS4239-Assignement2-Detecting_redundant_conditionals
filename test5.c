#include <stdlib.h>

int f(int x){
	x=x+2;
	return x;}

int g(int x){
	x=x*42;
	return x;}

int main(int argc, char *argv[])
{
	int a = atoi(argv[1]);
	int b,c,d;
	b=12;
	if (a==1){
		c = 42;
    		b = f(g(b));}
	else{
		b = f(g(b));
		d = 16;}
	return b;}
