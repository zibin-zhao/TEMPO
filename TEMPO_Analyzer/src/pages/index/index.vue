<template>
  <view class="container">
    <!-- Header Section -->
    <view class="header">
      <image src="/static/hsing-logo.png" class="logo" mode="aspectFit"></image>
      <view class="title-row">
        <text class="title">TEMPO SNP Analyzer</text>
      </view>
      <text class="subtitle">Local SNP analysis</text>
    </view>

    <!-- Upload Section -->
    <view class="upload-section">
      <view class="upload-card" @click="chooseImage" v-if="!selectedImage">
        <image src="/static/icon.png" class="upload-icon" mode="aspectFit"></image>
        <text class="upload-text">Upload microfluidic chip image</text>
        <text class="upload-hint">JPG, PNG formats</text>
        <text class="upload-requirement" @click.stop="showImageRequirements">📋 Image Requirements</text>
      </view>
      
      <!-- Image Preview -->
      <view class="preview-card" v-if="selectedImage">
        <image :src="selectedImage" class="preview-image" mode="aspectFit"></image>
        <view class="preview-actions">
          <button class="action-btn secondary" @click="removeImage">Remove</button>
          <button class="action-btn primary" @click="chooseImage">Change</button>
        </view>
      </view>
    </view>

    <!-- Analysis Button -->
    <view class="analyze-section">
      <!-- Debug Mode Toggle -->
      <view class="debug-toggle">
        <view class="toggle-item" @click="toggleDebugMode">
          <view class="toggle-switch" :class="{ active: debugMode }">
            <view class="toggle-slider"></view>
          </view>
          <text class="toggle-label">Debug Mode</text>
        </view>
        <text class="debug-hint">View region markers</text>
      </view>
      
      <button 
        class="analyze-btn" 
        :class="{ disabled: !selectedImage || isAnalyzing }"
        @click="analyzeImage"
        :disabled="!selectedImage || isAnalyzing"
      >
        <text v-if="!isAnalyzing">Analyze SNP</text>
        <text v-else>Analyzing…</text>
      </button>
    </view>

    <!-- Results Display Area -->
    <view class="results-section" v-if="analysisResult">
      <view class="results-card">
        <view class="results-header">
          <text class="results-title">Analysis Results</text>
        </view>
        
         <!-- Dynamic Groups -->
         <view class="result-group" v-for="(group, index) in analysisResult.groups" :key="index">
           <text class="group-label">{{ getSNPLabel(group.group_number) }}</text>
           <view class="group-content">
             <view class="value-item">
               <text class="value-label">SNPV</text>
               <view class="progress-container">
                 <view class="progress-bar">
                   <view class="progress-fill" :style="{ width: Math.min((group.snpv / 100) * 100, 100) + '%' }"></view>
                 </view>
                 <text class="value-text">{{ group.snpv.toFixed(1) }}</text>
               </view>
             </view>
             <view class="value-item">
               <text class="value-label">WTV</text>
               <view class="progress-container">
                 <view class="progress-bar">
                   <view class="progress-fill" :style="{ width: Math.min((group.wtv / 100) * 100, 100) + '%' }"></view>
                 </view>
                 <text class="value-text">{{ group.wtv.toFixed(1) }}</text>
               </view>
             </view>
             <view class="ratio-item">
               <text class="ratio-label">SNR</text>
               <text class="ratio-value">{{ group.snr.toFixed(3) }}</text>
             </view>
             <view class="result-item">
               <text class="result-label">Result</text>
               <text class="result-value" :class="getResultClass(group.result)">{{ group.result }}</text>
             </view>
           </view>
         </view>
         
         <!-- Debug: Show raw data if no groups -->
         <view class="debug-data" v-if="!analysisResult.groups || analysisResult.groups.length === 0">
           <text class="debug-title">Debug: Raw Response Data</text>
           <text class="debug-content">{{ JSON.stringify(analysisResult, null, 2) }}</text>
         </view>
      </view>
      
      <!-- Debug Image Display -->
      <view class="debug-image-section" v-if="debugImage">
        <text class="debug-image-title">Debug View</text>
        <view class="debug-image-container">
          <image :src="debugImage" class="debug-image" mode="aspectFit"></image>
        </view>
        <text class="debug-image-hint">Region markers and analysis overlay</text>
      </view>
    </view>
    
    <!-- Hidden Canvas for Image Processing -->
    <canvas 
      canvas-id="analysisCanvas" 
      id="analysisCanvas"
      style="position: fixed; top: -9999px; left: -9999px; width: 1500px; height: 900px;"
      disable-scroll="true"
    ></canvas>
  </view>
