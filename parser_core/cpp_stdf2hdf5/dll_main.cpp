// dllmain.cpp : ���� DLL Ӧ�ó������ڵ㡣
#include "pch.h"

BOOL APIENTRY DllMain(HMODULE hModule,
    DWORD  ul_reason_for_call,
    LPVOID lpReserved
)
{
    switch (ul_reason_for_call)
    {
    case DLL_PROCESS_ATTACH:
    case DLL_THREAD_ATTACH:
    case DLL_THREAD_DETACH:
    case DLL_PROCESS_DETACH:
        break;
    }
    return TRUE;
}

// ��ʱʹ��CSV, ����ʹ��pybind11_numpy(easy) / hdf5
extern "C"  _declspec(dllexport) Cplus_stdf * NewStdf() { return new Cplus_stdf(); }; // ����
extern "C"  _declspec(dllexport) void DeleteStdf(Cplus_stdf * stdf) { stdf->Clear(); delete stdf; stdf = nullptr; }; // ɾ����
extern "C"  _declspec(dllexport) bool ParserStdfToHdf5(Cplus_stdf * stdf, wchar_t* filename) { return stdf->ParserStdfToHdf5(filename); };
extern "C"  _declspec(dllexport) int GetFinishT(Cplus_stdf * stdf) { return stdf->GetFinishT(); };
