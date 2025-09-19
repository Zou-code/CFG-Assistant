<template>
  <div class="config-panel">
    <div class="panel-header">
      <h3>
        <el-icon><Setting /></el-icon>
        模型配置
      </h3>
    </div>

    <div class="panel-content">
      <!-- 模型选择 -->
      <div class="config-section">
        <label class="config-label">模型选择</label>
        <el-select
          v-model="localConfig.modelName"
          placeholder="选择模型"
          @change="handleModelChange"
          style="width: 100%"
        >
          <el-option
            v-for="model in supportedModels"
            :key="model.name"
            :label="model.display_name"
            :value="model.name"
          >
            <div class="model-option">
              <span class="model-name">{{ model.display_name }}</span>
              <span class="model-client">{{ model.client }}</span>
            </div>
          </el-option>
        </el-select>
      </div>

      <!-- 客户端类型 -->
      <div class="config-section">
        <label class="config-label">客户端类型</label>
        <el-radio-group 
          v-model="localConfig.clientName"
          @change="handleClientChange"
        >
          <el-radio label="openai">OpenAI</el-radio>
          <el-radio label="deepseek">DeepSeek</el-radio>
        </el-radio-group>
      </div>

      <!-- API密钥 -->
      <div class="config-section">
        <label class="config-label">
          API密钥
          <el-tooltip content="请输入对应模型的API密钥" placement="top">
            <el-icon class="help-icon"><QuestionFilled /></el-icon>
          </el-tooltip>
        </label>
        <el-input
          v-model="localConfig.apiKey"
          type="password"
          placeholder="请输入API密钥"
          show-password
          @input="handleApiKeyChange"
        />
        <div class="api-key-status">
          <el-icon 
            :class="['status-icon', apiKeyStatus.type]"
          >
            <component :is="apiKeyStatus.icon" />
          </el-icon>
          <span :class="['status-text', apiKeyStatus.type]">
            {{ apiKeyStatus.text }}
          </span>
        </div>
      </div>

      <!-- 温度参数 -->
      <div class="config-section">
        <label class="config-label">
          温度参数: {{ localConfig.temperature }}
          <el-tooltip content="控制模型输出的随机性，0表示确定性输出，2表示最大随机性" placement="top">
            <el-icon class="help-icon"><QuestionFilled /></el-icon>
          </el-tooltip>
        </label>
        <el-slider
          v-model="localConfig.temperature"
          :min="0"
          :max="2"
          :step="0.1"
          :show-tooltip="false"
          @change="handleTemperatureChange"
        />
      </div>

      <!-- 最大Token数 -->
      <div class="config-section">
        <label class="config-label">
          最大Token数
          <el-tooltip content="限制模型输出的最大token数量，留空表示使用默认值" placement="top">
            <el-icon class="help-icon"><QuestionFilled /></el-icon>
          </el-tooltip>
        </label>
        <el-input-number
          v-model="localConfig.maxTokens"
          :min="1"
          :max="4096"
          placeholder="默认"
          @change="handleMaxTokensChange"
          style="width: 100%"
        />
      </div>

      <!-- 语言选择 -->
      <div class="config-section">
        <label class="config-label">编程语言</label>
        <el-select
          v-model="selectedLanguage"
          placeholder="选择编程语言"
          @change="handleLanguageChange"
          style="width: 100%"
        >
          <el-option
            v-for="lang in supportedLanguages"
            :key="lang.value"
            :label="lang.label"
            :value="lang.value"
          />
        </el-select>
      </div>

      <!-- 操作按钮 -->
      <div class="config-actions">
        <el-button 
          type="primary" 
          :loading="testing"
          @click="handleTestConnection"
          style="width: 100%"
        >
          <el-icon><Connection /></el-icon>
          测试连接
        </el-button>
        
        <el-button 
          @click="handleReset"
          style="width: 100%; margin-top: 8px;"
        >
          <el-icon><Refresh /></el-icon>
          重置配置
        </el-button>
      </div>

      <!-- 配置预设 -->
      <div class="config-section">
        <label class="config-label">配置预设</label>
        <el-select
          v-model="selectedPreset"
          placeholder="选择预设配置"
          @change="handlePresetChange"
          style="width: 100%"
        >
          <el-option label="GPT-4 (推荐)" value="gpt4" />
          <el-option label="GPT-4 Turbo" value="gpt4-turbo" />
          <el-option label="GPT-3.5 Turbo" value="gpt35" />
          <el-option label="DeepSeek Chat" value="deepseek" />
        </el-select>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { 
  Setting, 
  QuestionFilled, 
  Connection, 
  Refresh,
  SuccessFilled,
  WarningFilled,
  CircleCloseFilled
} from '@element-plus/icons-vue'

import { modelApi } from '@/api/model'
import type { 
  ModelConfig, 
  SupportedModel, 
  SupportedLanguage,
  LanguageType 
} from '@/types'

// Props
interface Props {
  modelConfig: ModelConfig
  supportedModels: SupportedModel[]
  supportedLanguages: SupportedLanguage[]
}

const props = defineProps<Props>()

// Emits
const emit = defineEmits<{
  configChange: [config: ModelConfig]
  languageChange: [language: LanguageType]
}>()

// 响应式数据
const localConfig = ref<ModelConfig>({ ...props.modelConfig })
const selectedLanguage = ref<LanguageType>('Python')
const selectedPreset = ref('')
const testing = ref(false)

