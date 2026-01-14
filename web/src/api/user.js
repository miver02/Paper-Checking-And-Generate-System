import service from '@/utils/request'

// 登录
export function login(data) {
  return service({
    url: '/user/login/',
    method: 'post',
    data,
  })
}

// 注册
export function register(data) {
  return service({
    url: '/user/register/',
    method: 'post',
    data,
  })
}

// 获取用户信息
export function getProfile() {
  return service({
    url: '/user/profile/',
    method: 'get',
  })
}

// 更新用户信息
export function updateProfile(data) {
  return service({
    url: '/user/profile/',
    method: 'patch',
    data,
  })
}
