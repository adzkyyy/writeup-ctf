// gcc source.c -static -s -fno-stack-protector -no-pie -o ucalc

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct pls {
  unsigned int _0;
  unsigned int _4;
  long long _8;
} plu;

struct mnx {
  unsigned int _0;
  unsigned int _4;
  long long _8;
} mns;

struct kls {
  unsigned int _0;
  unsigned int _4;
  long long _8;
} klx;

struct bag {
  unsigned int _0;
  unsigned int _4;
  long long _8;
} bgi;

void setup() {
	setvbuf(stdout, NULL, _IONBF, 0);
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stderr, NULL, _IONBF, 0);
}

void handle_newline(void)

{
  int iVar1;
  
  do {
    iVar1 = getchar();
    if ((char)iVar1 == '\n') {
      return;
    }
  } while ((char)iVar1 != -1);
  return;
}

void print_menu(void){ 
    printf("Menu: \n[1] Tambah.\n[2] Kurang.\n[3] Kali.\n[4] Bagi.\n[5] Simpan dan keluar.\n=> ");
}

void plus(void){
  printf("Nilai x: ");
  scanf("%d",&plu._0);
  handle_newline();
  printf("Nilai y: ");
  scanf("%d",&plu._4);
  handle_newline();
  if ( (plu._0 > 100) && (plu._4 > 100) )
  {
    plu._8 = plu._4 + plu._0;
    printf("Hasil dari x + y adalah %d.\n\n",plu._8);
    return;
  }
  printf("1:%d 2:%d",plu._0,plu._4);
  printf("%d",(plu._0 > 39));
  printf("%d",(plu._4 > 39));
  printf("Broo, masa nilai segitu lu butuh kalkulator?\nKocakkk... Bye!");
  exit(-1);
}

void minus(void){
  printf("Nilai x: ");
  scanf("%d",&mns._0);
  handle_newline();
  printf("Nilai y: ");
  scanf("%d",&mns._4);
  handle_newline();
  if ( (mns._0 > 100) && (mns._4 > 100) )
  {
    mns._8 = mns._0 - mns._4;
    printf("Hasil dari x - y adalah %d.\n\n",mns._8);
    return;
  }
  printf("Broo, masa nilai segitu lu butuh kalkulator?\nKocakkk... Bye!");
  exit(-1);
}

void kali(void){
  printf("Nilai x: ");
  scanf("%d",&klx._0);
  handle_newline();
  printf("Nilai y: ");
  scanf("%d",&klx._4);
  handle_newline();
  if ( (klx._0 > 100) && (klx._4 > 100) )
  {
    klx._8 = klx._4 * klx._0;
    printf("Hasil dari x * y adalah %d.\n\n",klx._8);
    return;
  }
  printf("Broo, masa nilai segitu lu butuh kalkulator?\nKocakkk... Bye!");
  exit(-1);
}

void bagi(void){
  printf("Nilai x: ");
  scanf("%d",&bgi._0);
  handle_newline();
  printf("Nilai y: ");
  scanf("%d",&bgi._4);
  handle_newline();
  if ( (bgi._0 > 100) && (bgi._4 > 100) )
  {
    bgi._8 = bgi._0 / bgi._4;
    printf("Hasil dari x / y adalah %d.\n\n",bgi._8);
    return; 
  }
  printf("Broo, masa nilai segitu lu butuh kalkulator?\nKocakkk... Bye!");
  exit(-1);
}

int main(){
    setup();
    unsigned char store[32];
    int pilih_menu;
    int banyaknya_perhitungan = 0;
    long *stored_result;
    int index;

    printf("Mau berapa kali ngitung? ");
    scanf("%d",&banyaknya_perhitungan);
    handle_newline();
    if ((banyaknya_perhitungan < 256) && (3 < banyaknya_perhitungan)){
        stored_result = malloc(banyaknya_perhitungan << 2);
        for (index = 0; index < banyaknya_perhitungan; index++)
        {
            print_menu();
            scanf("%d",&pilih_menu);
            handle_newline();
            
            if (pilih_menu == 1) {
                plus();
                stored_result[index] = plu._8;
            } else if (pilih_menu == 2) {
                minus();
                stored_result[index] = mns._8;
            } else if (pilih_menu == 3) {
                kali();
                stored_result[index] = klx._8;
            } else if (pilih_menu == 4) {
                bagi();
                stored_result[index] = bgi._8;
            } else {
                if (pilih_menu == 5) {
                    memcpy(store,stored_result,banyaknya_perhitungan << 2);
                    free(stored_result);
                    return 0;
                }
                puts("Pilihan salah!\n");
            }
        }
        free(stored_result);    
    }
    else {
        puts("Invalid!");
    } 
    return 0;
}