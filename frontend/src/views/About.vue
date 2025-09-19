<template>
  <div class="about-page">
    <div class="about-container">
      <!-- 头部介绍 -->
      <div class="about-header">
        <div class="logo-section">
          <el-icon class="app-logo"><Share /></el-icon>
          <h1>CFG Assistant</h1>
          <p class="version">v1.0.0</p>
        </div>
        
        <div class="description">
          <h2>智能控制流图生成工具</h2>
          <p>
            CFG Assistant 是一个基于大语言模型的智能控制流图生成工具，
            支持多种编程语言的代码分析和可视化展示。
          </p>
        </div>
      </div>

      <!-- 功能特性 -->
      <div class="features-section">
        <h3>
          <el-icon><Star /></el-icon>
          主要特性
        </h3>
        
        <div class="features-grid">
          <div class="feature-card">
            <el-icon class="feature-icon"><Cpu /></el-icon>
            <h4>智能分析</h4>
            <p>基于GPT-4等大语言模型，智能分析代码结构和控制流</p>
          </div>
          
          <div class="feature-card">
            <el-icon class="feature-icon"><Document /></el-icon>
            <h4>多语言支持</h4>
            <p>支持Python、Java、JavaScript、C++等多种主流编程语言</p>
          </div>
          
          <div class="feature-card">
            <el-icon class="feature-icon"><Share /></el-icon>
            <h4>可视化展示</h4>
            <p>基于D3.js的交互式图形展示，支持多种布局和导出格式</p>
          </div>
          
          <div class="feature-card">
            <el-icon class="feature-icon"><Setting /></el-icon>
            <h4>灵活配置</h4>
            <p>支持多种模型配置，可自定义API密钥和参数设置</p>
          </div>
          
          <div class="feature-card">
            <el-icon class="feature-icon"><Monitor /></el-icon>
            <h4>实时编辑</h4>
            <p>集成Monaco Editor，提供专业的代码编辑体验</p>
          </div>
          
          <div class="feature-card">
            <el-icon class="feature-icon"><Download /></el-icon>
            <h4>导出功能</h4>
            <p>支持PNG、SVG、JSON等多种格式的图形导出</p>
          </div>
        </div>
      </div>

      <!-- 技术栈 -->
      <div class="tech-section">
        <h3>
          <el-icon><Tools /></el-icon>
          技术栈
        </h3>
        
        <div class="tech-grid">
          <div class="tech-category">
            <h4>前端技术</h4>
            <div class="tech-tags">
              <el-tag>Vue 3</el-tag>
              <el-tag>TypeScript</el-tag>
              <el-tag>Element Plus</el-tag>
              <el-tag>D3.js</el-tag>
              <el-tag>Monaco Editor</el-tag>
              <el-tag>Vite</el-tag>
            </div>
          </div>
          
          <div class="tech-category">
            <h4>后端技术</h4>
            <div class="tech-tags">
              <el-tag type="success">FastAPI</el-tag>
              <el-tag type="success">Python</el-tag>
              <el-tag type="success">Pydantic</el-tag>
              <el-tag type="success">Uvicorn</el-tag>
            </div>
          </div>
          
          <div class="tech-category">
            <h4>AI模型</h4>
            <div class="tech-tags">
              <el-tag type="warning">GPT-4</el-tag>
              <el-tag type="warning">GPT-3.5</el-tag>
              <el-tag type="warning">DeepSeek</el-tag>
              <el-tag type="warning">OpenAI API</el-tag>
            </div>
          </div>
        </div>
      </div>

      <!-- 使用指南 -->
      <div class="guide-section">
        <h3>
          <el-icon><Guide /></el-icon>
          使用指南
        </h3>
        
        <div class="guide-steps">
          <div class="step-item">
            <div class="step-number">1</div>
            <div class="step-content">
              <h4>配置模型</h4>
              <p>在左侧配置面板中选择AI模型并输入API密钥</p>
            </div>
          </div>
          
          <div class="step-item">
            <div class="step-number">2</div>
            <div class="step-content">
              <h4>输入代码</h4>
              <p>在代码编辑器中输入或粘贴需要分析的代码</p>
            </div>
          </div>
          
          <div class="step-item">
            <div class="step-number">3</div>
            <div class="step-content">
              <h4>生成CFG</h4>
              <p>点击"生成CFG"按钮，等待AI分析并生成控制流图</p>
            </div>
          </div>
          
          <div class="step-item">
            <div class="step-number">4</div>
            <div class="step-content">
              <h4>查看结果</h4>
              <p>在右侧图形展示区查看生成的控制流图，支持缩放和导出</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 联系信息 -->
      <div class="contact-section">
        <h3>
          <el-icon><Message /></el-icon>
          联系我们
        </h3>
        
        <div class="contact-info">
          <div class="contact-item">
            <el-icon><User /></el-icon>
            <span>开发者：CFG Assistant Team</span>
          </div>
          
          <div class="contact-item">
            <el-icon><Message /></el-icon>
            <span>邮箱：support@cfg-assistant.com</span>
          </div>
          
          <div class="contact-item">
            <el-icon><Link /></el-icon>
            <span>GitHub：github.com/cfg-assistant</span>
          </div>
        </div>
      </div>

      <!-- 版权信息 -->
      <div class="footer-section">
        <div class="copyright">
          <p>&copy; 2024 CFG Assistant. All rights reserved.</p>
          <p>基于MIT许可证开源</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {
  Share,
  Star,
  Cpu,
  Document,
  Setting,
  Monitor,
  Download,
  Tools,
  Guide,
  Message,
  User,
  Link
} from '@element-plus/icons-vue'
</script>

