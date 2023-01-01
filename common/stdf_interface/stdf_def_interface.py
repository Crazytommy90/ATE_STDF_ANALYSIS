#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : code_interface.py
@Author  : Link
@Time    : 2020/7/25 15:07
@Mark    : 定义了一些数据的类型
           @ 使用python重写部分STDF转换工具, 适用于对速度无要求的实验室场景
"""
from typing import List


class STDF_TYPE:
    pass


class STDF_FLAG:
    """
    base u8
    """
    # u8 = 0b00000000
    #
    # def set_bit(self, location: int, boolean: bool = True) -> int:
    #     """
    #     配置bit位的数据
    #     :param location:
    #     :param boolean:
    #     :return:
    #     """
    #     if boolean:
    #         return self.u8 | (1 << location)
    #     return self.u8 & ~(1 << location)
    #
    # def get_bit(self, location: int) -> bool:
    #     """
    #     获取bit位的数据
    #     :param location:
    #     :return:
    #     """
    #     if self.u8 & (1 << location):
    #         return True
    #     return False
    u8: List[str] = None

    def __init__(self):
        self.u8 = ['0'] * 8

    def set_bit(self, location: int, boolean: bool = True) -> List[str]:
        """
        配置bit位的数据
        :param location:
        :param boolean:
        :return:
        """
        if boolean:
            self.u8[7 - location] = "1"
        else:
            self.u8[7 - location] = "0"
        return self.u8

    def get_bit(self, location: int) -> bool:
        """
        获取bit位的数据
        :param location:
        :return:
        """
        if self.u8[7 - location] == "1":
            return True
        return False


class Mir(STDF_TYPE):
    SETUP_T: int = 0
    START_T: int = 0
    STAT_NUM: int = 1
    MODE_COD: str = "P"
    LOT_ID: str = ""
    PART_TYP: str = "Python"
    NODE_NAM: str = "LinkAte"
    TSTR_TYP: str = ""
    JOB_NAM: str = ""
    SBLOT_ID: str = ""
    FLOW_ID: str = "R0"
    TEST_COD: str = ""

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class Wir(STDF_TYPE):
    HEAD_NUM: int = 1
    SITE_GRP: int = 255
    START_T: int = 0
    WAFER_ID: str = ""

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class Mrr(STDF_TYPE):
    FINISH_T = 0

    def __init__(self, FINISH_T):
        self.FINISH_T = FINISH_T


class Pir(STDF_TYPE):
    HEAD_NUM: int = 1
    SITE_NUM: int = 0

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class Prr_PART_FLG(STDF_FLAG):

    def part_supersede_flag(self):
        return self.get_bit(0) or self.get_bit(1)

    def part_abnormal_flag(self):
        return self.get_bit(2)

    def part_failed_flag(self):
        return self.get_bit(3)

    def pass_fail_flag_invalid(self):
        return self.get_bit(4)

    def set_part_supersede_flag(self, boolean: bool = True):
        self.set_bit(0, boolean)
        self.set_bit(1, False)

    def set_part_abnormal_flag(self, boolean: bool = True):
        return self.set_bit(2, boolean)

    def set_part_failed_flag(self, boolean: bool = True):
        return self.set_bit(3, boolean)

    def set_pass_fail_flag_invalid(self, boolean: bool = True):
        return self.set_bit(4, boolean)