</template>

<script>
import { analyzeImage as processImage } from '@/utils/imageProcessor'

export default {
  data() {
    return {
      selectedImage: '',
      isAnalyzing: false,
      analysisResult: null,
      debugMode: true, // Debug mode switch (default: on)
      debugImage: null // Debug image data
    }
  },
  
  methods: {
    // Select image
    chooseImage() {
      uni.chooseImage({
        count: 1,
        sizeType: ['compressed'],
        sourceType: ['album', 'camera'],
        success: (res) => {
          console.log('Image selection successful:', res)
          if (res.tempFilePaths && res.tempFilePaths.length > 0) {
            this.selectedImage = res.tempFilePaths[0]
            console.log('Image path:', this.selectedImage)
            this.analysisResult = null // Clear previous results
            this.debugImage = null // Clear debug image
          } else {
            console.error('Failed to get image path')
            uni.showToast({
              title: 'Image selection failed',
              icon: 'none'
            })
          }
        },
        fail: (err) => {
          console.error('Image selection failed:', err)
          uni.showToast({
            title: 'Image selection failed',
            icon: 'none'
          })
        }
      })
    },
    
    // Remove image
    removeImage() {
      this.selectedImage = ''
      this.analysisResult = null
      this.debugImage = null
    },
    
    // Toggle debug mode
    toggleDebugMode() {
      this.debugMode = !this.debugMode
      // Clear previous debug image when toggling debug mode
      this.debugImage = null
    },
    
    // Analyze image (local processing)
    async analyzeImage() {
      console.log('=== analyzeImage() called ===', new Date().toISOString())
      console.log('Selected image:', this.selectedImage)
      console.log('Is analyzing:', this.isAnalyzing)
      
      if (!this.selectedImage || this.isAnalyzing) {
        console.log('Early return: no image or already analyzing')
        return
      }
      
      // Validate image path
      if (this.selectedImage.includes('https/') || this.selectedImage.includes('http/')) {
        console.error('Invalid image path:', this.selectedImage)
        uni.showToast({
          title: 'Invalid image path, please reselect',
          icon: 'none'
        })
        this.removeImage()
        return
      }
      
      console.log('Starting local image analysis (6-hole):', this.selectedImage)
      this.isAnalyzing = true
      
      // Show loading
      uni.showLoading({
        title: 'Analyzing...',
        mask: true
      })
      
      try {
        console.log('Calling processImage with:', {
          imagePath: this.selectedImage,
          debugMode: this.debugMode,
          canvasId: 'analysisCanvas'
        })
        
        // Use local image processor (6-hole only)
        const result = await processImage(
          this.selectedImage, 
          this.debugMode,
          'analysisCanvas'
        )
        
        console.log('Analysis result:', result)
        
        if (!result || !result.groups) {
          throw new Error('Invalid analysis result: missing groups data')
        }
        
        // Set results
        this.analysisResult = result
        
        // Handle debug image if available
        if (result.debugImage) {
          this.debugImage = result.debugImage
        } else {
          this.debugImage = null
        }
        
        uni.hideLoading()
        uni.showToast({
          title: 'Analysis completed',
          icon: 'success',
          duration: 2000
        })
        
      } catch (error) {
        console.error('Analysis error details:', {
          error: error,
          message: error.message,
          stack: error.stack,
          imagePath: this.selectedImage,
          layout: this.selectedLayout
        })
        uni.hideLoading()
        
        // Show user-friendly error message
        let errorMessage = 'Analysis failed'
        if (error.message) {
          errorMessage = error.message
        }
        
        // Check if it's a validation error (invalid image input)
        const isValidationError = errorMessage.includes('Invalid image input') || 
                                  errorMessage.includes('does not contain') ||
                                  errorMessage.includes('too dark') ||
                                  errorMessage.includes('color variation') ||
                                  errorMessage.includes('ROI positions')
        
        if (isValidationError) {
          uni.showModal({
            title: 'Image Validation Failed',
            content: errorMessage + '\n\nPlease check:\n• Image is a 6-hole chip\n• Check browser console for detailed measurements\n• ROI positions may need adjustment',
            showCancel: true,
            cancelText: 'Reselect Image',
            confirmText: 'OK',
            success: (res) => {
              if (res.cancel) {
                this.removeImage()
              }
            }
          })
        } else {
          uni.showModal({
            title: 'Analysis Failed',
            content: errorMessage + '\n\nCheck console for details.\n\nPossible reasons:\n• Canvas API not available in this environment\n• Image format not supported\n• Processing error occurred',
            showCancel: true,
            cancelText: 'Reselect',
            confirmText: 'I understand',
            success: (res) => {
              if (res.cancel) {
                this.removeImage()
              }
            }
          })
        }
      } finally {
        this.isAnalyzing = false
      }
    },
    
    
    // Show image requirements
    showImageRequirements() {
      uni.showModal({
        title: 'Image Requirements',
         content: '📋 Please upload images that meet the following requirements:\n\n✅ Contains 6-hole chip structure\n✅ Clear image with good quality\n✅ Sufficient color variation\n✅ Clear chip edges visible\n✅ Supports JPG, PNG formats\n✅ File size less than 16MB\n\n❌ Avoid blurry, too dark or too bright images',
        showCancel: false,
        confirmText: 'I understand'
      })
    },
    
    // Get CSS class for result display
    getResultClass(result) {
      const classMap = {
        'SNP': 'result-snp',
        'WT': 'result-wt',
        'Heterozygote': 'result-heterozygote'
      }
      return classMap[result] || ''
    },
    
    // Get SNP label for group number
    getSNPLabel(groupNumber) {
      const snpMap = {
        1: 'rs199476104',
        2: 'rs1229984',
        3: 'rs671'
      }
      return snpMap[groupNumber] || `Group ${groupNumber}`
    }
  }
}
</script>

