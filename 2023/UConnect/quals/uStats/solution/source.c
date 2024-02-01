// gcc source.c -no-pie -s -o ustats

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void setup() {
	setvbuf(stdout, NULL, _IONBF, 0);
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stderr, NULL, _IONBF, 0);
}

double mean(double a, int b){
    double res;
    res = a / b;
    return res;
}

double median(double a[], int n){
    double res;
    if ( n % 2 == 0){
    res = (a[n/2] + a[n/2+1])/2.0 ;
    } else {
    res = a[n/2 + 1];
    }
    return res;
}

double mode(double a[],int n){
   int res = 0;
   int maxCount = 0, i, j;

   for (i = 0; i < n; ++i) {
      int count = 0;
      
      for (j = 0; j < n; ++j) {
         if (a[j] == a[i])
         ++count;
      }
      
      if (count > maxCount) {
         maxCount = count;
         res = a[i];
      }
   }

   return res;
}

int main(){
    int jumlah_data;
    int idx;
    double total_nilai = 0.0;
    double simpan_data[37];

    setup();
    puts("Program penghitung statistik - uStats");
    printf("Berapa jumlah data yang ingin kamu masukkan? ");
    scanf("%d",&jumlah_data);
    for (idx = 0; idx < jumlah_data; idx++)
    {
        printf("Nilai ke-%d: ",idx+1);
        scanf("%lf",&simpan_data[idx]);
        total_nilai = total_nilai + simpan_data[idx];
    }
    printf("Nilai rata-rata (mean)\t\t\t: %.2f\n",mean(total_nilai,jumlah_data));
    printf("Nilai tengah (median)\t\t\t: %2.f\n",median(simpan_data,jumlah_data));
    printf("Nilai paling banyak muncul (modus)\t: %2.f\n",mode(simpan_data,jumlah_data));
    return 0;
}