# 图片分析API接口文档

## 服务信息
- **服务地址**: `https://ckpyesytwhye.sealosbja.site/`
- **协议**: HTTPS
- **数据格式**: JSON
- **字符编码**: UTF-8
- **部署环境**: Sealos 云平台

---

## 1. 健康检查接口

### 接口信息
- **URL**: `/api/health`
- **方法**: `GET`
- **功能**: 检查服务运行状态

### 请求示例
```bash
curl -X GET https://ckpyesytwhye.sealosbja.site/api/health
```

### 成功响应
```json
{
  "status": "healthy",
  "message": "服务运行正常",
  "timestamp": "2025-09-11T01:33:02.400929Z",
  "version": "1.0.0"
}
```

### 响应字段说明
| 字段名 | 类型 | 说明 |
|--------|------|------|
| status | string | 服务状态，固定值 "healthy" |
| message | string | 状态描述信息 |
| timestamp | string | 响应时间（ISO 8601格式） |
| version | string | API版本号 |

---

## 2. 图片分析接口

### 接口信息
- **URL**: `/api/analyze`
- **方法**: `POST`
- **Content-Type**: `multipart/form-data`
- **功能**: 上传图片进行分析并返回分析结果

### 请求参数
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| image | File | 是 | 上传的图片文件，支持JPG、PNG格式，最大16MB |
| layout | string | 是 | 分析布局："4-hole" 或 "6-hole" |
| debug | string | 否 | 是否返回调试图片，值为"true"时返回带区域标记的图片 |

### 请求示例

#### cURL 示例
```bash
# 4孔分析
curl -X POST https://ckpyesytwhye.sealosbja.site/api/analyze \
  -F "image=@/path/to/image.jpg" \
  -F "layout=4-hole"

# 6孔分析
curl -X POST https://ckpyesytwhye.sealosbja.site/api/analyze \
  -F "image=@/path/to/image.jpg" \
  -F "layout=6-hole"

# 带调试图片
curl -X POST https://ckpyesytwhye.sealosbja.site/api/analyze \
  -F "image=@/path/to/image.jpg" \
  -F "layout=4-hole" \
  -F "debug=true"
```

#### JavaScript (fetch) 示例
```javascript
// 4孔分析
const formData = new FormData();
formData.append('image', fileInput.files[0]);
formData.append('layout', '4-hole');

fetch('https://ckpyesytwhye.sealosbja.site/api/analyze', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));

// 6孔分析带调试
const formDataWithDebug = new FormData();
formDataWithDebug.append('image', fileInput.files[0]);
formDataWithDebug.append('layout', '6-hole');
formDataWithDebug.append('debug', 'true');

fetch('https://ckpyesytwhye.sealosbja.site/api/analyze', {
  method: 'POST',
  body: formDataWithDebug
})
.then(response => response.json())
.then(data => {
  console.log(data);
  if (data.data.debug_image) {
    // 显示调试图片
    const img = document.createElement('img');
    img.src = 'data:image/jpeg;base64,' + data.data.debug_image;
    document.body.appendChild(img);
  }
})
.catch(error => console.error('Error:', error));
```

#### JavaScript (axios) 示例
```javascript
const formData = new FormData();
formData.append('image', fileInput.files[0]);
formData.append('layout', '4-hole');

axios.post('https://ckpyesytwhye.sealosbja.site/api/analyze', formData, {
  headers: {
    'Content-Type': 'multipart/form-data',
  },
})
.then(response => {
  console.log(response.data);
})
.catch(error => {
  console.error('Error:', error);
});
```

#### UniApp 示例
```javascript
uni.uploadFile({
  url: 'https://ckpyesytwhye.sealosbja.site/api/analyze',
  filePath: this.selectedImage,
  name: 'image',
  formData: {
    layout: this.selectedLayout, // '4-hole' 或 '6-hole'
    debug: this.debugMode ? 'true' : undefined
  },
  success: (res) => {
    const data = JSON.parse(res.data);
    if (data.success) {
      this.analysisResult = data.data;
      if (data.data.debug_image) {
        this.debugImage = `data:image/jpeg;base64,${data.data.debug_image}`;
      }
    }
  },
  fail: (err) => {
    console.error('Upload failed:', err);
  }
});
```

### 成功响应