<style scoped>
.about-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 40px 20px;
}

.about-container {
  max-width: 1200px;
  margin: 0 auto;
  background: var(--el-bg-color);
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

/* 头部介绍 */
.about-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 60px 40px;
  text-align: center;
}

.logo-section {
  margin-bottom: 40px;
}

.app-logo {
  font-size: 64px;
  margin-bottom: 16px;
  display: block;
}

.about-header h1 {
  font-size: 48px;
  margin: 0 0 8px 0;
  font-weight: 700;
}

.version {
  font-size: 16px;
  opacity: 0.8;
  margin: 0;
}

.description h2 {
  font-size: 24px;
  margin: 0 0 16px 0;
  font-weight: 600;
}

.description p {
  font-size: 18px;
  line-height: 1.6;
  opacity: 0.9;
  max-width: 600px;
  margin: 0 auto;
}

/* 功能特性 */
.features-section {
  padding: 60px 40px;
}

.features-section h3 {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 28px;
  margin: 0 0 40px 0;
  color: var(--el-text-color-primary);
  justify-content: center;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px;
}

.feature-card {
  background: var(--el-bg-color-page);
  padding: 32px 24px;
  border-radius: 12px;
  text-align: center;
  border: 1px solid var(--el-border-color-lighter);
  transition: all 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.feature-icon {
  font-size: 48px;
  color: var(--el-color-primary);
  margin-bottom: 16px;
  display: block;
}

.feature-card h4 {
  font-size: 20px;
  margin: 0 0 12px 0;
  color: var(--el-text-color-primary);
}

.feature-card p {
  font-size: 14px;
  line-height: 1.6;
  color: var(--el-text-color-regular);
  margin: 0;
}

/* 技术栈 */
.tech-section {
  padding: 60px 40px;
  background: var(--el-bg-color-page);
}

.tech-section h3 {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 28px;
  margin: 0 0 40px 0;
  color: var(--el-text-color-primary);
  justify-content: center;
}

.tech-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 32px;
}

.tech-category h4 {
  font-size: 18px;
  margin: 0 0 16px 0;
  color: var(--el-text-color-primary);
}

.tech-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

/* 使用指南 */
.guide-section {
  padding: 60px 40px;
}

.guide-section h3 {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 28px;
  margin: 0 0 40px 0;
  color: var(--el-text-color-primary);
  justify-content: center;
}

.guide-steps {
  max-width: 800px;
  margin: 0 auto;
}

.step-item {
  display: flex;
  align-items: flex-start;
  gap: 24px;
  margin-bottom: 32px;
}

.step-item:last-child {
  margin-bottom: 0;
}

.step-number {
  width: 48px;
  height: 48px;
  background: var(--el-color-primary);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  font-weight: bold;
  flex-shrink: 0;
}

.step-content h4 {
  font-size: 18px;
  margin: 0 0 8px 0;
  color: var(--el-text-color-primary);
}

.step-content p {
  font-size: 14px;
  line-height: 1.6;
  color: var(--el-text-color-regular);
  margin: 0;
}

/* 联系信息 */
.contact-section {
  padding: 60px 40px;
  background: var(--el-bg-color-page);
}

.contact-section h3 {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 28px;
  margin: 0 0 40px 0;
  color: var(--el-text-color-primary);
  justify-content: center;
}

.contact-info {
  max-width: 600px;
  margin: 0 auto;
}

.contact-item {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
  font-size: 16px;
  color: var(--el-text-color-regular);
}

.contact-item .el-icon {
  color: var(--el-color-primary);
}

/* 版权信息 */
.footer-section {
  padding: 40px;
  text-align: center;
  border-top: 1px solid var(--el-border-color-lighter);
}

.copyright p {
  margin: 0 0 8px 0;
  color: var(--el-text-color-secondary);
  font-size: 14px;
}

.copyright p:last-child {
  margin-bottom: 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .about-page {
    padding: 20px 10px;
  }
  
  .about-header {
    padding: 40px 20px;
  }
  
  .about-header h1 {
    font-size: 36px;
  }
  
  .description h2 {
    font-size: 20px;
  }
  
  .description p {
    font-size: 16px;
  }
  
  .features-section,
  .tech-section,
  .guide-section,
  .contact-section {
    padding: 40px 20px;
  }
  
  .features-grid,
  .tech-grid {
    grid-template-columns: 1fr;
  }
  
  .step-item {
    flex-direction: column;
    text-align: center;
  }
}
</style>