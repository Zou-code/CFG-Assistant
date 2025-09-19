<template>
  <div class="graph-viewer">
    <div class="viewer-header">
      <div class="viewer-title">
        <el-icon><Share /></el-icon>
        控制流图
      </div>
      
      <div class="viewer-controls">
        <!-- 布局选择 -->
        <el-select
          v-model="layoutType"
          @change="handleLayoutChange"
          size="small"
          style="width: 120px"
        >
          <el-option label="层次布局" value="hierarchical" />
          <el-option label="力导向" value="force" />
          <el-option label="圆形布局" value="circular" />
          <el-option label="网格布局" value="grid" />
        </el-select>

        <!-- 缩放控制 -->
        <el-button-group size="small">
          <el-button @click="handleZoomIn">
            <el-icon><ZoomIn /></el-icon>
          </el-button>
          <el-button @click="handleZoomOut">
            <el-icon><ZoomOut /></el-icon>
          </el-button>
          <el-button @click="handleZoomReset">
            <el-icon><Refresh /></el-icon>
          </el-button>
        </el-button-group>

        <!-- 导出功能 -->
        <el-dropdown @command="handleExport">
          <el-button size="small">
            <el-icon><Download /></el-icon>
            导出
            <el-icon class="el-icon--right"><ArrowDown /></el-icon>
          </el-button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="png">导出为PNG</el-dropdown-item>
              <el-dropdown-item command="svg">导出为SVG</el-dropdown-item>
              <el-dropdown-item command="json">导出为JSON</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>

        <!-- 全屏切换 -->
        <el-button size="small" @click="toggleFullscreen">
          <el-icon><FullScreen /></el-icon>
          全屏
        </el-button>
      </div>
    </div>

    <div class="viewer-container" ref="viewerContainer">
      <!-- 加载状态 -->
      <div v-if="loading" class="viewer-loading">
        <el-icon class="is-loading"><Loading /></el-icon>
        <span>正在生成控制流图...</span>
      </div>

      <!-- 空状态 -->
      <div v-else-if="!graphData" class="viewer-empty">
        <el-icon><DocumentCopy /></el-icon>
        <h3>暂无图形数据</h3>
        <p>请在左侧输入代码并点击"生成CFG"按钮</p>
      </div>

      <!-- 图形容器 -->
      <div v-else class="graph-container" ref="graphContainer"></div>
    </div>

    <div class="viewer-footer" v-if="graphData">
      <div class="graph-info">
        <span class="info-item">
          <el-icon><Connection /></el-icon>
          节点: {{ nodeCount }}
        </span>
        <span class="info-item">
          <el-icon><Share /></el-icon>
          边: {{ edgeCount }}
        </span>
        <span class="info-item">
          <el-icon><Timer /></el-icon>
          生成时间: {{ generationTime }}ms
        </span>
      </div>
      
      <div class="graph-actions">
        <el-button size="small" @click="handleFitToView">
          <el-icon><Aim /></el-icon>
          适应窗口
        </el-button>
        <el-button size="small" @click="handleCenterGraph">
          <el-icon><Position /></el-icon>
          居中显示
        </el-button>
      </div>
    </div>

    <!-- 节点详情弹窗 -->
    <el-dialog
      v-model="nodeDialogVisible"
      :title="`节点详情 - ${selectedNode?.id}`"
      width="600px"
    >
      <div v-if="selectedNode" class="node-details">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="节点ID">
            {{ selectedNode.id }}
          </el-descriptions-item>
          <el-descriptions-item label="节点类型">
            <el-tag :type="getNodeTypeColor(selectedNode.type)">
              {{ selectedNode.type }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="代码行数" span="2">
            {{ selectedNode.line_start }} - {{ selectedNode.line_end }}
          </el-descriptions-item>
        </el-descriptions>
        
        <div class="node-code" v-if="selectedNode.code">
          <h4>代码内容</h4>
          <pre><code>{{ selectedNode.code }}</code></pre>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch, computed } from 'vue'
