# Image Analyzer API Documentation v2.0

## Service Information
- **Service URL**: `https://ckpyesytwhye.sealosbja.site/`
- **Protocol**: HTTPS
- **Data Format**: JSON
- **Character Encoding**: UTF-8
- **Deployment Environment**: Sealos Cloud Platform

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
| layout | string | Yes | Analysis layout: "4-hole" or "6-hole" |
| debug | string | No | Whether to return debug image, returns image with region markers when value is "true" |

### Request Examples

#### cURL Example
```bash
# 4-hole analysis
curl -X POST https://ckpyesytwhye.sealosbja.site/api/analyze \
  -F "image=@/path/to/image.jpg" \
  -F "layout=4-hole"

# 6-hole analysis
curl -X POST https://ckpyesytwhye.sealosbja.site/api/analyze \
  -F "image=@/path/to/image.jpg" \
  -F "layout=6-hole"

# With debug image
curl -X POST https://ckpyesytwhye.sealosbja.site/api/analyze \
  -F "image=@/path/to/image.jpg" \
  -F "layout=4-hole" \
  -F "debug=true"
```

#### JavaScript (fetch) Example
```javascript
// 4-hole analysis
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

// 6-hole analysis with debug
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

#### UniApp Example
```javascript
uni.uploadFile({
  url: 'https://ckpyesytwhye.sealosbja.site/api/analyze',
  filePath: this.selectedImage,
  name: 'image',
  formData: {
    layout: this.selectedLayout, // '4-hole' or '6-hole'
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

### Success Response

#### 4-Hole Analysis Response
```json
{
  "success": true,
  "message": "Analysis completed",
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

#### 6-Hole Analysis Response
```json
{
  "success": true,
  "message": "Analysis completed",
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

### Success Response Field Description
| Field Name | Type | Description |
|------------|------|-------------|
| success | boolean | Whether request is successful, fixed value true |
| message | string | Response message |
| data | object | Analysis result data |
| data.rows | array | Array of analysis results for each row |
| data.rows[].row_name | string | Row name: "Top", "Middle" (6-hole only), "Bottom" |
| data.rows[].a | float | A value (0-1 range) |
| data.rows[].b | float | B value (0-1 range) |
| data.rows[].ratio | float | A/B ratio (calculated value) |
| data.rows[].code | string | Four-digit code (10/11/01/00) |
| data.debug_image | string | Debug image (base64 encoded, only returned when debug=true) |
| timestamp | string | Analysis completion time (ISO 8601 format) |

---

## 3. Error Response

### 1. No File Uploaded (400)
```json
{
  "success": false,
  "message": "No file uploaded",
  "error_code": "NO_FILE",
  "timestamp": "2025-09-11T01:33:02.403493Z"
}
```

### 2. No File Selected (400)
```json
{
  "success": false,
  "message": "No file selected",
  "error_code": "NO_FILE",
  "timestamp": "2025-09-11T01:33:02.403493Z"
}
```

### 3. Invalid File Format (400)
```json
{
  "success": false,
  "message": "Unsupported file format, please upload JPG or PNG files",
  "error_code": "INVALID_FILE",
  "timestamp": "2025-09-11T01:33:02.406394Z"
}
```

### 4. File Too Large (413)
```json
{
  "success": false,
  "message": "File too large, please upload files smaller than 16MB",
  "error_code": "FILE_TOO_LARGE",
  "timestamp": "2025-09-11T01:33:02.406394Z"
}
```

### 5. Invalid Layout Parameter (400)
```json
{
  "success": false,
  "message": "Invalid layout parameter, must be \"4-hole\" or \"6-hole\"",
  "error_code": "INVALID_LAYOUT",
  "timestamp": "2025-09-11T01:33:02.406394Z"
}
```

### 6. Analysis Process Failed (500)
```json
{
  "success": false,
  "message": "Analysis process failed",
  "error_code": "ANALYSIS_FAILED",
  "timestamp": "2025-09-11T01:33:02.406394Z"
}
```

**Common Causes**:
- Image does not contain valid chip structure for selected layout
- Insufficient color variation in image
- Image quality is too low or too blurry
- Wrong layout selected for the image type

### 7. Internal Server Error (500)
```json
{
  "success": false,
  "message": "Internal server error",
  "error_code": "INTERNAL_ERROR",
  "timestamp": "2025-09-11T01:33:02.406394Z"
}
```

### 8. Interface Not Found (404)
```json
{
  "success": false,
  "message": "Interface not found",
  "error_code": "NOT_FOUND",
  "timestamp": "2025-09-11T01:33:02.406394Z"
}
```

### 9. Method Not Allowed (405)
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
| INVALID_LAYOUT | 400 | Invalid layout parameter (must be "4-hole" or "6-hole") |
| ANALYSIS_FAILED | 500 | Analysis process failed |
| INTERNAL_ERROR | 500 | Internal server error |
| NOT_FOUND | 404 | Interface not found |
| METHOD_NOT_ALLOWED | 405 | Request method not allowed |

---

## 4. Frontend Integration Examples

### React Component Example
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
        alert(`Analysis failed: ${data.message}`);
      }
    } catch (error) {
      console.error('Error:', error);
      alert('Network error, please retry');
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
          4-Hole Chip
        </label>
        <label>
          <input
            type="radio"
            value="6-hole"
            checked={layout === '6-hole'}
            onChange={(e) => setLayout(e.target.value)}
          />
          6-Hole Chip
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
        Debug Mode
      </label>
      
      <button onClick={analyzeImage} disabled={!file || loading}>
        {loading ? 'Analyzing...' : 'Start Analysis'}
      </button>
      
      {result && (
        <div>
          <h3>Analysis Results</h3>
          {result.rows.map((row, index) => (
            <div key={index}>
              <h4>{row.row_name}</h4>
              <p>A Value: {row.a.toFixed(3)}</p>
              <p>B Value: {row.b.toFixed(3)}</p>
              <p>Ratio: {row.ratio.toFixed(2)}</p>
              <p>Code: {row.code}</p>
            </div>
          ))}
          
          {result.debug_image && (
            <div>
              <h4>Debug Image</h4>
              <img src={`data:image/jpeg;base64,${result.debug_image}`} alt="Debug Image" />
            </div>
          )}
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
    <div>
      <label>
        <input
          type="radio"
          value="4-hole"
          v-model="layout"
        />
        4-Hole Chip
      </label>
      <label>
        <input
          type="radio"
          value="6-hole"
          v-model="layout"
        />
        6-Hole Chip
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
      Debug Mode
    </label>
    
    <button @click="analyzeImage" :disabled="!file || loading">
      {{ loading ? 'Analyzing...' : 'Start Analysis' }}
    </button>
    
    <div v-if="result">
      <h3>Analysis Results</h3>
      <div v-for="(row, index) in result.rows" :key="index">
        <h4>{{ row.row_name }}</h4>
        <p>A Value: {{ row.a.toFixed(3) }}</p>
        <p>B Value: {{ row.b.toFixed(3) }}</p>
        <p>Ratio: {{ row.ratio.toFixed(2) }}</p>
        <p>Code: {{ row.code }}</p>
      </div>
      
      <div v-if="result.debug_image">
        <h4>Debug Image</h4>
        <img :src="`data:image/jpeg;base64,${result.debug_image}`" alt="Debug Image" />
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
          alert(`Analysis failed: ${data.message}`);
        }
      } catch (error) {
        console.error('Error:', error);
        alert('Network error, please retry');
      } finally {
        this.loading = false;
      }
    }
  }
}
</script>
```

---

## 5. Notes

### File Requirements
- **Supported formats**: JPG, JPEG, PNG
- **Maximum size**: 16MB
- **File naming**: Recommend using English and numbers, avoid special characters
- **Image content**: Must contain chip structure matching selected layout
- **Image quality**: Image should be clear with sufficient color variation and edge information

### Layout Requirements
- **4-hole layout**: Image must contain 4 circular wells arranged in 2x2 grid
- **6-hole layout**: Image must contain 6 circular wells arranged in 2x3 grid
- **Layout parameter**: Must be exactly "4-hole" or "6-hole" (case-sensitive)

### Network Requirements
- Ensure network connection is normal
- Production environment deployed on Sealos cloud platform, using HTTPS protocol
- API address: `https://ckpyesytwhye.sealosbja.site/`
- Supports cross-origin requests (CORS)