#### 4孔分析响应
```json
{
  "success": true,
  "message": "分析完成",
  "data": {
    "rows": [
      {
        "row_name": "Top",
        "a": 0.756,
        "b": 0.234,
        "ratio": 3.23,
        "code": "10"
      },
      {
        "row_name": "Bottom",
        "a": 0.432,
        "b": 0.568,
        "ratio": 0.76,
        "code": "01"
      }
    ],
    "debug_image": "/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAYEBQYFBAYGBQYHBwYIChAKCgkJChQODwwQFxQYGBcUFhYaHSUfGhsjHBYWICwgIyYnKSopGR8tMC0oMCUoKSj/2wBDAQcHBwoIChMKChMoGhYaKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCj/wAARCAABAAEDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAv/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFQEBAQAAAAAAAAAAAAAAAAAAAAX/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwCdABmX/9k="
  },
  "timestamp": "2025-09-11T01:33:20.261869Z"
}
```

#### 6孔分析响应
```json
{
  "success": true,
  "message": "分析完成",
  "data": {
    "rows": [
      {
        "row_name": "Top",
        "a": 0.756,
        "b": 0.234,
        "ratio": 3.23,
        "code": "10"
      },
      {
        "row_name": "Middle",
        "a": 0.543,
        "b": 0.457,
        "ratio": 1.19,
        "code": "11"
      },
      {
        "row_name": "Bottom",
        "a": 0.432,
        "b": 0.568,
        "ratio": 0.76,
        "code": "01"
      }
    ],
    "debug_image": "/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAYEBQYFBAYGBQYHBwYIChAKCgkJChQODwwQFxQYGBcUFhYaHSUfGhsjHBYWICwgIyYnKSopGR8tMC0oMCUoKSj/2wBDAQcHBwoIChMKChMoGhYaKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCj/wAARCAABAAEDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAv/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFQEBAQAAAAAAAAAAAAAAAAAAAAX/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwCdABmX/9k="
  },
  "timestamp": "2025-09-11T01:33:20.261869Z"
}
```

### 成功响应字段说明
| 字段名 | 类型 | 说明 |
|--------|------|------|
| success | boolean | 请求是否成功，固定值 true |
| message | string | 响应消息 |
| data | object | 分析结果数据 |
| data.rows | array | 每行的分析结果数组 |
| data.rows[].row_name | string | 行名称："Top"、"Middle"（仅6孔）、"Bottom" |
| data.rows[].a | float | A值（0-1范围） |
| data.rows[].b | float | B值（0-1范围） |
| data.rows[].ratio | float | A/B比值（计算值） |
| data.rows[].code | string | 四位代码（10/11/01/00） |
| data.debug_image | string | 调试图片（base64编码，仅当debug=true时返回） |
| timestamp | string | 分析完成时间（ISO 8601格式） |

---

## 3. 错误响应

### 1. 没有上传文件 (400)
```json
{
  "success": false,
  "message": "没有上传文件",
  "error_code": "NO_FILE",
  "timestamp": "2025-09-11T01:33:02.403493Z"
}
```

### 2. 没有选择文件 (400)
```json
{
  "success": false,
  "message": "没有选择文件",
  "error_code": "NO_FILE",
  "timestamp": "2025-09-11T01:33:02.403493Z"
}
```

### 3. 无效文件格式 (400)
```json
{
  "success": false,
  "message": "不支持的文件格式，请上传 JPG 或 PNG 文件",
  "error_code": "INVALID_FILE",
  "timestamp": "2025-09-11T01:33:02.406394Z"
}
```

### 4. 文件过大 (413)
```json
{
  "success": false,
  "message": "文件过大，请上传小于16MB的文件",
  "error_code": "FILE_TOO_LARGE",
  "timestamp": "2025-09-11T01:33:02.406394Z"
}
```

### 5. 无效布局参数 (400)
```json
{
  "success": false,
  "message": "无效的布局参数，必须是 \"4-hole\" 或 \"6-hole\"",
  "error_code": "INVALID_LAYOUT",
  "timestamp": "2025-09-11T01:33:02.406394Z"
}
```

### 6. 分析过程失败 (500)
```json
{
  "success": false,
  "message": "分析过程失败",
  "error_code": "ANALYSIS_FAILED",
  "timestamp": "2025-09-11T01:33:02.406394Z"
}
```

**常见原因**：
- 图片不包含所选布局的有效芯片结构
- 图片颜色变化不足
- 图片质量过低或过于模糊
- 为图片类型选择了错误的布局

### 7. 服务器内部错误 (500)
```json
{
  "success": false,
  "message": "服务器内部错误",
  "error_code": "INTERNAL_ERROR",
  "timestamp": "2025-09-11T01:33:02.406394Z"
}
```