import { ElMessage } from 'element-plus'
import {
  Share,
  ZoomIn,
  ZoomOut,
  Refresh,
  Download,
  ArrowDown,
  FullScreen,
  Loading,
  DocumentCopy,
  Connection,
  Timer,
  Aim,
  Position
} from '@element-plus/icons-vue'

import * as d3 from 'd3'
import type { CFGNode, CFGEdge, CFGData } from '@/types'

// Props
interface Props {
  graphData?: CFGData
  loading?: boolean
  generationTime?: number
}

const props = withDefaults(defineProps<Props>(), {
  loading: false,
  generationTime: 0
})

// 响应式数据
const viewerContainer = ref<HTMLElement>()
const graphContainer = ref<HTMLElement>()
const layoutType = ref('hierarchical')
const nodeDialogVisible = ref(false)
const selectedNode = ref<CFGNode | null>(null)

let svg: d3.Selection<SVGSVGElement, unknown, null, undefined> | null = null
let simulation: d3.Simulation<CFGNode, CFGEdge> | null = null
let zoom: d3.ZoomBehavior<SVGSVGElement, unknown> | null = null

// 计算属性
const nodeCount = computed(() => props.graphData?.nodes?.length || 0)
const edgeCount = computed(() => props.graphData?.edges?.length || 0)

// 生命周期
onMounted(() => {
  initGraph()
})

onUnmounted(() => {
  if (simulation) {
    simulation.stop()
  }
})

// 监听图形数据变化
watch(() => props.graphData, (newData) => {
  if (newData) {
    renderGraph(newData)
  }
}, { deep: true })

// 方法
const initGraph = () => {
  if (!graphContainer.value) return

  const container = d3.select(graphContainer.value)
  container.selectAll('*').remove()

  // 创建SVG
  svg = container
    .append('svg')
    .attr('width', '100%')
    .attr('height', '100%')
    .style('background-color', '#fafafa')

  // 添加缩放功能
  zoom = d3.zoom<SVGSVGElement, unknown>()
    .scaleExtent([0.1, 3])
    .on('zoom', (event) => {
      svg?.select('g').attr('transform', event.transform)
    })

  svg.call(zoom)

  // 创建主容器组
  svg.append('g').attr('class', 'graph-group')
}

