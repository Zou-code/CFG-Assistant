// 基础类型定义
export type LanguageType = 'Python' | 'Java' | 'C'
export type ModelType = 'gpt-4' | 'gpt-4-turbo' | 'gpt-4o' | 'gpt-3.5-turbo' | 'deepseek-chat'
export type ClientType = 'openai' | 'deepseek'

// 接口定义
export interface SupportedLanguage {
  value: LanguageType
  label: string
}

export interface SupportedModel {
  name: ModelType
  client: ClientType
  display_name?: string
  description?: string
}

export interface ModelConfig {
  modelName: ModelType
  clientName: ClientType
  apiKey: string
  temperature: number
  maxTokens?: number
}

export interface CFGGenerationRequest {
  code: string
  language: LanguageType
  model_name: ModelType
  client_name: ClientType
  temperature: number
  api_key?: string
}

export interface CFGGenerationResponse {
  success: boolean
  message: string
  graph_data?: GraphData
  graph_code?: string
  image_url?: string
  processing_time?: number
}

export interface GraphData {
  nodes: GraphNode[]
  edges: GraphEdge[]
  type: string
}

export interface GraphNode {
  id: string
  label: string
  x?: number
  y?: number
  size?: number
  color?: string
}

export interface GraphEdge {
  source: string
  target: string
  label?: string
  color?: string
  size?: number
}

export interface ApiResponse<T = any> {
  data: T
  message?: string
  success?: boolean
}

export interface ErrorResponse {
  success: boolean
  error: string
  error_code?: string
  details?: Record<string, any>
}

// 编辑器相关类型
export interface EditorConfig {
  language: LanguageType
  theme: 'vs-dark' | 'vs-light'
  fontSize: number
  wordWrap: 'on' | 'off'
  minimap: boolean
}

// 图形可视化相关类型
export interface GraphVisualizationConfig {
  layout: 'force' | 'circular' | 'hierarchical'
  nodeSize: number
  edgeSize: number
  showLabels: boolean
  enableZoom: boolean
  enableDrag: boolean
}

// 应用状态类型
export interface AppState {
  loading: boolean
  initialized: boolean
  currentLanguage: LanguageType
  currentCode: string
  currentGraph?: GraphData
  editorConfig: EditorConfig
  graphConfig: GraphVisualizationConfig
}

// 组件Props类型
export interface ConfigPanelProps {
  modelConfig: ModelConfig
  supportedModels: SupportedModel[]
  supportedLanguages: SupportedLanguage[]
}

export interface CodeEditorProps {
  language: LanguageType
  code: string
  config: EditorConfig
}

export interface GraphViewerProps {
  graphData?: GraphData
  config: GraphVisualizationConfig
  imageUrl?: string
}

// 事件类型
export interface ModelConfigChangeEvent {
  config: ModelConfig
}

export interface CodeChangeEvent {
  code: string
  language: LanguageType
}

export interface GraphGeneratedEvent {
  graphData: GraphData
  imageUrl?: string
  processingTime: number
}