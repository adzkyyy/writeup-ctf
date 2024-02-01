//  gcc source.c -s -o usystem

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

int getnline(char *buf, size_t n) {
    for (int i = 0; i < n; i++) {
        if (read(0, &buf[i], 1) != 1) {
            exit(1);
        }
        if (buf[i] == '\n') {
            buf[i] = '\0';
            return i;
        }
    }
    return n;
}

void setup(){
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

int main(void) {
    setup();
    struct dbs {
    char name[0x20];
    char password[0x20];
    char buf[0x20];
    } db;
    size_t n;
    
start:
    puts("Buat akun dulu bro.");
    printf("Panjang nama: ");
    scanf("%lu", &n);
    getchar();
    if (n > 0x1f) {
        puts("Panjang bener nama lu!");
        goto start;
    }
    
    printf("Tulis nama lu: ");
    getnline(db.name, n);
    printf("kata sandi: ");
    getnline(db.password, 0x20);

    puts("Akun berhasil dibuat. Masukkan ulang kata sandi.");
    printf("kata sandi: ");

    read(0, db.buf, strlen(db.password));
    db.buf[strlen(db.password)] = '\0';
    if (strcmp(db.password, db.buf) != 0) {
        puts("Bruhh??");
        printf("Gagal login pake password %s!\n",db.buf);
        goto start;
    }
    puts("Berhasil Login.");
    printf("Ga ada apa-apa. Mau logout? (y/n) ");
    char pilihan;
    scanf("%1s",&pilihan);
    switch (pilihan)
    {
    case 'n':
        goto start;
        break;
    default:
        return 0;
    }
}
