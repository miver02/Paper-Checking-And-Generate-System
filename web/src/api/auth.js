import service from '@/utils/request'

export const login = data => {
  return service({
    url: '/token/',
    method: 'post',
    data,
  })
}

export const refreshToken = data => {
  return service({
    url: '/token/refresh/',
    method: 'post',
    data,
  })
}

export const verifyToken = data => {
  return service({
    url: '/token/verify/',
    method: 'post',
    data,
  })
}
