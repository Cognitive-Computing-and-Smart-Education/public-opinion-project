export default {
    SUCCESS: "000000" // 操作成功
    ,WORK_ERROR: "000001"//操作失败
    ,EXCEL_VERIFY_FAIL: "000002"//excel导入验证失败,请根据提示修改后重新上传!
    ,IS_MOCK: process.env.NODE_ENV === 'mock' //是否为mock环境
    ,LOGOUT_SUCCESS:'000006' //退出成功
};
