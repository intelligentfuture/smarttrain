#include<stdio.h>
int main(){

    int sum = 1+3+2;
    sum = 256-sum;
    char *modbuscode;
    sprintf(modbuscode,":%02X%02X%02X%06X%02X\r\n",1,3,0,2,sum);
    printf("%s\n",modbuscode);
return 0;
}
