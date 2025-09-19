<template>
  <div class="home-container">
    <!-- 顶部工具栏 -->
    <div class="toolbar">
      <div class="toolbar-left">
        <h1 class="title">
          <el-icon><Cpu /></el-icon>
          CFG Assistant
        </h1>
        <span class="subtitle">控制流图生成助手</span>
      </div>
      <div class="toolbar-right">
        <el-button 
          type="primary" 
          :loading="generating"
          :disabled="!canGenerate"
          @click="handleGenerate"
        >
          <el-icon><VideoPlay /></el-icon>
          生成控制流图
        </el-button>
        <el-button @click="handleClear">
          <el-icon><Delete /></el-icon>
          清空
        </el-button>
      </div>
    </div>

    <!-- 主要内容区域 -->
    <div class="main-content">
      <!-- 左侧配置面板 -->
      <div class="left-panel">
        <ConfigPanel
          :model-config="modelConfig"
          :supported-models="appStore.supportedModels"
          :supported-languages="appStore.supportedLanguages"
          @config-change="handleConfigChange"
          @language-change="handleLanguageChange"
        />
      </div>

      <!-- 中央代码编辑区 -->
      <div class="center-panel">
        <CodeEditor
          v-model="currentCode"
          :language="currentLanguage"
          :supported-languages="appStore.supportedLanguages"
          :generating="generating"
          @language-change="handleLanguageChange"
          @generate="handleGenerate"
        />
      </div>

      <!-- 右侧图形展示区 -->
      <div class="right-panel">
        <GraphViewer
          :graph-data="cfgData"
          :loading="generating"
          :generation-time="generationTime"
        />
      </div>
    </div>

    <!-- 状态栏 -->
    <div class="status-bar">
      <div class="status-left">
        <span v-if="lastGenerationTime">
          上次生成耗时: {{ lastGenerationTime.toFixed(2) }}s
        </span>
      </div>
      <div class="status-right">
        <span :class="['status-indicator', appStore.isConfigured ? 'configured' : 'not-configured']">
          {{ appStore.isConfigured ? '已配置' : '未配置' }}
        </span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Cpu, VideoPlay, Delete } from '@element-plus/icons-vue'

import ConfigPanel from '@/components/ConfigPanel.vue'
import CodeEditor from '@/components/CodeEditor.vue'
import GraphViewer from '@/components/GraphViewer.vue'

import { useAppStore } from '@/stores/app'
import { cfgApi } from '@/api/cfg'
import type { 
  ModelConfig, 
  LanguageType, 
  GraphData, 
  CFGGenerationRequest 
} from '@/types'

const appStore = useAppStore()

// 响应式数据
const generating = ref(false)
const generationTime = ref(0)
const currentLanguage = ref<LanguageType>('Python')
const currentCode = ref('')
const cfgData = ref<GraphData | null>(null)
const lastGenerationTime = ref<number>()

// 模型配置
const modelConfig = ref<ModelConfig>({
  modelName: 'gpt-4',
  clientName: 'openai',
  apiKey: '',
  temperature: 0.0,
  maxTokens: undefined
})

// 计算属性
const canGenerate = computed(() => {
  return currentCode.value.trim() !== '' && 
         modelConfig.value.apiKey.trim() !== '' &&
         !generating.value
})

// 事件处理
const handleConfigChange = (config: ModelConfig) => {
  modelConfig.value = { ...config }
  appStore.updateModelConfig(config)
}

const handleCodeChange = (code: string) => {
  currentCode.value = code
}

const handleLanguageChange = (language: LanguageType) => {
  currentLanguage.value = language
}

