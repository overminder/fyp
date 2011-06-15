#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <iostream>
#include  <string>

#include "ICTCLAS50.h"

using namespace std;

int main(int argc, char * argv[])
{
    if(!ICTCLAS_Init())
	{   
		//printf("Init failed.\n");  
		return -1;
	}   
	else
	{   
		//printf("Init done.\n");
	} 

	ICTCLAS_SetPOSmap(2);
	
	//unsigned int length = strlen(argv[1]);
	//char* result = (char*)malloc(length*6);
	//int resultLen = ICTCLAS_ParagraphProcess(argv[1],length,result,CODE_TYPE_UTF8,1);
	//printf("The result is \n%s\n",result);
	//printf("(%d)%s\n",resultLen,result);
	
	ICTCLAS_FileProcess(argv[1], argv[2],CODE_TYPE_UTF8,1);
	ICTCLAS_Exit(); 
	return 0;
}
