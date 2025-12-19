# Image Analyzer API Documentation

## Service Information
- **Service URL**: `https://ckpyesytwhye.sealosbja.site/`
- **Protocol**: HTTPS
- **Data Format**: JSON
- **Character Encoding**: UTF-8
- **Deployment Environment**: Sealos Cloud Platform

## Quick Start

### Test Service Status
```bash
curl -X GET https://ckpyesytwhye.sealosbja.site/api/health
```

### Upload Image for Analysis
```bash
curl -X POST https://ckpyesytwhye.sealosbja.site/api/analyze \
  -F "image=@/path/to/your/image.jpg"
```

---

## 1. Health Check Interface

### Interface Information
- **URL**: `/api/health`
- **Method**: `GET`
- **Function**: Check service running status

### Request Example
```bash
curl -X GET https://ckpyesytwhye.sealosbja.site/api/health
```

### Success Response
```json
{
  "status": "healthy",
  "message": "Service running normally",
  "timestamp": "2025-09-11T01:33:02.400929Z",
  "version": "1.0.0"
}
```

### Response Field Description
| Field Name | Type | Description |
|------------|------|-------------|
| status | string | Service status, fixed value "healthy" |
| message | string | Status description information |
| timestamp | string | Response time (ISO 8601 format) |
| version | string | API version number |

---

## 2. Image Analysis Interface

### Interface Information
- **URL**: `/api/analyze`
- **Method**: `POST`
- **Content-Type**: `multipart/form-data`
- **Function**: Upload image for analysis and return analysis results

### Request Parameters
| Parameter Name | Type | Required | Description |
|----------------|------|----------|-------------|
| image | File | Yes | Uploaded image file, supports JPG, PNG formats, maximum 16MB |
| debug | string | No | Whether to return debug image, returns image with four-hole region markers when value is "true" |

### Request Examples

#### cURL Example
```bash
# Normal analysis
curl -X POST https://ckpyesytwhye.sealosbja.site/api/analyze \
  -F "image=@/path/to/image.jpg"

# Analysis with debug image
curl -X POST https://ckpyesytwhye.sealosbja.site/api/analyze \
  -F "image=@/path/to/image.jpg" \
  -F "debug=true"
```

#### JavaScript (fetch) Example
```javascript
// Normal analysis
const formData = new FormData();
formData.append('image', fileInput.files[0]);

fetch('https://ckpyesytwhye.sealosbja.site/api/analyze', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));

// Analysis with debug image
const formDataWithDebug = new FormData();
formDataWithDebug.append('image', fileInput.files[0]);
formDataWithDebug.append('debug', 'true');

fetch('https://ckpyesytwhye.sealosbja.site/api/analyze', {
  method: 'POST',
  body: formDataWithDebug
})
.then(response => response.json())
.then(data => {
  console.log(data);
  if (data.data.debug_image) {
    // Display debug image
    const img = document.createElement('img');
    img.src = 'data:image/jpeg;base64,' + data.data.debug_image;
    document.body.appendChild(img);
  }
})
.catch(error => console.error('Error:', error));
```

#### JavaScript (axios) Example
```javascript
const formData = new FormData();
formData.append('image', fileInput.files[0]);

axios.post('https://ckpyesytwhye.sealosbja.site/api/analyze', formData, {
  headers: {
    'Content-Type': 'multipart/form-data'
  }
})
.then(response => {
  console.log(response.data);
})
.catch(error => {
  console.error('Error:', error);
});
```

#### UniApp Example
```javascript
uni.uploadFile({
  url: 'https://ckpyesytwhye.sealosbja.site/api/analyze',
  filePath: this.selectedImage,
  name: 'image',
  success: (res) => {
    try {
      const data = JSON.parse(res.data);
      if (data.success) {
        this.analysisResult = data.data;
        uni.showToast({
          title: '分析完成',
          icon: 'success'
        });
      } else {
        uni.showToast({
          title: data.message || '分析失败',
          icon: 'none'
        });
      }
    } catch (e) {
      uni.showToast({
        title: '数据解析失败',
        icon: 'none'
      });
    }
  },
  fail: (err) => {
    console.error('上传失败:', err);
    uni.showToast({
      title: '网络错误',
      icon: 'none'
    });
  }
});
```

### Success Response

#### Normal Analysis Response
```json
{
  "success": true,
  "message": "Analysis completed",
  "data": {
    "row1": {
      "a": 0.756,
      "b": 0.234,
      "code": "10"
    },
    "row2": {
      "a": 0.432,
      "b": 0.568,
      "code": "01"
    }
  },
  "timestamp": "2025-09-11T01:33:20.261869Z"
}
```