class Prr(STDF_TYPE):
    """
      **Part Results Record (PRR)**

      Function:
        Contains the result information relating to each part tested by the
        test_utils program. The PRR and the Part Information Record (PIR) bracket
        all the stored information pertaining to one tested part.

      Data Fields:
        ======== ===== ======================================== ====================
        Name     Type  Description                              Missing/Invalid Flag
        ======== ===== ======================================== ====================
        REC_LEN  U*2   Bytes of code_interface following header
        REC_TYP  U*1   Record type(5)
        REC_SUB  U*1   Record sub-type (20)
        HEAD_NUM U*1   Test head number
        SITE_NUM U*1   Test site number
        PART_FLG B*1   Part information flag
        NUM_TEST U*2   Number of tests executed
        HARD_BIN U*2   Hardware bin number
        SOFT_BIN U*2   Software bin number                      65535
        X_COORD  I*2   (Wafer) X coordinate                     -32768
        Y_COORD  I*2   (Wafer) Y coordinate                     -32768
        TEST_T   U*4   Elapsed test_utils time in milliseconds        0
        PART_ID  C*n   Part identification                      length byte = 0
        PART_TXT C*n   Part description text                    length byte = 0
        PART_FIX B*n   Part repair information                  length byte = 0
        ======== ===== ======================================== ====================

      Notes on Specific Fields:
        HEAD_NUM, SITE_NUM:
          If a test_utils system does not support parallel testing, and does not have
          a standard way to identify its single test_utils site or head, then these
          fields should be set to 1.  When parallel testing, these fields are
          used to associate individual datalogged results (FTR's an dPTR's) with
          a PIR/PRR pair. An FTR or PTR belongs to the PIR/PRR pair having the
          same values for HEAD_NUM and SITE_NUM.
        X_COORD, Y_COORD:
          Have legal values in the range -32767 to 32767. A missing value is
          indicated by the value -32768.
        X_COORD, Y_COORD, PART_ID:
          Are all optional, but you should provide either the PART_ID or the X_COORD
          and Y_COORD in order to make the resultant code_interface use ful for analysis.
        PART_FLG:
          Contains the following fields:

            * bit 0:

              * 0 = This is a new part. Its code_interface device does not supersede that of
                any previous device.
              * 1 = The PIR, PTR, MPR, FTR, and PRR records that make up the current
                sequence (identified as having the same HEAD_NUM and SITE_NUM)
                supersede any previous sequence of records with the same PART_ID.(A
                repeated part sequence usually indicates a mistested part.)
            * bit 1:

              * 0 = This is a new part. Its code_interface device does not supersede that of
                any previous device.
              * 1 = The PIR, PTR, MPR, FTR, and PRR records that make up the current
                sequence (identified as having the same HEAD_NUM and SITE_NUM)
                supersede any previous sequence of records with the same X_COORD and
                Y_COORD.(A repeated part sequence usually indicates a mistested
                part.)

            Note:
              Either Bit 0 or Bit 1 can be set, but not both. (It is also valid to
              have neither set.)

            * bit2:

              * 0 = Part testing completed normally
              * 1 = Abnormal end of testing

            * bit3:

              * 0 = Part passed
              * 1 = Part failed

            * bit 4:

              * 0 = Pass/fail flag (bit 3) is valid
              * 1 = Device completed testing with no pass/fail indication
                (i.e., bit 3 is invalid)

            * bits 5 - 7:

              Reserved for future use  must be 0

        HARD_BIN:
          Has legal values in the range 0 to 32767.
        SOFT_BIN:
          Has legal values in the range 0 to 32767. A missing value is indicated
          by the value 65535.
        PART_FIX:
          This is an application-specific field for storing device repair
          information. It may be used for bit-encoded, integer, floating point,
          or character information. Regardless of the information stored, the
          first byte must contain the number of bytes to follow. This field can
          be decoded only by an application-specific analysis program.

      Frequency:
        One per part tested.

      Location:
        Anywhere in the code_interface stream after the corresponding PIR and before the MRR.
        Sent after completion of testing each part.

      Possible Use:
        * Datalog
        * Wafer map
        * RTBM
        * Shmoo Plot
        * Repair Data
      """
    HEAD_NUM: int = 1
    SITE_NUM: int = 0
    PART_FLG: Prr_PART_FLG = None
    NUM_TEST: int = 0
    HARD_BIN: int = 1
    SOFT_BIN: int = 1
    X_COORD: int = 1
    Y_COORD: int = 1
    TEST_T: int = 0
    PART_ID: str = ""
    PART_TXT: str = ""

    def __init__(self, **kwargs):
        self.PART_FLG = Prr_PART_FLG()
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.PART_FLG.set_part_failed_flag(False)

    def value(self) -> dict:
        pass

    def __str__(self):
        return "SITE: {}, RESULT FAIL?: {}, HARD_BIN: {}, SOFT_BIN: {}".format(self.SITE_NUM,
                                                                               self.PART_FLG.part_failed_flag(),
                                                                               self.HEAD_NUM, self.SOFT_BIN)


class Ptr_TEST_FLG(STDF_FLAG):

    def alarm_detected(self):
        return self.get_bit(0)

    def result_invalid(self):
        return self.get_bit(1)

    def result_unreliable(self):
        return self.get_bit(2)

    def timeout_occured(self):
        return self.get_bit(3)

    def test_unexecuted(self):
        return self.get_bit(4)

    def test_aborted(self):
        return self.get_bit(5)

    def test_pfflag_invalid(self):
        return self.get_bit(6)

    def test_failed(self):
        return self.get_bit(7)

    def set_alarm_detected(self, boolean: bool = True):
        return self.set_bit(0, boolean)

    def set_result_invalid(self, boolean: bool = True):
        return self.set_bit(1, boolean)

    def set_result_unreliable(self, boolean: bool = True):
        return self.set_bit(2, boolean)

    def set_timeout_occured(self, boolean: bool = True):
        return self.set_bit(3, boolean)

    def set_test_unexecuted(self, boolean: bool = True):
        return self.set_bit(4, boolean)

    def set_test_aborted(self, boolean: bool = True):
        return self.set_bit(5, boolean)

    def set_test_pfflag_invalid(self, boolean: bool = True):
        return self.set_bit(6, boolean)

    def set_test_failed(self, boolean: bool = True):
        return self.set_bit(7, boolean)


