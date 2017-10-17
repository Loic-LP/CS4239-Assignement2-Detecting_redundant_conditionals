#include <stdlib.h>

int f(int x){
	x=x+2;
	return x;}

int main(int argc, char *argv[])
{
	int a = atoi(argv[1]);
	int b,c,d;
	b=12;
	if (a==1){
    		b = f(b);
		c = f(19);}
	else{
		b = f(b);}
	return b;}
