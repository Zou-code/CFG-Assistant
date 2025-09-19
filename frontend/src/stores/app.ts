import { defineStore } from 'pinia'
import { ref, computed, readonly } from 'vue'
import { ElMessage } from 'element-plus'
import type { ModelConfig, SupportedLanguage, SupportedModel } from '@/types'
import { cfgApi } from '@/api/cfg'
import { modelApi } from '@/api/model'

export const useAppStore = defineStore('app', () => {
  // 状态
  const loading = ref(false)
  const initialized = ref(false)
  const supportedLanguages = ref<SupportedLanguage[]>([])
  const supportedModels = ref<SupportedModel[]>([])
  
  // 当前配置
  const currentModelConfig = ref<ModelConfig>({
    modelName: 'gpt-4',
    clientName: 'openai',
    apiKey: '',
    temperature: 0.0,
    maxTokens: undefined
  })
  
  // 计算属性
  const isConfigured = computed(() => {
    return currentModelConfig.value.apiKey.trim() !== ''
  })
  
  // 方法
  const initialize = async () => {
    if (initialized.value) return
    
    loading.value = true
    try {
      // 并行加载支持的语言和模型
      const [languagesRes, modelsRes] = await Promise.all([
        cfgApi.getSupportedLanguages(),
        modelApi.getSupportedModels()
      ])
      
      supportedLanguages.value = languagesRes.data.languages.map(lang => ({
        value: lang,
        label: lang
      }))
      
      supportedModels.value = modelsRes.data.models
      
      initialized.value = true
    } catch (error) {
      console.error('初始化失败:', error)
      ElMessage.error('初始化应用失败，请刷新页面重试')
    } finally {
      loading.value = false
    }
  }
  
  const updateModelConfig = (config: Partial<ModelConfig>) => {
    currentModelConfig.value = {
      ...currentModelConfig.value,
      ...config
    }
  }
  
  const resetModelConfig = () => {
    currentModelConfig.value = {
      modelName: 'gpt-4',
      clientName: 'openai',
      apiKey: '',
      temperature: 0.0,
      maxTokens: undefined
    }
  }
  
  const setLoading = (value: boolean) => {
    loading.value = value
  }
  
  return {
    // 状态
    loading: readonly(loading),
    initialized: readonly(initialized),
    supportedLanguages: readonly(supportedLanguages),
    supportedModels: readonly(supportedModels),
    currentModelConfig: readonly(currentModelConfig),
    
    // 计算属性
    isConfigured,
    
    // 方法
    initialize,
    updateModelConfig,
    resetModelConfig,
    setLoading
  }
})