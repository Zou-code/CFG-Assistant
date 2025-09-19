<template>
  <div class="code-editor">
    <div class="editor-header">
      <div class="editor-title">
        <el-icon><Document /></el-icon>
        代码编辑器
      </div>
      
      <div class="editor-controls">
        <!-- 语言选择 -->
        <el-select
          v-model="currentLanguage"
          @change="handleLanguageChange"
          size="small"
          style="width: 120px"
        >
          <el-option
            v-for="lang in supportedLanguages"
            :key="lang.value"
            :label="lang.label"
            :value="lang.value"
          />
        </el-select>

        <!-- 编辑器操作 -->
        <el-button-group size="small">
          <el-button @click="handleFormat">
            <el-icon><MagicStick /></el-icon>
            格式化
          </el-button>
          <el-button @click="handleClear">
            <el-icon><Delete /></el-icon>
            清空
          </el-button>
          <el-button @click="handleCopy">
            <el-icon><CopyDocument /></el-icon>
            复制
          </el-button>
        </el-button-group>

        <!-- 示例代码 -->
        <el-dropdown @command="handleLoadExample">
          <el-button size="small">
            <el-icon><FolderOpened /></el-icon>
            示例代码
            <el-icon class="el-icon--right"><ArrowDown /></el-icon>
          </el-button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item 
                v-for="example in examples"
                :key="example.name"
                :command="example"
              >
                {{ example.name }}
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </div>

    <div class="editor-container" ref="editorContainer">
      <div class="editor-loading" v-if="loading">
        <el-icon class="is-loading"><Loading /></el-icon>
        <span>编辑器加载中...</span>
      </div>
    </div>

    <div class="editor-footer">
      <div class="editor-info">
        <span class="info-item">
          <el-icon><Document /></el-icon>
          {{ currentLanguage }}
        </span>
        <span class="info-item">
          <el-icon><EditPen /></el-icon>
          行: {{ cursorPosition.line }}, 列: {{ cursorPosition.column }}
        </span>
        <span class="info-item">
          <el-icon><DataLine /></el-icon>
          {{ codeStats.lines }} 行, {{ codeStats.characters }} 字符
        </span>
      </div>
      
      <div class="editor-actions">
        <el-button 
          type="primary" 
          size="small"
          :loading="generating"
          :disabled="!code.trim()"
          @click="handleGenerate"
        >
          <el-icon><Promotion /></el-icon>
          生成CFG
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed, watch, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import {
  Document,
  MagicStick,
  Delete,
  CopyDocument,
  FolderOpened,
  ArrowDown,
  Loading,
  EditPen,
  DataLine,
  Promotion
} from '@element-plus/icons-vue'

import * as monaco from 'monaco-editor'
import type { LanguageType, SupportedLanguage } from '@/types'

// Props
interface Props {
  modelValue: string
  language: LanguageType
  supportedLanguages: SupportedLanguage[]
  generating?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  generating: false
})

// Emits
const emit = defineEmits<{
  'update:modelValue': [value: string]
  'language-change': [language: LanguageType]
  'generate': []
}>()

// 响应式数据
const editorContainer = ref<HTMLElement>()
const loading = ref(true)
const currentLanguage = ref<LanguageType>(props.language)
const cursorPosition = ref({ line: 1, column: 1 })

let editor: monaco.editor.IStandaloneCodeEditor | null = null

// 计算属性
const code = computed({
  get: () => props.modelValue,
  set: (value: string) => emit('update:modelValue', value)
})

const codeStats = computed(() => {
  const lines = code.value.split('\n').length
  const characters = code.value.length
  return { lines, characters }
})

// 示例代码
const examples = computed(() => {
  const exampleMap = {
    Python: [
      {
        name: '简单条件判断',
        code: `def check_number(x):
    if x > 0:
        print("正数")
    elif x < 0:
        print("负数")
    else:
        print("零")
    return x`
      },
      {
        name: '循环结构',
        code: `def factorial(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result`
      },
      {
        name: '异常处理',
        code: `def divide(a, b):
    try:
        result = a / b
        return result
    except ZeroDivisionError:
        print("除零错误")
        return None
    finally:
        print("计算完成")`
      }
    ],
    Java: [
      {
        name: '简单条件判断',
        code: `public class NumberChecker {
    public static void checkNumber(int x) {
        if (x > 0) {
            System.out.println("正数");
        } else if (x < 0) {
            System.out.println("负数");
        } else {
            System.out.println("零");
        }
    }
}`
      },
      {
        name: '循环结构',
        code: `public class Factorial {
    public static int factorial(int n) {
        int result = 1;
        for (int i = 1; i <= n; i++) {
            result *= i;
        }
        return result;
    }
}`
      }
    ],
    JavaScript: [
      {
        name: '简单条件判断',
        code: `function checkNumber(x) {
    if (x > 0) {
        console.log("正数");
    } else if (x < 0) {
        console.log("负数");
    } else {
        console.log("零");
    }
    return x;
}`
      },
      {
        name: '异步函数',
        code: `async function fetchData(url) {
    try {
        const response = await fetch(url);
        if (response.ok) {
            return await response.json();
        } else {
            throw new Error('请求失败');
        }
    } catch (error) {
        console.error('错误:', error);
        return null;
    }
}`
      }
    ]
  }
  
  return exampleMap[currentLanguage.value] || []
})

