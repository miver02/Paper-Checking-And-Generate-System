import service from '@/utils/request'

export const login = data => {
  return service({
    url: '/user/token/',
    method: 'post',
    data,
  })
}

export const refreshToken = data => {
  return service({
    url: '/user/token/refresh/',
    method: 'post',
    data,
  })
}

export const verifyToken = data => {
  return service({
    url: '/user/token/verify/',
    method: 'post',
    data,
  })
}

export const logout = () => {
  return service({
    url: '/user/logout/',
    method: 'post',
  })
}