const handleGenerate = async () => {
  if (!canGenerate.value) {
    ElMessage.warning('请检查代码内容和模型配置')
    return
  }

  generating.value = true
  const startTime = Date.now()
  
  try {
    const request: CFGGenerationRequest = {
      code: currentCode.value,
      language: currentLanguage.value,
      model_name: modelConfig.value.modelName,
      client_name: modelConfig.value.clientName,
      temperature: modelConfig.value.temperature,
      api_key: modelConfig.value.apiKey
    }

    const response = await cfgApi.generateCFG(request)
    const result = response.data

    if (result.success) {
      cfgData.value = result.graph_data
      generationTime.value = Date.now() - startTime
      lastGenerationTime.value = result.processing_time
      
      ElMessage.success('控制流图生成成功！')
    } else {
      ElMessage.error(result.message || '生成失败')
    }
  } catch (error) {
    console.error('生成CFG失败:', error)
    ElMessage.error('生成控制流图失败，请检查网络连接和配置')
  } finally {
    generating.value = false
  }
}

const handleClear = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要清空所有内容吗？',
      '确认清空',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    currentCode.value = ''
    cfgData.value = null
    lastGenerationTime.value = undefined
    
    ElMessage.success('已清空所有内容')
  } catch {
    // 用户取消操作
  }
}

// 示例代码
const exampleCodes = {
  Python: `def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)

def main():
    num = 10
    for i in range(num):
        print(f"F({i}) = {fibonacci(i)}")

if __name__ == "__main__":
    main()`,
  
  Java: `public class QuickSort {
    public static void quickSort(int[] arr, int low, int high) {
        if (low < high) {
            int pi = partition(arr, low, high);
            quickSort(arr, low, pi - 1);
            quickSort(arr, pi + 1, high);
        }
    }
    
    public static int partition(int[] arr, int low, int high) {
        int pivot = arr[high];
        int i = (low - 1);
        
        for (int j = low; j < high; j++) {
            if (arr[j] < pivot) {
                i++;
                int temp = arr[i];
                arr[i] = arr[j];
                arr[j] = temp;
            }
        }
        
        int temp = arr[i + 1];
        arr[i + 1] = arr[high];
        arr[high] = temp;
        
        return i + 1;
    }
}`,
  
  C: `#include <stdio.h>

int factorial(int n) {
    if (n <= 1) {
        return 1;
    } else {
        return n * factorial(n - 1);
    }
}

int main() {
    int num = 5;
    int result = factorial(num);
    printf("Factorial of %d is %d\\n", num, result);
    return 0;
}`
}

// 组件挂载时的初始化
onMounted(() => {
  // 设置示例代码
  currentCode.value = exampleCodes[currentLanguage.value]
})

// 监听语言变化，更新示例代码
watch(currentLanguage, (newLang) => {
  if (!currentCode.value.trim()) {
    currentCode.value = exampleCodes[newLang]
  }
})
</script>

<style scoped>
.home-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: var(--el-bg-color);
}

.toolbar {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  border-bottom: 1px solid var(--el-border-color);
  background-color: var(--el-bg-color-page);
}

.toolbar-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.title {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
  color: var(--el-text-color-primary);
  display: flex;
  align-items: center;
  gap: 8px;
}

.subtitle {
  font-size: 14px;
  color: var(--el-text-color-regular);
}

.toolbar-right {
  display: flex;
  gap: 12px;
}

.main-content {
  flex: 1;
  display: flex;
  min-height: 0;
}

.left-panel {
  width: 320px;
  border-right: 1px solid var(--el-border-color);
  background-color: var(--el-bg-color-page);
}

.center-panel {
  flex: 1;
  min-width: 0;
}

.right-panel {
  width: 400px;
  border-left: 1px solid var(--el-border-color);
  background-color: var(--el-bg-color-page);
}

.status-bar {
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  border-top: 1px solid var(--el-border-color);
  background-color: var(--el-bg-color-page);
  font-size: 12px;
  color: var(--el-text-color-regular);
}

.status-indicator {
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
}

.status-indicator.configured {
  background-color: var(--el-color-success-light-9);
  color: var(--el-color-success);
}

.status-indicator.not-configured {
  background-color: var(--el-color-warning-light-9);
  color: var(--el-color-warning);
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .left-panel {
    width: 280px;
  }
  
  .right-panel {
    width: 350px;
  }
}

@media (max-width: 768px) {
  .main-content {
    flex-direction: column;
  }
  
  .left-panel,
  .right-panel {
    width: 100%;
    height: 200px;
  }
  
  .center-panel {
    flex: 1;
  }
}
</style>