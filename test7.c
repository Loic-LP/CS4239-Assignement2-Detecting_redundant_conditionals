#include <stdlib.h>
#include "stdio.h"

int f(int x){
	x = x*2;
	return x;}

int main(int argc, char *argv[])
{
	int a = atoi(argv[1]);
	int b;
	int c = 1664;
	if (a==1){
		b = a + 42;
		printf("Hello!!!");}
	else{
		c = c - 64;
		printf("Hello!!!");}
	return b;
	}