### Error Handling
- Always check the `success` field in response
- Handle errors accordingly based on `error_code`
- Provide retry mechanism for network errors
- If receiving `ANALYSIS_FAILED` error, check if image matches selected layout

### Performance Recommendations
- Perform client-side pre-check before image upload (format, size)
- Display upload progress
- Show loading state during analysis process

### Debug Image Function
- Set `debug=true` parameter to get debug image with region markers
- Debug image returned in base64 format, can be displayed directly in browser
- Debug image includes:
  - Colored circle markers for ROI regions
  - Region labels (Top, Middle, Bottom)
  - Analysis result text display
- Use debug image to verify if regions are correctly identified

---

## 6. Testing Tools

### Postman Testing
1. Create new POST request
2. URL: `https://ckpyesytwhye.sealosbja.site/api/analyze`
3. Body select `form-data`
4. Add key: `image`, type: `File`, value: select image file
5. Add key: `layout`, type: `Text`, value: `4-hole` or `6-hole`
6. Add key: `debug`, type: `Text`, value: `true` (optional)
7. Send request

### cURL Testing Commands
```bash
# Health check
curl -X GET https://ckpyesytwhye.sealosbja.site/api/health

# 4-hole image analysis
curl -X POST https://ckpyesytwhye.sealosbja.site/api/analyze \
  -F "image=@/path/to/your/image.jpg" \
  -F "layout=4-hole"

# 6-hole image analysis with debug
curl -X POST https://ckpyesytwhye.sealosbja.site/api/analyze \
  -F "image=@/path/to/your/image.jpg" \
  -F "layout=6-hole" \
  -F "debug=true"
```

---

**Document Version**: 2.0  
**Update Time**: 2025-09-11  
**Applicable Project**: Image Analyzer Backend API with 4-hole/6-hole Support