const renderGraph = (data: CFGData) => {
  if (!svg || !data.nodes || !data.edges) return

  const width = graphContainer.value?.clientWidth || 800
  const height = graphContainer.value?.clientHeight || 600

  // 清除之前的内容
  svg.select('.graph-group').selectAll('*').remove()

  const g = svg.select('.graph-group')

  // 创建箭头标记
  const defs = svg.select('defs').empty() ? svg.append('defs') : svg.select('defs')
  
  defs.selectAll('marker').remove()
  defs.append('marker')
    .attr('id', 'arrowhead')
    .attr('viewBox', '0 -5 10 10')
    .attr('refX', 25)
    .attr('refY', 0)
    .attr('markerWidth', 6)
    .attr('markerHeight', 6)
    .attr('orient', 'auto')
    .append('path')
    .attr('d', 'M0,-5L10,0L0,5')
    .attr('fill', '#666')

  // 根据布局类型设置节点位置
  const nodes = [...data.nodes]
  const edges = [...data.edges]

  switch (layoutType.value) {
    case 'hierarchical':
      layoutHierarchical(nodes, edges, width, height)
      break
    case 'force':
      layoutForce(nodes, edges, width, height)
      break
    case 'circular':
      layoutCircular(nodes, width, height)
      break
    case 'grid':
      layoutGrid(nodes, width, height)
      break
  }

  // 绘制边
  const link = g.selectAll('.edge')
    .data(edges)
    .enter()
    .append('line')
    .attr('class', 'edge')
    .attr('stroke', '#666')
    .attr('stroke-width', 2)
    .attr('marker-end', 'url(#arrowhead)')
    .attr('x1', d => getNodeById(nodes, d.source)?.x || 0)
    .attr('y1', d => getNodeById(nodes, d.source)?.y || 0)
    .attr('x2', d => getNodeById(nodes, d.target)?.x || 0)
    .attr('y2', d => getNodeById(nodes, d.target)?.y || 0)

  // 绘制节点
  const node = g.selectAll('.node')
    .data(nodes)
    .enter()
    .append('g')
    .attr('class', 'node')
    .attr('transform', d => `translate(${d.x},${d.y})`)
    .style('cursor', 'pointer')
    .on('click', (event, d) => {
      selectedNode.value = d
      nodeDialogVisible.value = true
    })

  // 节点背景
  node.append('rect')
    .attr('width', 120)
    .attr('height', 60)
    .attr('x', -60)
    .attr('y', -30)
    .attr('rx', 8)
    .attr('fill', d => getNodeColor(d.type))
    .attr('stroke', '#333')
    .attr('stroke-width', 2)

  // 节点文本
  node.append('text')
    .attr('text-anchor', 'middle')
    .attr('dy', '0.35em')
    .attr('fill', '#333')
    .attr('font-size', '12px')
    .attr('font-weight', 'bold')
    .text(d => d.id)

  // 节点类型标签
  node.append('text')
    .attr('text-anchor', 'middle')
    .attr('dy', '1.5em')
    .attr('fill', '#666')
    .attr('font-size', '10px')
    .text(d => d.type)

  // 添加悬停效果
  node.on('mouseenter', function(event, d) {
    d3.select(this).select('rect')
      .transition()
      .duration(200)
      .attr('stroke-width', 3)
      .attr('filter', 'drop-shadow(0 4px 8px rgba(0,0,0,0.2))')
  })
  .on('mouseleave', function(event, d) {
    d3.select(this).select('rect')
      .transition()
      .duration(200)
      .attr('stroke-width', 2)
      .attr('filter', 'none')
  })
}

const layoutHierarchical = (nodes: CFGNode[], edges: CFGEdge[], width: number, height: number) => {
  // 简单的层次布局
  const levels: { [key: string]: number } = {}
  const visited = new Set<string>()
  
  // 找到入口节点
  const entryNode = nodes.find(n => n.type === 'entry') || nodes[0]
  if (entryNode) {
    assignLevel(entryNode.id, 0, levels, edges, visited)
  }
  
  // 按层级分组
  const levelGroups: { [level: number]: CFGNode[] } = {}
  nodes.forEach(node => {
    const level = levels[node.id] || 0
    if (!levelGroups[level]) levelGroups[level] = []
    levelGroups[level].push(node)
  })
  
  // 设置位置
  const maxLevel = Math.max(...Object.keys(levelGroups).map(Number))
  const levelHeight = height / (maxLevel + 1)
  
  Object.entries(levelGroups).forEach(([level, levelNodes]) => {
    const levelNum = Number(level)
    const nodeWidth = width / (levelNodes.length + 1)
    
    levelNodes.forEach((node, index) => {
      node.x = nodeWidth * (index + 1)
      node.y = levelHeight * (levelNum + 0.5)
    })
  })
}

const assignLevel = (nodeId: string, level: number, levels: { [key: string]: number }, edges: CFGEdge[], visited: Set<string>) => {
  if (visited.has(nodeId)) return
  visited.add(nodeId)
  levels[nodeId] = level
  
  // 找到所有子节点
  const childEdges = edges.filter(e => e.source === nodeId)
  childEdges.forEach(edge => {
    assignLevel(edge.target, level + 1, levels, edges, visited)
  })
}

const layoutForce = (nodes: CFGNode[], edges: CFGEdge[], width: number, height: number) => {
  // 停止之前的仿真
  if (simulation) {
    simulation.stop()
  }
  
  // 创建力导向仿真
  simulation = d3.forceSimulation(nodes)
    .force('link', d3.forceLink(edges).id((d: any) => d.id).distance(100))
    .force('charge', d3.forceManyBody().strength(-300))
    .force('center', d3.forceCenter(width / 2, height / 2))
    .force('collision', d3.forceCollide().radius(70))
  
  // 运行仿真直到稳定
  simulation.tick(300)
  simulation.stop()
}