### 8. 接口不存在 (404)
```json
{
  "success": false,
  "message": "接口不存在",
  "error_code": "NOT_FOUND",
  "timestamp": "2025-09-11T01:33:02.406394Z"
}
```

### 9. 请求方法不允许 (405)
```json
{
  "success": false,
  "message": "请求方法不允许",
  "error_code": "METHOD_NOT_ALLOWED",
  "timestamp": "2025-09-11T01:33:02.406394Z"
}
```

### 错误响应字段说明
| 字段名 | 类型 | 说明 |
|--------|------|------|
| success | boolean | 请求是否成功，固定值 false |
| message | string | 错误描述信息 |
| error_code | string | 错误代码 |
| timestamp | string | 错误发生时间（ISO 8601格式） |

### 错误代码说明
| 错误代码 | HTTP状态码 | 说明 |
|----------|------------|------|
| NO_FILE | 400 | 没有上传文件或没有选择文件 |
| INVALID_FILE | 400 | 无效文件格式 |
| FILE_TOO_LARGE | 413 | 文件过大 |
| INVALID_LAYOUT | 400 | 无效布局参数（必须是"4-hole"或"6-hole"） |
| ANALYSIS_FAILED | 500 | 分析过程失败 |
| INTERNAL_ERROR | 500 | 服务器内部错误 |
| NOT_FOUND | 404 | 接口不存在 |
| METHOD_NOT_ALLOWED | 405 | 请求方法不允许 |

---

## 4. 前端集成示例

### React 组件示例
```jsx
import React, { useState } from 'react';

const ImageAnalyzer = () => {
  const [file, setFile] = useState(null);
  const [layout, setLayout] = useState('4-hole');
  const [debugMode, setDebugMode] = useState(false);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const analyzeImage = async () => {
    if (!file) return;
    
    setLoading(true);
    const formData = new FormData();
    formData.append('image', file);
    formData.append('layout', layout);
    if (debugMode) {
      formData.append('debug', 'true');
    }

    try {
      const response = await fetch('https://ckpyesytwhye.sealosbja.site/api/analyze', {
        method: 'POST',
        body: formData
      });
      
      const data = await response.json();
      
      if (data.success) {
        setResult(data.data);
      } else {
        console.error('Analysis failed:', data.message);
        alert(`分析失败: ${data.message}`);
      }
    } catch (error) {
      console.error('Error:', error);
      alert('网络错误，请重试');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div>
        <label>
          <input
            type="radio"
            value="4-hole"
            checked={layout === '4-hole'}
            onChange={(e) => setLayout(e.target.value)}
          />
          4孔芯片
        </label>
        <label>
          <input
            type="radio"
            value="6-hole"
            checked={layout === '6-hole'}
            onChange={(e) => setLayout(e.target.value)}
          />
          6孔芯片
        </label>
      </div>
      
      <input
        type="file"
        accept="image/*"
        onChange={(e) => setFile(e.target.files[0])}
      />
      
      <label>
        <input
          type="checkbox"
          checked={debugMode}
          onChange={(e) => setDebugMode(e.target.checked)}
        />
        调试模式
      </label>
      
      <button onClick={analyzeImage} disabled={!file || loading}>
        {loading ? '分析中...' : '开始分析'}
      </button>
      
      {result && (
        <div>
          <h3>分析结果</h3>
          {result.rows.map((row, index) => (
            <div key={index}>
              <h4>{row.row_name}</h4>
              <p>A值: {row.a.toFixed(3)}</p>
              <p>B值: {row.b.toFixed(3)}</p>
              <p>比值: {row.ratio.toFixed(2)}</p>
              <p>代码: {row.code}</p>
            </div>
          ))}
          
          {result.debug_image && (
            <div>
              <h4>调试图片</h4>
              <img src={`data:image/jpeg;base64,${result.debug_image}`} alt="调试图片" />
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default ImageAnalyzer;
```

