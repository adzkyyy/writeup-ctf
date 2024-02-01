// gcc source.c -Wl,-z,relro,-z,now -fPIE -pie -o uNote
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

#define NOTE_SIZE 32

char *note;

void setup() {
	setvbuf(stdout, NULL, _IONBF, 0);
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stderr, NULL, _IONBF, 0);
}

void print_menu(){
    char *menu[6] = {
        "--- Selamat datang di aplikasi pencatatan ---",
        "Silahkan pilih salah satu menu di bawah ini:",
        "[1] Tambah catatan",
        "[2] Hapus catatan",
        "[3] Lihat catatan",
        "[4] Keluar"
    };
    for (int i = 0; i < 6; i++){
        printf("%s\n",menu[i]);
    }
}

int getnline(char *buf, int size)
{
    char *lf;

    if (size < 0)
        return 0;

    fgets(buf, size, stdin);
    if ((lf = strchr(buf, '\n')))
        *lf = '\0';

    return 1;
}

unsigned int read_int()	{
   char buf[16];
   fgets(buf, 16, stdin);
   return strtoul(buf, NULL, 10);
}

void tambah(void)
{
    if (!(note = (char *)malloc(NOTE_SIZE)))
    {
        puts("Gagal membuat catatan");
        return;
    }

    printf("Masukkan isi catatan > ");
    getnline(note, NOTE_SIZE);
}

void tampil(void)
{
    if (!note)
    {
        puts("Catatan tidak ada!");
        return;
    }

    puts(note);
}

void hapus(void)
{
    if (!note)
    {
        puts("Catatan tidak ada!");
        return;
    }

    free(note);
}

int main(){
    unsigned int pilih;
    setup();

    for (;;){
        print_menu();
        pilih = read_int();
        if (pilih == 1){
            tambah();
        } else if (pilih == 2){
            hapus();
        } else if (pilih == 3){
            tampil();
        } else {
            if (pilih == 4){
                puts("Bye!");
				exit(0);
				break;
            }
            printf("Pilihan salah!\n");
        }
    }
}