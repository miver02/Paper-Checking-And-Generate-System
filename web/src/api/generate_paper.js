import service from '@/utils/request'

export function generatePaper(data) {
  return service({
    url: '/paper/generate/all/',
    method: 'post',
    data,
  })
}

export function getPaperStatus(paperId) {
  return service({
    url: `/paper/generate/${paperId}/status/`,
    method: 'get',
  })
}