### Vue.js 组件示例
```vue
<template>
  <div>
    <div>
      <label>
        <input
          type="radio"
          value="4-hole"
          v-model="layout"
        />
        4孔芯片
      </label>
      <label>
        <input
          type="radio"
          value="6-hole"
          v-model="layout"
        />
        6孔芯片
      </label>
    </div>
    
    <input
      type="file"
      accept="image/*"
      @change="handleFileChange"
    />
    
    <label>
      <input
        type="checkbox"
        v-model="debugMode"
      />
      调试模式
    </label>
    
    <button @click="analyzeImage" :disabled="!file || loading">
      {{ loading ? '分析中...' : '开始分析' }}
    </button>
    
    <div v-if="result">
      <h3>分析结果</h3>
      <div v-for="(row, index) in result.rows" :key="index">
        <h4>{{ row.row_name }}</h4>
        <p>A值: {{ row.a.toFixed(3) }}</p>
        <p>B值: {{ row.b.toFixed(3) }}</p>
        <p>比值: {{ row.ratio.toFixed(2) }}</p>
        <p>代码: {{ row.code }}</p>
      </div>
      
      <div v-if="result.debug_image">
        <h4>调试图片</h4>
        <img :src="`data:image/jpeg;base64,${result.debug_image}`" alt="调试图片" />
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      file: null,
      layout: '4-hole',
      debugMode: false,
      result: null,
      loading: false
    }
  },
  methods: {
    handleFileChange(event) {
      this.file = event.target.files[0];
    },
    
    async analyzeImage() {
      if (!this.file) return;
      
      this.loading = true;
      const formData = new FormData();
      formData.append('image', this.file);
      formData.append('layout', this.layout);
      if (this.debugMode) {
        formData.append('debug', 'true');
      }

      try {
        const response = await fetch('https://ckpyesytwhye.sealosbja.site/api/analyze', {
          method: 'POST',
          body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
          this.result = data.data;
        } else {
          console.error('Analysis failed:', data.message);
          alert(`分析失败: ${data.message}`);
        }
      } catch (error) {
        console.error('Error:', error);
        alert('网络错误，请重试');
      } finally {
        this.loading = false;
      }
    }
  }
}
</script>
```

---

## 5. 注意事项

### 文件要求
- **支持格式**: JPG、JPEG、PNG
- **最大大小**: 16MB
- **文件命名**: 建议使用英文和数字，避免特殊字符
- **图片内容**: 必须包含与所选布局匹配的芯片结构
- **图片质量**: 图片应清晰，具有足够的颜色变化和边缘信息

### 布局要求
- **4孔布局**: 图片必须包含4个圆形孔位，排列成2x2网格
- **6孔布局**: 图片必须包含6个圆形孔位，排列成2x3网格
- **布局参数**: 必须精确为"4-hole"或"6-hole"（区分大小写）

### 网络要求
- 确保网络连接正常
- 生产环境部署在Sealos云平台，使用HTTPS协议
- API地址: `https://ckpyesytwhye.sealosbja.site/`
- 支持跨域请求（CORS）

### 错误处理
- 始终检查响应中的`success`字段
- 根据`error_code`进行相应的错误处理
- 为网络错误提供重试机制
- 如果收到`ANALYSIS_FAILED`错误，检查图片是否与所选布局匹配

### 性能建议
- 在图片上传前进行客户端预检查（格式、大小）
- 显示上传进度
- 在分析过程中显示加载状态

### 调试图片功能
- 设置`debug=true`参数可获取带区域标记的调试图片
- 调试图片以base64格式返回，可直接在浏览器中显示
- 调试图片包括：
  - ROI区域的彩色圆圈标记
  - 区域标签（Top、Middle、Bottom）
  - 分析结果文本显示
- 使用调试图片验证区域是否正确识别

---

## 6. 测试工具

### Postman 测试
1. 创建新的POST请求
2. URL: `https://ckpyesytwhye.sealosbja.site/api/analyze`
3. Body选择`form-data`
4. 添加键: `image`，类型: `File`，值: 选择图片文件
5. 添加键: `layout`，类型: `Text`，值: `4-hole`或`6-hole`
6. 添加键: `debug`，类型: `Text`，值: `true`（可选）
7. 发送请求

### cURL 测试命令
```bash
# 健康检查
curl -X GET https://ckpyesytwhye.sealosbja.site/api/health

# 4孔图片分析
curl -X POST https://ckpyesytwhye.sealosbja.site/api/analyze \
  -F "image=@/path/to/your/image.jpg" \
  -F "layout=4-hole"

# 6孔图片分析带调试
curl -X POST https://ckpyesytwhye.sealosbja.site/api/analyze \
  -F "image=@/path/to/your/image.jpg" \
  -F "layout=6-hole" \
  -F "debug=true"
```

---

**文档版本**: 2.0  
**更新时间**: 2025-09-11  
**适用项目**: 图片分析后端API，支持4孔/6孔芯片分析