<style scoped>
.container {
  min-height: 100vh;
  background-color: #F5F5F7;
  padding: 24rpx 20rpx;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* Header Section */
.header {
  text-align: center;
  margin-bottom: 32rpx;
}

.logo {
  width: 120rpx;
  height: 120rpx;
  margin: 0 auto 16rpx;
  display: block;
}

.title-row {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12rpx;
  margin-bottom: 8rpx;
}

.title {
  font-size: 40rpx;
  font-weight: 700;
  color: #1D1D1F;
  letter-spacing: -0.3rpx;
}

.help-btn {
  width: 40rpx;
  height: 40rpx;
  background: #F2F2F7;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.help-btn:active {
  transform: scale(0.95);
  background: #E5E5EA;
}

.help-icon {
  font-size: 20rpx;
  color: #8E8E93;
}

.subtitle {
  display: block;
  font-size: 24rpx;
  color: #8E8E93;
  font-weight: 400;
  margin-bottom: 0;
}

/* Upload Section */
.upload-section {
  margin-bottom: 24rpx;
}

.upload-card {
  background: #FFFFFF;
  border-radius: 16rpx;
  padding: 48rpx 32rpx;
  text-align: center;
  box-shadow: 0 2rpx 12rpx rgba(0, 0, 0, 0.06);
  border: 2rpx dashed #D1D1D6;
  transition: all 0.3s ease;
}

.upload-card:active {
  transform: scale(0.98);
  background: #F8F8F8;
}

.upload-icon {
  width: 64rpx;
  height: 64rpx;
  margin-bottom: 16rpx;
}

.upload-text {
  display: block;
  font-size: 28rpx;
  font-weight: 600;
  color: #1D1D1F;
  margin-bottom: 8rpx;
}

.upload-hint {
  display: block;
  font-size: 22rpx;
  color: #8E8E93;
  margin-bottom: 6rpx;
}

.upload-requirement {
  display: inline-block;
  font-size: 20rpx;
  color: #007AFF;
  font-weight: 500;
  background: #F0F8FF;
  padding: 8rpx 12rpx;
  border-radius: 8rpx;
  border: 1rpx solid #E3F2FD;
  margin-top: 12rpx;
}

/* Preview Card */
.preview-card {
  background: #FFFFFF;
  border-radius: 16rpx;
  padding: 20rpx;
  box-shadow: 0 2rpx 12rpx rgba(0, 0, 0, 0.06);
}

.preview-image {
  width: 100%;
  height: 320rpx;
  border-radius: 12rpx;
  margin-bottom: 16rpx;
}

.preview-actions {
  display: flex;
  gap: 12rpx;
}

.action-btn {
  flex: 1;
  height: 72rpx;
  border-radius: 12rpx;
  border: none;
  font-size: 26rpx;
  font-weight: 600;
  transition: all 0.2s ease;
}

.action-btn.secondary {
  background: #F2F2F7;
  color: #1D1D1F;
}

.action-btn.primary {
  background: #007AFF;
  color: #FFFFFF;
}

.action-btn:active {
  transform: scale(0.95);
}

/* Analysis Button */
.analyze-section {
  margin-bottom: 24rpx;
}

/* Debug Mode Toggle */
.debug-toggle {
  background: #FFFFFF;
  border-radius: 12rpx;
  padding: 16rpx 20rpx;
  margin-bottom: 16rpx;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.04);
}