// 计算属性
const apiKeyStatus = computed(() => {
  if (!localConfig.value.apiKey.trim()) {
    return {
      type: 'warning',
      icon: WarningFilled,
      text: '请输入API密钥'
    }
  }
  
  if (localConfig.value.apiKey.length < 20) {
    return {
      type: 'error',
      icon: CircleCloseFilled,
      text: 'API密钥格式不正确'
    }
  }
  
  return {
    type: 'success',
    icon: SuccessFilled,
    text: 'API密钥格式正确'
  }
})

// 监听props变化
watch(() => props.modelConfig, (newConfig) => {
  localConfig.value = { ...newConfig }
}, { deep: true })

// 事件处理
const handleModelChange = () => {
  // 根据模型自动设置客户端
  if (localConfig.value.modelName.startsWith('gpt')) {
    localConfig.value.clientName = 'openai'
  } else if (localConfig.value.modelName === 'deepseek-chat') {
    localConfig.value.clientName = 'deepseek'
  }
  
  emitConfigChange()
}

const handleClientChange = () => {
  emitConfigChange()
}

const handleApiKeyChange = () => {
  emitConfigChange()
}

const handleTemperatureChange = () => {
  emitConfigChange()
}

const handleMaxTokensChange = () => {
  emitConfigChange()
}

const handleLanguageChange = () => {
  emit('languageChange', selectedLanguage.value)
}

const handleTestConnection = async () => {
  if (!localConfig.value.apiKey.trim()) {
    ElMessage.warning('请先输入API密钥')
    return
  }

  testing.value = true
  
  try {
    await modelApi.testModel(
      localConfig.value.modelName,
      localConfig.value.clientName,
      localConfig.value.apiKey
    )
    
    ElMessage.success('模型连接测试成功！')
  } catch (error) {
    console.error('测试连接失败:', error)
    ElMessage.error('模型连接测试失败，请检查API密钥和网络连接')
  } finally {
    testing.value = false
  }
}

const handleReset = () => {
  localConfig.value = {
    modelName: 'gpt-4',
    clientName: 'openai',
    apiKey: '',
    temperature: 0.0,
    maxTokens: undefined
  }
  selectedPreset.value = ''
  emitConfigChange()
  ElMessage.success('配置已重置')
}

const handlePresetChange = () => {
  const presets = {
    'gpt4': {
      modelName: 'gpt-4' as const,
      clientName: 'openai' as const,
      temperature: 0.0,
      maxTokens: undefined
    },
    'gpt4-turbo': {
      modelName: 'gpt-4-turbo' as const,
      clientName: 'openai' as const,
      temperature: 0.0,
      maxTokens: undefined
    },
    'gpt35': {
      modelName: 'gpt-3.5-turbo' as const,
      clientName: 'openai' as const,
      temperature: 0.0,
      maxTokens: undefined
    },
    'deepseek': {
      modelName: 'deepseek-chat' as const,
      clientName: 'deepseek' as const,
      temperature: 0.0,
      maxTokens: undefined
    }
  }
  
  const preset = presets[selectedPreset.value as keyof typeof presets]
  if (preset) {
    localConfig.value = {
      ...localConfig.value,
      ...preset
    }
    emitConfigChange()
    ElMessage.success(`已应用 ${selectedPreset.value} 预设配置`)
  }
}

const emitConfigChange = () => {
  emit('configChange', { ...localConfig.value })
}
</script>

<style scoped>
.config-panel {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.panel-header {
  padding: 16px 20px;
  border-bottom: 1px solid var(--el-border-color);
}

.panel-header h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: var(--el-text-color-primary);
  display: flex;
  align-items: center;
  gap: 8px;
}

.panel-content {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}

.config-section {
  margin-bottom: 24px;
}

.config-section:last-child {
  margin-bottom: 0;
}

.config-label {
  display: flex;
  align-items: center;
  gap: 4px;
  margin-bottom: 8px;
  font-size: 14px;
  font-weight: 500;
  color: var(--el-text-color-primary);
}

.help-icon {
  font-size: 14px;
  color: var(--el-text-color-placeholder);
  cursor: help;
}

.model-option {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.model-name {
  font-weight: 500;
}

.model-client {
  font-size: 12px;
  color: var(--el-text-color-secondary);
  background-color: var(--el-fill-color-light);
  padding: 2px 6px;
  border-radius: 4px;
}

.api-key-status {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-top: 6px;
  font-size: 12px;
}

.status-icon {
  font-size: 14px;
}

.status-icon.success {
  color: var(--el-color-success);
}

.status-icon.warning {
  color: var(--el-color-warning);
}

.status-icon.error {
  color: var(--el-color-error);
}

.status-text.success {
  color: var(--el-color-success);
}

.status-text.warning {
  color: var(--el-color-warning);
}

.status-text.error {
  color: var(--el-color-error);
}

.config-actions {
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px solid var(--el-border-color-lighter);
}

/* 滚动条样式 */
.panel-content::-webkit-scrollbar {
  width: 6px;
}

.panel-content::-webkit-scrollbar-track {
  background: transparent;
}

.panel-content::-webkit-scrollbar-thumb {
  background: var(--el-border-color);
  border-radius: 3px;
}
</style>