#### Response with Debug Image
```json
{
  "success": true,
  "message": "Analysis completed",
  "data": {
    "row1": {
      "a": 0.756,
      "b": 0.234,
      "code": "10"
    },
    "row2": {
      "a": 0.432,
      "b": 0.568,
      "code": "01"
    },
    "debug_image": "/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAYEBQYFBAYGBQYHBwYIChAKCgkJChQODwwQFxQYGBcUFhYaHSUfGhsjHBYWICwgIyYnKSopGR8tMC0oMCUoKSj/2wBDAQcHBwoIChMKChMoGhYaKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCj/wAARCAABAAEDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAv/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFQEBAQAAAAAAAAAAAAAAAAAAAAX/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwCdABmX/9k="
  },
  "timestamp": "2025-09-11T01:33:20.261869Z"
}
```

### Success Response Field Description
| Field Name | Type | Description |
|------------|------|-------------|
| success | boolean | Whether request is successful, fixed value true |
| message | string | Response message |
| data | object | Analysis result data |
| data.row1 | object | First row analysis result |
| data.row1.a | float | A value (0-1 range) |
| data.row1.b | float | B value (0-1 range) |
| data.row1.code | string | Four-digit code (10/11/01/00) |
| data.row2 | object | Second row analysis result |
| data.row2.a | float | A value (0-1 range) |
| data.row2.b | float | B value (0-1 range) |
| data.row2.code | string | Four-digit code (10/11/01/00) |
| data.debug_image | string | Debug image (base64 encoded, only returned when debug=true) |
| timestamp | string | Analysis completion time (ISO 8601 format) |

### Error Response

#### 1. No File Uploaded (400)
```json
{
  "success": false,
  "message": "No file uploaded",
  "error_code": "NO_FILE",
  "timestamp": "2025-09-11T01:33:02.403493Z"
}
```

#### 2. No File Selected (400)
```json
{
  "success": false,
  "message": "No file selected",
  "error_code": "NO_FILE",
  "timestamp": "2025-09-11T01:33:02.403493Z"
}
```

#### 3. Invalid File Format (400)
```json
{
  "success": false,
  "message": "Unsupported file format, please upload JPG or PNG files",
  "error_code": "INVALID_FILE",
  "timestamp": "2025-09-11T01:33:02.406394Z"
}
```

#### 4. File Too Large (413)
```json
{
  "success": false,
  "message": "File too large, please upload files smaller than 16MB",
  "error_code": "FILE_TOO_LARGE",
  "timestamp": "2025-09-11T01:33:02.406394Z"
}
```

#### 5. Analysis Process Failed (500)
```json
{
  "success": false,
  "message": "Analysis process failed",
  "error_code": "ANALYSIS_FAILED",
  "timestamp": "2025-09-11T01:33:02.406394Z"
}
```

**Common Causes**:
- Image does not contain valid four-hole chip structure
- Insufficient color variation in image
- Image quality is too low or too blurry

#### 6. Internal Server Error (500)
```json
{
  "success": false,
  "message": "Internal server error",
  "error_code": "INTERNAL_ERROR",
  "timestamp": "2025-09-11T01:33:02.406394Z"
}
```

#### 7. Interface Not Found (404)
```json
{
  "success": false,
  "message": "Interface not found",
  "error_code": "NOT_FOUND",
  "timestamp": "2025-09-11T01:33:02.406394Z"
}
```

#### 8. Method Not Allowed (405)
```json
{
  "success": false,
  "message": "Request method not allowed",
  "error_code": "METHOD_NOT_ALLOWED",
  "timestamp": "2025-09-11T01:33:02.406394Z"
}
```

### Error Response Field Description
| Field Name | Type | Description |
|------------|------|-------------|
| success | boolean | Whether request is successful, fixed value false |
| message | string | Error description information |
| error_code | string | Error code |
| timestamp | string | Error occurrence time (ISO 8601 format) |

### Error Code Description
| Error Code | HTTP Status Code | Description |
|------------|------------------|-------------|
| NO_FILE | 400 | No file uploaded or no file selected |
| INVALID_FILE | 400 | Invalid file format |
| FILE_TOO_LARGE | 413 | File too large |
| ANALYSIS_FAILED | 500 | Analysis process failed |
| INTERNAL_ERROR | 500 | Internal server error |
| NOT_FOUND | 404 | Interface not found |
| METHOD_NOT_ALLOWED | 405 | Request method not allowed |

---

## 3. Frontend Integration Examples