.toggle-item {
  display: flex;
  align-items: center;
  gap: 12rpx;
  margin-bottom: 6rpx;
}

.toggle-switch {
  width: 72rpx;
  height: 36rpx;
  background: #D1D1D6;
  border-radius: 18rpx;
  position: relative;
  transition: all 0.3s ease;
}

.toggle-switch.active {
  background: #007AFF;
}

.toggle-slider {
  width: 28rpx;
  height: 28rpx;
  background: #FFFFFF;
  border-radius: 50%;
  position: absolute;
  top: 4rpx;
  left: 4rpx;
  transition: all 0.3s ease;
  box-shadow: 0 2rpx 4rpx rgba(0, 0, 0, 0.2);
}

.toggle-switch.active .toggle-slider {
  left: 40rpx;
}

.toggle-label {
  font-size: 26rpx;
  font-weight: 600;
  color: #1D1D1F;
}

.debug-hint {
  font-size: 20rpx;
  color: #8E8E93;
  line-height: 1.4;
  margin-left: 84rpx;
}

.analyze-btn {
  width: 100%;
  height: 88rpx;
  background: #007AFF;
  color: #FFFFFF;
  border: none;
  border-radius: 16rpx;
  font-size: 30rpx;
  font-weight: 600;
  box-shadow: 0 4rpx 16rpx rgba(0, 122, 255, 0.25);
  transition: all 0.3s ease;
}

.analyze-btn:active:not(.disabled) {
  transform: scale(0.98);
  box-shadow: 0 2rpx 8rpx rgba(0, 122, 255, 0.25);
}

.analyze-btn.disabled {
  background: #D1D1D6;
  color: #8E8E93;
  box-shadow: none;
}

/* Results Area */
.results-section {
  margin-bottom: 24rpx;
}

.results-card {
  background: #FFFFFF;
  border-radius: 16rpx;
  padding: 24rpx;
  box-shadow: 0 2rpx 12rpx rgba(0, 0, 0, 0.06);
}

.results-header {
  margin-bottom: 20rpx;
  text-align: center;
  padding-bottom: 16rpx;
  border-bottom: 1rpx solid #E5E5EA;
}

