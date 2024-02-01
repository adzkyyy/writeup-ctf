// gcc source.c -fno-stack-protector -s -o uBof

#include <stdio.h>
#include <stdlib.h>

void setup() {
	setvbuf(stdout, NULL, _IONBF, 0);
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stderr, NULL, _IONBF, 0);
}

void win(){
	system("cat flag.txt");
}

int main(){
    char buffer[64];
    int len_input;
    setup();

    printf("Masukkan panjang pesan yang akan dikirim: ");
    scanf("%d\n",&len_input);

    if ((len_input < 1 || len_input > 50)){
        len_input = 105;
    }
    
    fread(buffer, len_input, 1, stdin);
    printf("Pesanmu terkirim!\n");
    return 0;
}