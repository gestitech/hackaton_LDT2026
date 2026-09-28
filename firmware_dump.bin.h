typedef unsigned char   undefined;

typedef unsigned char    undefined1;
typedef unsigned int    undefined4;
#define unkbyte9   unsigned long long
#define unkbyte10   unsigned long long
#define unkbyte11   unsigned long long
#define unkbyte12   unsigned long long
#define unkbyte13   unsigned long long
#define unkbyte14   unsigned long long
#define unkbyte15   unsigned long long
#define unkbyte16   unsigned long long

#define unkuint9   unsigned long long
#define unkuint10   unsigned long long
#define unkuint11   unsigned long long
#define unkuint12   unsigned long long
#define unkuint13   unsigned long long
#define unkuint14   unsigned long long
#define unkuint15   unsigned long long
#define unkuint16   unsigned long long

#define unkint9   long long
#define unkint10   long long
#define unkint11   long long
#define unkint12   long long
#define unkint13   long long
#define unkint14   long long
#define unkint15   long long
#define unkint16   long long

#define unkfloat1   float
#define unkfloat2   float
#define unkfloat3   float
#define unkfloat5   double
#define unkfloat6   double
#define unkfloat7   double
#define unkfloat9   long double
#define unkfloat11   long double
#define unkfloat12   long double
#define unkfloat13   long double
#define unkfloat14   long double
#define unkfloat15   long double
#define unkfloat16   long double

#define BADSPACEBASE   void
#define code   void




void Stage2_Bootloader(void);
undefined8 SPI_Flash_WaitReady(undefined4 param_1,undefined4 param_2,undefined4 param_3,int param_4);
undefined8 SPI_Flash_SendCommand(undefined4 param_1,undefined4 param_2,undefined4 param_3,int param_4);
void Tick_Callback_Handler(void);
void System_Tick_Handler(undefined4 param_1,undefined4 param_2);
void USB_BuildStringDescriptor(undefined4 param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4);
undefined4 Stub_ValidateDescriptor(void);
undefined4 TEA_XTEA_Decrypt(undefined4 param_1,uint param_2,uint param_3,undefined4 param_4);
undefined4 MSC_HandleWriteSector(undefined4 param_1,uint param_2,uint param_3,undefined4 param_4);
void NOP_Handler(void);
undefined4 Error_Return_Negative(void);
void HardFault_Panic(int param_1,undefined4 param_2,int param_3);
void Stub_Halt_1(void);
void Stub_Halt_2(void);
void GPIO_IncrementCounter(void);
void Stub_GPIO_SetMode(undefined4 param_1);
void Stub_Halt_3(void);
void GPIO_ConfigureIRQ(uint param_1,int param_2);
void Stub_Halt_4(void);
void Stub_Halt_5(void);
void GPIO_CalculateAddress(int *param_1,int param_2);
void Stub_GPIO_SetupPin(int param_1);
void Stub_GPIO_GetPin(int *param_1);
void Stub_Halt_Wrapper(undefined4 param_1,undefined4 param_2);
undefined4 System_GetTickCount(void);
void USB_MSC_ConfigureEndpoint_IN(int param_1,uint param_2,int param_3,undefined4 param_4,int param_5);
void USB_MSC_ConfigureEndpoint_OUT(int param_1,uint param_2,int param_3,undefined4 param_4);
undefined4 USB_MSC_GetEndpointValue(int param_1);
void USB_MSC_SetupBuffer(uint *param_1,uint param_2,undefined4 param_3,int param_4,int param_5);
void USB_MSC_SetFlag(undefined4 param_1,uint param_2);
void IRQ_SetHandler(undefined4 param_1);
void IRQ_SetHandler_Alt(undefined4 param_1);
byte Validate_Array(int *param_1,int param_2);
void USB_MSC_InitController(void);
void Call_Callback_Array(void);
void Call_Callback_Array_NoArgs(void);
void USB_MSC_ResetController(void);
void USB_MSC_CheckStatus(void);
ulonglong USB_MSC_ComputeSectorAddress(int param_1,int param_2);
ulonglong USB_MSC_ComputeSectorAddress_Alt(int param_1,int param_2,int param_3);
void ROM_API_Call(void);
void USB_Handler_Indirect(void);
bool USB_CallCallback(undefined4 param_1,undefined4 param_2);
void Debug_Breakpoint(void);
void USB_ProcessString(undefined4 *param_1,char *param_2,int param_3);
int USB_Printf(undefined4 param_1,int param_2,int param_3,int param_4);
undefined4 USB_Putchar(undefined4 param_1);
undefined4 USB_Puts(undefined4 param_1);
void USB_SendString(undefined4 param_1);
undefined4 USB_ConfigureEndpoint_Params(int param_1,int param_2,uint param_3,uint param_4,char param_5);
undefined4 USB_MSC_Initialize(void);
void USB_EnableInterrupt(void);
undefined4 USB_HandleSetupPacket(undefined4 param_1,int param_2);
undefined4 USB_TransmitPacket(undefined4 param_1,uint param_2,undefined4 param_3,undefined4 param_4);
void USB_ResetEndpoint(undefined4 param_1,uint param_2);
void USB_InitBuffers(void);
void USB_PrepareTransaction(int param_1,undefined4 param_2,undefined2 param_3);
undefined4 USB_InitializeDevice(undefined4 param_1,int param_2);
undefined4 USB_ParseDescriptors(undefined4 param_1,byte *param_2,int param_3,uint param_4,byte *param_5,byte *param_6);
int USB_Endpoint_Transmit(undefined4 param_1,uint param_2);
byte USB_CheckEndpointStatus(undefined4 param_1,uint param_2);
void USB_HandleError(undefined4 param_1,uint param_2);
uint USB_GetEndpointStatus(undefined4 param_1,uint param_2);
void USB_SendStatus(undefined4 param_1,byte *param_2);
undefined4 USB_SendData(undefined4 param_1,byte *param_2,int param_3,uint param_4);
void MSC_HandleReadError(undefined4 param_1,undefined1 param_2);
void MSC_HandleReadSector(undefined4 param_1);
undefined4 SCSI_CommandHandler(undefined4 param_1,uint param_2,undefined4 param_3,uint param_4);
bool USB_ValidateEndpointParams(int param_1,int param_2);
undefined4 USB_CleanupEndpoint(int param_1);
void USB_SendString_Wrapper(void);
void Memcpy_Overlap(undefined4 *param_1,undefined4 *param_2,uint param_3);
int Strlen(uint *param_1);
void Call_Handler_0(undefined4 param_1);
void Call_Handler_1(undefined4 param_1);
void Call_Handler_2(undefined4 param_1);
void Call_Handler_3(undefined4 param_1);
void Call_Handler_4(undefined4 param_1);
void Call_Handler_5(undefined4 param_1);
void Call_Handler_6(undefined4 param_1);
void Call_Handler_7(undefined4 param_1);
void Call_Handler_8(undefined4 param_1);
void Call_Handler_9(undefined4 param_1);
void Call_Handler_A(undefined4 param_1);
void Decompress_Copy(int param_1,int param_2);
void GPIO_ConfigureInterrupt(int param_1,uint param_2,uint param_3);
void Call_Handler_B(undefined4 param_1);

