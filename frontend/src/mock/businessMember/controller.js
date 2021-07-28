import Mock from 'mockjs';
import get from './data/get';
import save from './data/save';
import list from './data/list';
import disable from './data/disable';
import enable from './data/enable';

//通过pnr编码获取 pnr信息
Mock.mock('http://localhost:8091/member-manage/businessMember/get', 'get', get);
Mock.mock('/member-manage/businessMember/save', 'post', save);
Mock.mock('/member-manage/businessMember/list', 'get', list);
Mock.mock('/member-manage/businessMember/disable', 'post', disable);
Mock.mock('/member-manage/businessMember/enable', 'post', enable);
