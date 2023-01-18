#   -*- coding:utf-8 -*-
#   The pk_error_cn.py in pk_gui
#   created by Jiang Feng(silencejiang@zju.edu.cn)
#   created at 3:19 on 2023/1/7
from pk.pk import PK
class PkError:
    errors = {
        PK.ALL_CHECKS_OK : "输入数据格式检查无误！",
        PK.ALL_CALCULATION_OK : "输入数据计算完成！",
        PK.CHECK_CASE_ERROR_DATA_FRAME_COLUMNS : "输入数据错误！列数过少！",
        PK.CHECK_CASE_ERROR_XY_TYPE : "输入数据错误！X、Y列不是有效的数据类型！",
        PK.CHECK_CASE_ERROR_UNKNOWN_TYPE : "输入数据错误！不支持的输入数据类型！",
        PK.CHECK_CASE_ERROR_CONTAIN_NON_NUM : "输入数据错误！包含非数字类型的输入！",
        PK.CHECK_CASE_ERROR_CONTAIN_NON_NAN : "输入数据错误！包含NaN类型的输入！",
        PK.CHECK_CASE_ERROR_NUMS : "输入数据错误！数据行数过少，观测数据数量不够！",
        PK.CHECK_Y_ERROR_CONTAIN_VALUES : "输入数据错误！Y值观测值值域过少，需大于等于2个！",
        PK.JACKKNIFE_WARN : "警告！无法按刀切法（jackknife）进行非参数估计；对于只有两个观测值的输入Y值，每个观测值需至少包含两个测试案例！",
    }