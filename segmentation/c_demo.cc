/******************************************************************************* 
@All Right Reserved (C), 2010-2100, golaxy.cn
Filepath   : e:\Project\IctClas\ictclas_demo_c
Filename   : win_cDemo.cpp
Version    : ver 5.0
Author     : x10n6y@gmail.com 
Date       : 2010/07/12  
Description:   
History    :
1.2010/07/12 14:04 Created by x10n6y@gmail.com Version 5.0 
*******************************************************************************/
#ifndef OS_LINUX
#include <Windows.h>
#pragma comment(lib, "ICTCLAS50.lib") //ICTCLAS50.lib库加入到工程中
#endif

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <iostream>
#include  <string>
#include "ICTCLAS50.h"

using namespace std;

#define POS_TAGGER_TEST
#ifdef POS_TAGGER_TEST
bool g_bPOSTagged=true;
#else
bool g_bPOSTagged=false;
#endif    

int
cxx_init()
{
    // 设置词性标注集(0 计算所二级标注集，1 计算所一级标注集，
    // 2 北大二级标注集，3 北大一级标注集)
    ICTCLAS_SetPOSmap(2);

    return ICTCLAS_Init();  //初始化分词组件。
}

/* for use in the below function */
static char *paragraph_res = NULL;
  
char *
cxx_do_paragraph(const char *sentence, int sentence_len)
{
    if (paragraph_res) free(paragraph_res);
    // 建议长度为字符串长度的6倍... why?
    paragraph_res = (char *)malloc(sentence_len * 6);

    int res_len = 0; //分词结果的长度

    res_len = ICTCLAS_ParagraphProcess(sentence, sentence_len, paragraph_res,
        CODE_TYPE_UTF8, 1);  //字符串处理

    paragraph_res[res_len] = 0;
    return paragraph_res;
}

void
cxx_finalize()
{
    free(paragraph_res);
    ICTCLAS_Exit();    //释放资源退出
}


extern "C" {

int
do_init()
{
    return cxx_init();
}

char *
do_paragraph(const char *sentence, int sentence_len)
{
    return cxx_do_paragraph(sentence, sentence_len);
}

int
do_finalize()
{
    cxx_finalize();
}

}


