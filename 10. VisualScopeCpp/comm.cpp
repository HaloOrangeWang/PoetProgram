#include "variables.h"
unsigned int OutData[4];   //CRC16


////////////////////////////////////////////////////////////////////////////////////////////////////
//CRC16串口通讯协议

//--------------------------------------------------------------------------------
//The following is the function of CRC16,please refer
//--------------------------------------------------------------------------------
unsigned short CRC_CHECK(unsigned char* Buf, unsigned char CRC_CNT)
{
	unsigned short CRC_Temp;
	unsigned char i, j;
	CRC_Temp = 0xffff;

	for (i = 0; i < CRC_CNT; i++) {
		CRC_Temp ^= Buf[i];
		for (j = 0; j < 8; j++) {
			if (CRC_Temp & 0x01)
				CRC_Temp = (CRC_Temp >> 1) ^ 0xa001;
			else
				CRC_Temp = CRC_Temp >> 1;
		}
	}
	return(CRC_Temp);
}
//--------------------------------------------------------------------------------
//The above is the function of CRC16,please refer
//--------------------------------------------------------------------------------


//--------------------------------------------------------------------------------
//Monitor routine Execute every T Period time
void OutPut_Data()
{
	unsigned short ChxData[4] = { 0 };
	unsigned char databuf[10] = { 0 };
	unsigned char i;
	unsigned short CRC16 = 0;
	for (i = 0; i < 4; i++)
	{

		ChxData[i] = (unsigned short)OutData[i];
		//test161u = (unsigned short)OutData[i];

	}

	for (i = 0; i < 4; i++)
	{
		databuf[i * 2 + 0] = (unsigned char)((ChxData[i]) & 0xff);
		databuf[i * 2 + 1] = (unsigned char)((ChxData[i]) >> 8);
	}

	CRC16 = CRC_CHECK(databuf, 8);
	databuf[8] = CRC16 & 0xff;
	databuf[9] = CRC16 >> 8;

	//for (i = 0; i < 10; i++)
	//	uart_send(databuf[i]);
	DWORD bytes_num = 10;
	bool write_state = WriteFile(hComm, databuf, bytes_num, &bytes_num, NULL);
	if (!write_state) {
		DWORD error_id = GetLastError();
		printf("write serial failed. error id =%d\n", error_id);
	}
}
//--------------------------------------------------------------------------------
//above is MCU code for CRC16 ,please refer.
//--------------------------------------------------------------------------------

void GetData(float Ch1, float Ch2, float Ch3, float Ch4)
{
	int temp[4];
	temp[0] = (int)Ch1;
	temp[1] = (int)Ch2;
	temp[2] = (int)Ch3;
	temp[3] = (int)Ch4;
	OutData[0] = (unsigned int)temp[0];
	OutData[1] = (unsigned int)temp[1];
	OutData[2] = (unsigned int)temp[2];
	OutData[3] = (unsigned int)temp[3];
}

//////////////////////////////////////////////////////////////////////////////////////////////////