### React Component Example
```jsx
import React, { useState } from 'react';

const ImageAnalyzer = () => {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setResult(null);
    setError(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return;

    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('image', file);

    try {
      const response = await fetch('https://ckpyesytwhye.sealosbja.site/api/analyze', {
        method: 'POST',
        body: formData
      });

      const data = await response.json();

      if (data.success) {
        setResult(data.data);
      } else {
        setError(data.message);
      }
    } catch (err) {
      setError('网络错误，请重试');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input
          type="file"
          accept="image/jpeg,image/png"
          onChange={handleFileChange}
        />
        <button type="submit" disabled={!file || loading}>
          {loading ? '分析中...' : '开始分析'}
        </button>
      </form>

      {error && <div style={{color: 'red'}}>错误: {error}</div>}
      
      {result && (
        <div>
          <h3>分析结果:</h3>
          <p>第一行: A={result.row1.a}, B={result.row1.b}, 代码={result.row1.code}</p>
          <p>第二行: A={result.row2.a}, B={result.row2.b}, 代码={result.row2.code}</p>
        </div>
      )}
    </div>
  );
};

export default ImageAnalyzer;
```

### Vue.js Component Example
```vue
<template>
  <div>
    <form @submit.prevent="analyzeImage">
      <input
        type="file"
        accept="image/jpeg,image/png"
        @change="handleFileChange"
        ref="fileInput"
      />
      <button type="submit" :disabled="!selectedFile || loading">
        {{ loading ? '分析中...' : '开始分析' }}
      </button>
    </form>

    <div v-if="error" style="color: red;">
      错误: {{ error }}
    </div>
    
    <div v-if="result">
      <h3>分析结果:</h3>
      <p>第一行: A={{ result.row1.a }}, B={{ result.row1.b }}, 代码={{ result.row1.code }}</p>
      <p>第二行: A={{ result.row2.a }}, B={{ result.row2.b }}, 代码={{ result.row2.code }}</p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      selectedFile: null,
      result: null,
      loading: false,
      error: null
    };
  },
  methods: {
    handleFileChange(event) {
      this.selectedFile = event.target.files[0];
      this.result = null;
      this.error = null;
    },
    async analyzeImage() {
      if (!this.selectedFile) return;

      this.loading = true;
      this.error = null;

      const formData = new FormData();
      formData.append('image', this.selectedFile);

      try {
        const response = await fetch('https://ckpyesytwhye.sealosbja.site/api/analyze', {
          method: 'POST',
          body: formData
        });

        const data = await response.json();

        if (data.success) {
          this.result = data.data;
        } else {
          this.error = data.message;
        }
      } catch (err) {
        this.error = '网络错误，请重试';
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>
```

---

## 4. Notes

### File Requirements
- **Supported formats**: JPG, JPEG, PNG
- **Maximum size**: 16MB
- **File naming**: Recommend using English and numbers, avoid special characters
- **Image content**: Must contain four-hole chip structure
- **Image quality**: Image should be clear with sufficient color variation and edge information

### Network Requirements
- Ensure network connection is normal
- Production environment deployed on Sealos cloud platform, using HTTPS protocol
- API address: `https://ckpyesytwhye.sealosbja.site/`
- Supports cross-origin requests (CORS)

### Error Handling
- Always check the `success` field in response
- Handle errors accordingly based on `error_code`
- Provide retry mechanism for network errors
- If receiving `ANALYSIS_FAILED` error, check if image is a valid four-hole chip image

### Performance Recommendations
- Perform client-side pre-check before image upload (format, size)
- Display upload progress
- Show loading state during analysis process

### Debug Image Function
- Set `debug=true` parameter to get debug image with four-hole region markers
- Debug image returned in base64 format, can be displayed directly in browser
- Debug image includes:
  - Colored circle markers for four ROI regions
  - Region labels (Upper Left, Upper Right, Lower Left, Lower Right)
  - Analysis result text display
- Use debug image to verify if four-hole regions are correctly identified

---

## 5. Testing Tools

### Postman Testing
1. Create new POST request
2. URL: `https://ckpyesytwhye.sealosbja.site/api/analyze`
3. Body select `form-data`
4. Add key: `image`, type: `File`, value: select image file
5. Send request

### cURL Testing Commands
```bash
# Health check
curl -X GET https://ckpyesytwhye.sealosbja.site/api/health

# Image analysis
curl -X POST https://ckpyesytwhye.sealosbja.site/api/analyze \
  -F "image=@/path/to/your/image.jpg"
```

---

**Document Version**: 1.0  
**Update Time**: 2025-09-11  
**Applicable Project**: Image Analyzer Backend API