// 生命周期
onMounted(async () => {
  await initEditor()
})

onUnmounted(() => {
  if (editor) {
    editor.dispose()
  }
})

// 监听语言变化
watch(() => props.language, (newLang) => {
  currentLanguage.value = newLang
  updateEditorLanguage()
})

// 方法
const initEditor = async () => {
  if (!editorContainer.value) return

  try {
    // 配置Monaco Editor
    monaco.editor.defineTheme('custom-dark', {
      base: 'vs-dark',
      inherit: true,
      rules: [],
      colors: {
        'editor.background': '#1e1e1e',
        'editor.foreground': '#d4d4d4',
        'editorLineNumber.foreground': '#858585',
        'editor.selectionBackground': '#264f78',
        'editor.inactiveSelectionBackground': '#3a3d41'
      }
    })

    // 创建编辑器实例
    editor = monaco.editor.create(editorContainer.value, {
      value: code.value,
      language: getMonacoLanguage(currentLanguage.value),
      theme: 'custom-dark',
      fontSize: 14,
      lineNumbers: 'on',
      roundedSelection: false,
      scrollBeyondLastLine: false,
      automaticLayout: true,
      minimap: { enabled: false },
      wordWrap: 'on',
      tabSize: 4,
      insertSpaces: true,
      folding: true,
      lineDecorationsWidth: 10,
      lineNumbersMinChars: 3,
      renderLineHighlight: 'line',
      selectOnLineNumbers: true,
      scrollbar: {
        vertical: 'auto',
        horizontal: 'auto',
        verticalScrollbarSize: 8,
        horizontalScrollbarSize: 8
      }
    })

    // 监听内容变化
    editor.onDidChangeModelContent(() => {
      const value = editor?.getValue() || ''
      emit('update:modelValue', value)
    })

    // 监听光标位置变化
    editor.onDidChangeCursorPosition((e) => {
      cursorPosition.value = {
        line: e.position.lineNumber,
        column: e.position.column
      }
    })

    loading.value = false
  } catch (error) {
    console.error('编辑器初始化失败:', error)
    ElMessage.error('编辑器初始化失败')
    loading.value = false
  }
}

const getMonacoLanguage = (lang: LanguageType): string => {
  const languageMap = {
    Python: 'python',
    Java: 'java',
    JavaScript: 'javascript',
    TypeScript: 'typescript',
    'C++': 'cpp',
    C: 'c',
    'C#': 'csharp',
    Go: 'go',
    Rust: 'rust',
    PHP: 'php'
  }
  return languageMap[lang] || 'plaintext'
}

const updateEditorLanguage = () => {
  if (editor) {
    const model = editor.getModel()
    if (model) {
      monaco.editor.setModelLanguage(model, getMonacoLanguage(currentLanguage.value))
    }
  }
}

// 事件处理
const handleLanguageChange = () => {
  emit('language-change', currentLanguage.value)
  updateEditorLanguage()
}

const handleFormat = () => {
  if (editor) {
    editor.getAction('editor.action.formatDocument')?.run()
    ElMessage.success('代码已格式化')
  }
}

const handleClear = () => {
  if (editor) {
    editor.setValue('')
    ElMessage.success('代码已清空')
  }
}

const handleCopy = async () => {
  try {
    await navigator.clipboard.writeText(code.value)
    ElMessage.success('代码已复制到剪贴板')
  } catch (error) {
    console.error('复制失败:', error)
    ElMessage.error('复制失败')
  }
}

const handleLoadExample = (example: { name: string; code: string }) => {
  if (editor) {
    editor.setValue(example.code)
    ElMessage.success(`已加载示例: ${example.name}`)
  }
}

const handleGenerate = () => {
  if (!code.value.trim()) {
    ElMessage.warning('请先输入代码')
    return
  }
  emit('generate')
}
</script>

<style scoped>
.code-editor {
  height: 100%;
  display: flex;
  flex-direction: column;
  background: var(--el-bg-color);
  border: 1px solid var(--el-border-color);
  border-radius: 6px;
  overflow: hidden;
}

.editor-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: var(--el-bg-color-page);
  border-bottom: 1px solid var(--el-border-color);
}

.editor-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 600;
  color: var(--el-text-color-primary);
}

.editor-controls {
  display: flex;
  align-items: center;
  gap: 12px;
}

.editor-container {
  flex: 1;
  position: relative;
  min-height: 300px;
}

.editor-loading {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  color: var(--el-text-color-secondary);
}

.editor-loading .el-icon {
  font-size: 24px;
}

.editor-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 16px;
  background: var(--el-bg-color-page);
  border-top: 1px solid var(--el-border-color);
  font-size: 12px;
}

.editor-info {
  display: flex;
  align-items: center;
  gap: 16px;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 4px;
  color: var(--el-text-color-secondary);
}

.editor-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

/* Monaco Editor 样式覆盖 */
:deep(.monaco-editor) {
  border-radius: 0;
}

:deep(.monaco-editor .margin) {
  background-color: var(--el-bg-color-page);
}

:deep(.monaco-editor .monaco-editor-background) {
  background-color: var(--el-bg-color);
}
</style>