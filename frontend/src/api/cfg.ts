import { api } from './request'
import type { 
  CFGGenerationRequest, 
  CFGGenerationResponse, 
  SupportedLanguage,
  ApiResponse 
} from '@/types'

export const cfgApi = {
  // 生成控制流图
  generateCFG: (data: CFGGenerationRequest) => {
    return api.post<CFGGenerationResponse>('/cfg/generate', data)
  },
  
  // 获取支持的编程语言
  getSupportedLanguages: () => {
    return api.get<{ languages: string[] }>('/cfg/languages')
  },
  
  // 获取CFG服务状态
  getCFGStatus: () => {
    return api.get('/cfg/status')
  }
}