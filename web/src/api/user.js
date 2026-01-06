import service from '@/utils/request'

export function login(data) {
  return service({
    url: '/user/login',
    method: 'post',
    data
  })
}