class Ptr_PARM_FLG(STDF_FLAG):

    def param_scale_error(self):
        return self.get_bit(0)

    def param_drift_error(self):
        return self.get_bit(1)

    def param_oscillation(self):
        return self.get_bit(2)

    def result_higher_limit(self):
        return self.get_bit(3)

    def result_lower_limit(self):
        return self.get_bit(4)

    def passed_alternate_limit(self):
        return self.get_bit(5)

    def equal_lowlimit_pass(self):
        return self.get_bit(6)

    def equal_highlimit_pass(self):
        return self.get_bit(7)

    def set_param_scale_error(self, boolean: bool = True):
        return self.set_bit(0, boolean)

    def set_param_drift_error(self, boolean: bool = True):
        return self.set_bit(1, boolean)

    def set_param_oscillation(self, boolean: bool = True):
        return self.set_bit(2, boolean)

    def set_result_higher_limit(self, boolean: bool = True):
        return self.set_bit(3, boolean)

    def set_result_lower_limit(self, boolean: bool = True):
        return self.set_bit(4, boolean)

    def set_passed_alternate_limit(self, boolean: bool = True):
        return self.set_bit(5, boolean)

    def set_equal_lowlimit_pass(self, boolean: bool = True):
        """
        :param boolean:
        :return: GT if boolean else GE
        """
        return self.set_bit(6, boolean)

    def set_equal_highlimit_pass(self, boolean: bool = True):
        """
        :param boolean:
        :return: LT if boolean else LE
        """
        return self.set_bit(7, boolean)


class Ptr_OPT_FLAG(STDF_FLAG):
    def result_exponent_invalid(self):
        return self.get_bit(0)

    def unknown(self):
        return self.get_bit(1)

    def no_low_spec(self):
        return self.get_bit(2)

    def no_high_spec(self):
        return self.get_bit(3)

    def low_limit_invalid(self):
        return self.get_bit(4)

    def high_limit_invalid(self):
        return self.get_bit(5)

    def no_low_limit(self):
        """
        NA?
        :return:
        """
        return self.get_bit(6)

    def no_high_limit(self):
        """
        NA?
        :return:
        """
        return self.get_bit(7)

    def set_result_exponent_invalid(self, boolean: bool = True):
        return self.set_bit(0, boolean)

    def set_unknown(self, boolean: bool = True):
        return self.set_bit(1, boolean)

    def set_no_low_spec(self, boolean: bool = True):
        return self.set_bit(2, boolean)

    def set_no_high_spec(self, boolean: bool = True):
        return self.set_bit(3, boolean)

    def set_low_limit_invalid(self, boolean: bool = True):
        return self.set_bit(4, boolean)

    def set_high_limit_invalid(self, boolean: bool = True):
        return self.set_bit(5, boolean)

    def set_no_low_limit(self, boolean: bool = True):
        return self.set_bit(6, boolean)

    def set_no_high_limit(self, boolean: bool = True):
        return self.set_bit(7, boolean)