const layoutCircular = (nodes: CFGNode[], width: number, height: number) => {
  const centerX = width / 2
  const centerY = height / 2
  const radius = Math.min(width, height) / 3
  
  nodes.forEach((node, index) => {
    const angle = (2 * Math.PI * index) / nodes.length
    node.x = centerX + radius * Math.cos(angle)
    node.y = centerY + radius * Math.sin(angle)
  })
}

const layoutGrid = (nodes: CFGNode[], width: number, height: number) => {
  const cols = Math.ceil(Math.sqrt(nodes.length))
  const rows = Math.ceil(nodes.length / cols)
  const cellWidth = width / cols
  const cellHeight = height / rows
  
  nodes.forEach((node, index) => {
    const col = index % cols
    const row = Math.floor(index / cols)
    node.x = cellWidth * (col + 0.5)
    node.y = cellHeight * (row + 0.5)
  })
}

const getNodeById = (nodes: CFGNode[], id: string): CFGNode | undefined => {
  return nodes.find(n => n.id === id)
}

const getNodeColor = (type: string): string => {
  const colorMap: { [key: string]: string } = {
    'entry': '#67C23A',
    'exit': '#F56C6C',
    'condition': '#E6A23C',
    'loop': '#409EFF',
    'statement': '#909399',
    'function_call': '#9C27B0',
    'return': '#FF5722'
  }
  return colorMap[type] || '#909399'
}

const getNodeTypeColor = (type: string): string => {
  const typeMap: { [key: string]: string } = {
    'entry': 'success',
    'exit': 'danger',
    'condition': 'warning',
    'loop': 'primary',
    'statement': 'info',
    'function_call': '',
    'return': 'danger'
  }
  return typeMap[type] || 'info'
}

// 事件处理
const handleLayoutChange = () => {
  if (props.graphData) {
    renderGraph(props.graphData)
  }
}

const handleZoomIn = () => {
  if (svg && zoom) {
    svg.transition().call(zoom.scaleBy, 1.5)
  }
}

const handleZoomOut = () => {
  if (svg && zoom) {
    svg.transition().call(zoom.scaleBy, 1 / 1.5)
  }
}

const handleZoomReset = () => {
  if (svg && zoom) {
    svg.transition().call(zoom.transform, d3.zoomIdentity)
  }
}

const handleFitToView = () => {
  if (!svg || !props.graphData?.nodes) return
  
  const bounds = svg.select('.graph-group').node()?.getBBox()
  if (!bounds) return
  
  const width = graphContainer.value?.clientWidth || 800
  const height = graphContainer.value?.clientHeight || 600
  
  const scale = Math.min(width / bounds.width, height / bounds.height) * 0.9
  const translateX = (width - bounds.width * scale) / 2 - bounds.x * scale
  const translateY = (height - bounds.height * scale) / 2 - bounds.y * scale
  
  svg.transition().call(
    zoom!.transform,
    d3.zoomIdentity.translate(translateX, translateY).scale(scale)
  )
}

const handleCenterGraph = () => {
  if (!svg || !props.graphData?.nodes) return
  
  const width = graphContainer.value?.clientWidth || 800
  const height = graphContainer.value?.clientHeight || 600
  
  svg.transition().call(
    zoom!.transform,
    d3.zoomIdentity.translate(width / 2, height / 2)
  )
}

const handleExport = async (format: string) => {
  if (!svg) return
  
  try {
    switch (format) {
      case 'png':
        await exportAsPNG()
        break
      case 'svg':
        await exportAsSVG()
        break
      case 'json':
        await exportAsJSON()
        break
    }
    ElMessage.success(`已导出为 ${format.toUpperCase()} 格式`)
  } catch (error) {
    console.error('导出失败:', error)
    ElMessage.error('导出失败')
  }
}

