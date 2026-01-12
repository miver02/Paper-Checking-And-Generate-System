import service from '@/utils/request'

export function login(data) {
  return service({
    url: '/user/login/',
    method: 'post',
    data,
  })
}

export function register(data) {
  return service({
    url: '/user/register/',
    method: 'post',
    data,
  })
}

export function getProfile() {
  return service({
    url: '/user/profile/',
    method: 'get',
  })
}

export function updateProfile(data) {
  return service({
    url: '/user/profile/',
    method: 'patch',
    data,
  })
}
