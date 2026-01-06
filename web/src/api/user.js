import service from '@/utils/request'

export function login(data) {
  return service({
    url: '/user/login/',
    method: 'post',
    data
  })
}

export function register(data) {
  return service({
    url: '/user/register/',
    method: 'post',
    data
  })
}