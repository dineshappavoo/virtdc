	#include <stdio.h>
	#include <stdlib.h>
	#include <time.h>
	int main(int argc, char *argv[])
	{
		if(argc!=2)
		{
		    printf( "usage: %d <Memory in Kbs>", argc );
		}

		int nmeg,l_retval,tot_megs =0;
		char *ptr,buf[128];
		char *t;
		int reqdMegs, n;
		int noOfMallocs =1;
		int leftOver=0;
		tot_megs=0;
		
		if (ptr==NULL) 
		{
			printf("\n\n");
			exit (0);
		}
		reqdMegs=atoi(argv[1])/1024;
		if(reqdMegs>2047)
		{
		  noOfMallocs = reqdMegs/2047 + 1;
		  leftOver = reqdMegs%2047;
		  n=2047; 
		}
		else
		{
		  n=reqdMegs;
		}
		int nmegs[noOfMallocs];
		int i;
	
	
		nmeg=n*(1024*1024);
	
		void *mptr[noOfMallocs];
		for(i=0;i<noOfMallocs;i++)	
		{
		 mptr[i]=malloc(nmeg);
		}
		if(leftOver>0)
		{
			mptr[i]=malloc(leftOver*(1024*1024));
		}
		int j=0;
		while (1) {
		for(i=0;i<noOfMallocs;i++)		
		{
		if(tot_megs<reqdMegs)	 
		 {
			tot_megs=(tot_megs+n);
		 }
		if (mptr == NULL)
		{
		
			/* Error message */
			printf("malloc %d more megs failed (%d total)\n",n,tot_megs);
			exit(1);
		}
		else 
		{
			if(tot_megs<reqdMegs)		
			{
				//printf("%d megs additional RAM, Total megs = %d \n\n",n,tot_megs);
			}
			else if(tot_megs != reqdMegs)
			{
				tot_megs = tot_megs-n+leftOver;			
				//printf("%d megs additional RAM, Total megs = %d \n\n",leftOver,tot_megs);
			}
		}

		 for (j=0;j<nmeg;j+=1024)
			{
				*((char *)mptr[i]+j)='!';
			}
	
	}
	sleep(10);
		} /* while */

		printf("\n\n");
		return 0;
	} /* main */