const exportAsPNG = async () => {
  // PNG导出实现
  const svgElement = svg?.node()
  if (!svgElement) return
  
  const canvas = document.createElement('canvas')
  const ctx = canvas.getContext('2d')
  if (!ctx) return
  
  const svgData = new XMLSerializer().serializeToString(svgElement)
  const img = new Image()
  
  return new Promise<void>((resolve, reject) => {
    img.onload = () => {
      canvas.width = img.width
      canvas.height = img.height
      ctx.drawImage(img, 0, 0)
      
      canvas.toBlob((blob) => {
        if (blob) {
          const url = URL.createObjectURL(blob)
          const a = document.createElement('a')
          a.href = url
          a.download = 'cfg-graph.png'
          a.click()
          URL.revokeObjectURL(url)
          resolve()
        } else {
          reject(new Error('Failed to create blob'))
        }
      })
    }
    
    img.onerror = reject
    img.src = 'data:image/svg+xml;base64,' + btoa(svgData)
  })
}

const exportAsSVG = () => {
  const svgElement = svg?.node()
  if (!svgElement) return
  
  const svgData = new XMLSerializer().serializeToString(svgElement)
  const blob = new Blob([svgData], { type: 'image/svg+xml' })
  const url = URL.createObjectURL(blob)
  
  const a = document.createElement('a')
  a.href = url
  a.download = 'cfg-graph.svg'
  a.click()
  
  URL.revokeObjectURL(url)
}

const exportAsJSON = () => {
  if (!props.graphData) return
  
  const jsonData = JSON.stringify(props.graphData, null, 2)
  const blob = new Blob([jsonData], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  
  const a = document.createElement('a')
  a.href = url
  a.download = 'cfg-data.json'
  a.click()
  
  URL.revokeObjectURL(url)
}

const toggleFullscreen = () => {
  if (!viewerContainer.value) return
  
  if (document.fullscreenElement) {
    document.exitFullscreen()
  } else {
    viewerContainer.value.requestFullscreen()
  }
}
</script>

<style scoped>
.graph-viewer {
  height: 100%;
  display: flex;
  flex-direction: column;
  background: var(--el-bg-color);
  border: 1px solid var(--el-border-color);
  border-radius: 6px;
  overflow: hidden;
}

.viewer-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: var(--el-bg-color-page);
  border-bottom: 1px solid var(--el-border-color);
}

.viewer-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 600;
  color: var(--el-text-color-primary);
}

.viewer-controls {
  display: flex;
  align-items: center;
  gap: 12px;
}

.viewer-container {
  flex: 1;
  position: relative;
  min-height: 400px;
}

.viewer-loading,
.viewer-empty {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  color: var(--el-text-color-secondary);
  text-align: center;
}

.viewer-loading .el-icon,
.viewer-empty .el-icon {
  font-size: 48px;
}

.viewer-empty h3 {
  margin: 0;
  font-size: 18px;
  color: var(--el-text-color-primary);
}

.viewer-empty p {
  margin: 0;
  font-size: 14px;
}

.graph-container {
  width: 100%;
  height: 100%;
}

.viewer-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 16px;
  background: var(--el-bg-color-page);
  border-top: 1px solid var(--el-border-color);
  font-size: 12px;
}

.graph-info {
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

.graph-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.node-details {
  padding: 16px 0;
}

.node-code {
  margin-top: 16px;
}

.node-code h4 {
  margin: 0 0 8px 0;
  font-size: 14px;
  color: var(--el-text-color-primary);
}

.node-code pre {
  background: var(--el-fill-color-light);
  padding: 12px;
  border-radius: 4px;
  font-size: 12px;
  line-height: 1.5;
  overflow-x: auto;
}

/* D3.js 图形样式 */
:deep(.node) {
  transition: all 0.2s ease;
}

:deep(.edge) {
  transition: all 0.2s ease;
}

:deep(.node:hover rect) {
  filter: drop-shadow(0 4px 8px rgba(0,0,0,0.2));
}

/* 全屏样式 */
.viewer-container:fullscreen {
  background: white;
}

.viewer-container:fullscreen .graph-container {
  background: white;
}
</style>