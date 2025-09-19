import { api } from './request'
import type { 
  ModelConfig, 
  SupportedModel,
  ApiResponse 
} from '@/types'

export const modelApi = {
  // 获取支持的模型列表
  getSupportedModels: () => {
    return api.get<{ models: SupportedModel[] }>('/models/list')
  },
  
  // 配置模型
  configureModel: (data: ModelConfig) => {
    return api.post('/models/config', {
      model_name: data.modelName,
      client_name: data.clientName,
      api_key: data.apiKey,
      temperature: data.temperature,
      max_tokens: data.maxTokens
    })
  },
  
  // 测试模型连接
  testModel: (modelName: string, clientName: string, apiKey?: string) => {
    const params = new URLSearchParams()
    params.append('client_name', clientName)
    if (apiKey) {
      params.append('api_key', apiKey)
    }
    return api.get(`/models/test/${modelName}?${params.toString()}`)
  }
}