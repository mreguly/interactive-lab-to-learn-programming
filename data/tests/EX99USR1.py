import sys, os
sys.stdout = open(os.devnull, 'w')
#include <stdio.h>
int main() {
printf("Hello World");
}
sys.stdout = sys.__stdout__