.results-title {
  display: block;
  font-size: 30rpx;
  font-weight: 700;
  color: #1D1D1F;
  margin-bottom: 0;
}

.result-group {
  margin-bottom: 20rpx;
  padding: 18rpx;
  background: #F8F8F8;
  border-radius: 12rpx;
  border: 1rpx solid #E5E5EA;
}

.result-group:last-child {
  margin-bottom: 0;
}

.group-label {
  display: block;
  font-size: 26rpx;
  font-weight: 700;
  color: #1D1D1F;
  margin-bottom: 16rpx;
  text-align: center;
}

.group-content {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr 1fr;
  gap: 10rpx;
}

.value-item {
  display: flex;
  flex-direction: column;
  gap: 6rpx;
}

.value-label {
  font-size: 20rpx;
  font-weight: 600;
  color: #8E8E93;
  text-transform: uppercase;
  letter-spacing: 0.5rpx;
}

.progress-container {
  display: flex;
  align-items: center;
  gap: 8rpx;
}

.progress-bar {
  flex: 1;
  height: 10rpx;
  background: #F2F2F7;
  border-radius: 5rpx;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #007AFF, #5AC8FA);
  border-radius: 5rpx;
  transition: width 0.5s ease;
}

.value-text {
  font-size: 18rpx;
  font-weight: 600;
  color: #1D1D1F;
  min-width: 60rpx;
  text-align: right;
}

.ratio-item, .result-item {
  display: flex;
  flex-direction: column;
  gap: 6rpx;
  align-items: center;
  justify-content: center;
  background: #FFFFFF;
  border-radius: 10rpx;
  padding: 12rpx 8rpx;
  border: 1rpx solid #E5E5EA;
}

.ratio-label, .result-label {
  font-size: 18rpx;
  font-weight: 600;
  color: #8E8E93;
  text-transform: uppercase;
  letter-spacing: 0.5rpx;
}

.ratio-value {
  font-size: 22rpx;
  font-weight: 700;
  color: #1D1D1F;
}

.result-value {
  font-size: 20rpx;
  font-weight: 700;
  text-align: center;
  padding: 6rpx 12rpx;
  border-radius: 6rpx;
  min-width: 100rpx;
}

.result-value.result-snp {
  background: #FF3B30;
  color: #FFFFFF;
}

.result-value.result-wt {
  background: #34C759;
  color: #FFFFFF;
}

.result-value.result-heterozygote {
  background: #FF9500;
  color: #FFFFFF;
}

/* Debug Image Area */
.debug-image-section {
  margin-top: 24rpx;
  padding-top: 24rpx;
  border-top: 1rpx solid #E5E5EA;
}

.debug-image-title {
  display: block;
  font-size: 24rpx;
  font-weight: 600;
  color: #1D1D1F;
  margin-bottom: 12rpx;
  text-align: center;
}

.debug-image-container {
  background: #F8F8F8;
  border-radius: 12rpx;
  padding: 12rpx;
  margin-bottom: 8rpx;
}

.debug-image {
  width: 100%;
  max-height: 320rpx;
  border-radius: 10rpx;
}

.debug-image-hint {
  display: block;
  font-size: 18rpx;
  color: #8E8E93;
  text-align: center;
  line-height: 1.4;
}

/* Debug data display */
.debug-data {
  margin-top: 24rpx;
  padding: 18rpx;
  background: #F8F8F8;
  border-radius: 12rpx;
  border: 1rpx solid #E5E5EA;
}

.debug-title {
  display: block;
  font-size: 22rpx;
  font-weight: 600;
  color: #FF3B30;
  margin-bottom: 12rpx;
}

.debug-content {
  display: block;
  font-size: 18rpx;
  color: #1D1D1F;
  font-family: 'SF Mono', Monaco, 'Cascadia Code', monospace;
  line-height: 1.4;
  word-break: break-all;
  white-space: pre-wrap;
}
</style>
