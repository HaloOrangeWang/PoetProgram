#pragma once

#ifndef VARIABLES_H_
#define VARIABLES_H_

#include <Windows.h>
#include <string>

using namespace std;

extern unsigned int OutData[4];   //CRC16
extern HANDLE hComm;

extern const string ImgPath;  //ͼƬ·��

void OutPut_Data();
void GetData(float Ch1, float Ch2, float Ch3, float Ch4);

#endif