class Ptr(STDF_TYPE):
    """
    **Parametric Test Record (PTR)**

    Function:
      Contains the results of a single execution of a parametric test_utils in the
      test_utils program. The first occurrence of this record also establishes
      the default values for all semi-static information about the test_utils,
      such as limits, units, and scaling. The PTR is related to the Test
      Synopsis Record (TSR) by test_utils number, head number, and site number.

    Data Fields:
      ======== ===== ======================================== ====================
      Name     Type  Description                              Missing/Invalid Flag
      ======== ===== ======================================== ====================
      REC_LEN  U*2   Bytes of code_interface following header
      REC_TYP  U*1   Record type(15)
      REC_SUB  U*1   Record sub-type (10)
      TEST_NUM U*4   Test number
      HEAD_NUM U*1   Test head number
      SITE_NUM U*1   Test site number
      TEST_FLG B*1   Test flags (fail, alarm, etc.)
      PARM_FLG B*1   Parametric test_utils flags (drift, etc.)
      RESULT   R*4   Test result                              TEST_FLG bit 1 = 1
      TEST_TXT C*n   Test description text or label           length byte = 0
      ALARM_ID C*n   Name of alarm                            length byte = 0
      OPT_FLAG B*1   Optional code_interface flag                       See note
      RES_SCAL I*1   Test results scaling exponent            OPT_FLAG bit 0 = 1
      LLM_SCAL I*1   Low limit scaling exponent               OPT_FLAG bit 4or6=1
      HLM_SCAL I*1   High limit scaling exponent              OPT_FLAG bit 5or7=1
      LO_LIMIT R*4   Low test_utils limit value                     OPT_FLAG bit 4or6=1
      HI_LIMIT R*4   High test_utils limit value                    OPT_FLAG bit 5or7=1
      UNITS    C*n   Test units                               length byte = 0
      C_RESFMT C*n   ANSI Cresultformatstring                 length byte = 0
      C_LLMFMT C*n   ANSI C low limit format string           length byte = 0
      C_HLMFMT C*n   ANSI C high limit format string          length byte = 0
      LO_SPEC  R*4   Low specification limit value            OPT_FLAG bit 2 = 1
      HI_SPEC  R*4   High specification limit value           OPT_FLAG bit 3 = 1
      ======== ===== ======================================== ====================

    Notes on Specific Fields:

    Default Data:
      All code_interface following the OPT_FLAG field has a special function in the STDF
      file. The first PTR for each test_utils will have these fields filled in. These
      values will be the default for each subsequent PTR with the same test_utils
      number: if a subsequent PTR has a value for one of these fields, it will
      be used instead of the default, for that one record only; if the field
      is blank, the default will be used. This method replaces use of the PDR
      in STDF V3.  If the PTR is not associated with a test_utils execution (that
      is, it contains only default information), bit 4 of the TEST_FLG field
      must be set, and the PARM_FLG field must be zero.  Unless the default
      is being overridden, the default code_interface fields should be omitted in order
      to save space in the file.  Note that RES_SCAL, LLM_SCAL, HLM_SCAL,
      UNITS, C_RESFMT, C_LLMFMT, and C_HLMFMT are interdependent. If you
      are overriding the default value of one, make sure that you also make
      appropriate changes to the others in order to keep them consistent.
      For character strings, you can override the default with a null value
      by setting the string length to 1 and the string itself to a single
      binary 0.
    HEAD_NUM, SITE_NUM:
      If a test_utils system does not support parallel testing, and does not have a
      standard way of identifying its single test_utils site or head, these fields
      should be set to 1.  When parallel testing, these fields are used to
      associate individual datalogged results with a PIR/PRR pair. APTR belongs
      to the PIR/PRR pair having the same values for HEAD_NUM and SITE_NUM.

    TEST_FLG:
      Contains the following fields:

        * bit 0

          * 0 = No alarm
          * 1 = Alarm detected during testing

        * bit 1

          * 0 = The value in the RESULT field is valid (see note on RESULT )
          * 1 = The value in the RESULT field is not valid. This setting
            indicates that the test_utils was executed, but no datalogged value was
            taken. You should read bits 6 and 7 of TEST_FLG to determine if the
            test_utils passed or failed.

        * bit2

          * 0 = Test result is reliable
          * 1 = Test result is unreliable

        * bit 3

          * 0 = No timeout
          * 1 = Timeout occurred

        * bit 4

          * 0 = Test was executed
          * 1 = Test not executed

        * bit 5

          * 0 = No abort
          * 1 = Test aborted

        * bit 6

          * 0 = Pass/fail flag (bit 7) is valid
          * 1 = Test completed with no pass/fail indication

        * bit 7

          * 0 = Test passed
          * 1 = Test failed

    PARM_FLG:
      Is the parametric flag field, and contains the following bits:
        * bit 0

          * 0 = No scale error
          * 1 = Scale error

        * bit 1

          * 0 = No drift error
          * 1 = Drift error (unstable measurement)

        * bit 2

          * 0 = No oscillation
          * 1 = Oscillation detected

        * bit 3

          * 0 = Measured value not high
          * 1 = Measured value higher than high test_utils limit

        * bit 4

          * 0 = Measured value not low
          * 1 = Measured value lower than low test_utils limit

        * bit 5

          * 0 = Test failed or test_utils passed standard limits
          * 1 = Test passed alternate limits

        * bit 6

          * 0 = If result = low limit, then result is *fail.*
          * 1 = If result = low limit, then result is *pass.*

        * bit 7

          * 0 = If result = high limit, then result is *fail.*
          * 1 = If result = high limit, then result is *pass.*

    RESULT:
      The RESULT value is considered useful only if all the following bits from
      TEST_FLG and PARM_FLG are 0:

        * TEST_FLG

          * bit 0 = 0 no alarm
          * bit 1 = 0 value in result field is valid
          * bit 2 = 0 test_utils result is reliable
          * bit 3 = 0 no timeout
          * bit 4 = 0 test_utils was executed
          * bit 5 = 0 no abort

        * PARM_FLG

          * bit 0 = 0 no scale error
          * bit 1 = 0 no drifterror
          * bit 2 = 0 no oscillation

      If any one of these bits is 1, then the PTR result should not be used.

    ALARM_ID:
      If the alarm flag (bit 0 of TEST_FLG ) is set, this field can contain
      the name or ID of the alarms that were triggered. Alarm names are
      tester-dependent.

    OPT_FLAG:
      Is the Optional code_interface flag and contains the following bits:

        * bit 0 set = RES_SCAL value is invalid. The default set by the first PTR
          with this test_utils number will be used.
        * bit 1 reserved for future used and must be 1.
        * bit 2 set = No low specification limit.
        * bit 3 set = No high specification limit.
        * bit 4 set = LO_LIMIT and LLM_SCAL are invalid. The default values set
          for these fields in the first PTR with this test_utils number will be used.
        * bit 5 set = HI_LIMIT and HLM_SCAL are invalid. The default values set
          for these fields in the first PTR with this test_utils number will be used.
        * bit 6 set = No Low Limit for this test_utils (LO_LIMIT and LLM_SCAL are
          invalid).
        * bit7 set = No High Limit for this test_utils (HI_LIMIT and HLM_SCAL
          are invalid).

      The OPT_FLAG field may be omitted if it is the last field in the record.

    C_RESFMT, C_LLMFMT, C_HLMFMT:
      ANSI C format strings for use in formatting the test_utils result and low
      and high limits ,(both test_utils and spec). For example, *%7.2*.Tf he format
      string is also known as an output specification string, as used with the
      printf statement. See any ANSI C reference man, or the man page on printf

    LO_SPEC, HI_SPEC:
      The specification limits are set in the first PTR and should never
      change. They use the same scaling and format strings as the corresponding
      test_utils limits.

    Frequency:
      One per parametric test_utils execution.

    Location:
      Under normal circumstances, the PTR can appear anywhere in the code_interface
      stream after the corresponding Part Information Record (PIR) and before
      the corresponding Part Result Record (PRR).  In addition, to facilitate
      conversion from STDF V3, if the first PTR for a test_utils contains default
      information only (no test_utils results), it may appear anywhere after the
      initial sequence, and before the first corresponding PTR , but need
      not appear between a PIR and PRR.

    Possible Use:
      * Datalog
      * Histogram
      * Wafer Map
    """

    TEST_NUM: int = 0
    HEAD_NUM: int = 0
    SITE_NUM: int = 0
    TEST_FLG: Ptr_TEST_FLG = None
    PARM_FLG: Ptr_PARM_FLG = None
    RESULT: float = .0
    TEST_TXT: str = ""
    # ALARM_ID = 0
    OPT_FLAG: Ptr_OPT_FLAG = None
    LO_LIMIT: float = .0
    HI_LIMIT: float = .0
    UNITS: str = ""

    def __str__(self):
        return "Site:{} Test:{} value:{} {} > Result:{}".format(
            self.SITE_NUM, self.TEST_TXT, self.RESULT, self.UNITS, 0 if self.TEST_FLG.test_failed() else 1
        )

    def __init__(self, **kwargs):
        self.TEST_FLG = Ptr_TEST_FLG()
        self.PARM_FLG = Ptr_PARM_FLG()
        self.OPT_FLAG = Ptr_OPT_FLAG()
        self.OPT_FLAG.set_unknown()
        for key, value in kwargs.items():
            setattr(self, key, value)

    def set_value(self, value: float):
        self.RESULT = value
        self.TEST_FLG.set_bit(0, False)
        self.TEST_FLG.set_bit(1, False)
        self.TEST_FLG.set_bit(2, False)
        self.TEST_FLG.set_bit(3, False)
        self.TEST_FLG.set_bit(4, False)
        self.TEST_FLG.set_bit(5, False)

        self.PARM_FLG.set_bit(0, False)
        self.PARM_FLG.set_bit(1, False)
        self.PARM_FLG.set_bit(2, False)


if __name__ == '__main__':
    ptr = Ptr()

    for each in filter(lambda m: not m.startswith('__') and not callable(getattr(ptr, m)), dir(ptr)):
        print(each)
