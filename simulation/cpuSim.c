#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>
#include <pthread.h> 
//magic number for 1.0 sec  = 537377990
//magic number for 0.01 sec = 5373779 	//*60 for 60%
//100,0000 = 1 sec sleep

//0.6


int main(int argc, char *argv[]){
	
	//int interval=300; //sec
	int interval=atoi(argv[2]); //sec
	float input=atof(argv[1]);
	int cores=(int)input+1;
	float cpuUsage=input/cores;
	pid_t *pids = (pid_t*)malloc(sizeof(pid_t)*cores);

	int i=0;
	long magicPer01 = 5373779; 
	
	int ratioCpu;
	int sleepTime;
	int elapsedTime=0;

	clock_t start;
	clock_t end;
	double time;

	int a=1;
	int b=2;
	int c=1;

	for(i=0; i<cores; i++){
		pids[i]=fork();
		if(pids[i]==0){
			while(1){
				long myId=(long)getpid();

				start=clock();
				ratioCpu = (int)(cpuUsage*100);
				sleepTime = (100-ratioCpu)*10000;
				for(i=0; i<magicPer01*ratioCpu; i++){
					c=a*b;
				}

				end=clock();
				time=(double)(end-start)/(CLOCKS_PER_SEC);
				// printf("core: %d process ID: %d usage: %.2f calc time: %.2f\n", cores, myId, cpuUsage, time);

				usleep(sleepTime);
				elapsedTime++;
				
				if(elapsedTime>=interval){
					elapsedTime=0;
					//break;
					return 0;
				}
			}
			return 0;
		}
	}

	return 0;
}
