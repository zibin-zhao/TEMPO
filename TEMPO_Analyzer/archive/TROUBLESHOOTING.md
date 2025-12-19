# Troubleshooting: "Local processing coming soon" Issue

## Issue
When clicking "Analyze", you see "Local processing coming soon" instead of actual analysis.

## Solutions

### 1. Restart Dev Server
The code has been updated. You need to restart:

```bash
# Stop current server (Ctrl+C)
cd HsingApp
npm run dev:h5
# Or for Android:
npm run dev:app-plus
```

### 2. Clear Browser Cache
If using H5 preview:
- Hard refresh: `Cmd+Shift+R` (Mac) or `Ctrl+Shift+R` (Windows)
- Or clear browser cache

### 3. Check Console for Errors
Open browser DevTools (F12) and check:
- Console tab for error messages
- Network tab for failed requests
- Look for messages starting with "Analysis error" or "Failed to"

### 4. Canvas API Limitation
**Important**: UniApp's canvas API (`uni.createCanvasContext`) works differently in:
- **H5 (browser)**: Limited support, may not work
- **App-plus (Android/iOS)**: Full support

**If testing in H5 preview:**
- The canvas API might fail silently
- You'll see errors in console
- **Solution**: Test on Android emulator/device instead

### 5. Check Image Path
The image path format matters:
- ✅ Valid: `/tmp/xxx.jpg` (temp file from `uni.chooseImage`)
- ❌ Invalid: `http://` or `https://` paths

### 6. Verify Files Are Updated
Check that these files exist and are updated:
- ✅ `src/utils/imageProcessor.js` exists
- ✅ `src/pages/index/index.vue` has import statement
- ✅ Canvas element is in template

## Expected Behavior After Fix

1. Click "Analyze" button
2. See "Analyzing..." loading indicator
3. Processing happens (1-5 seconds)
4. Results appear with:
   - Row names (Top, Bottom)
   - A and B values
   - Ratio
   - Code (10/01/11/00)
   - Genotype

## Common Errors

### Error: "Failed to get canvas image data"
**Cause**: Canvas API not available or canvas not found
**Solution**: 
- Ensure canvas element is in template
- Test on Android device/emulator (not H5)
- Check canvas ID matches

### Error: "Failed to load image"
**Cause**: Image path invalid or image not accessible
**Solution**:
- Use `uni.chooseImage` to select image
- Don't use network URLs
- Check image format (JPG/PNG)

### Error: "Analysis failed: Unknown error"
**Cause**: Generic error in processing
**Solution**:
- Check console for detailed error
- Verify image has chip structure
- Try with different image

## Testing Checklist

- [ ] Dev server restarted
- [ ] Browser cache cleared (if H5)
- [ ] Console checked for errors
- [ ] Image selected successfully
- [ ] Canvas element in template
- [ ] Testing on Android (not just H5)

## Next Steps

If still not working:
1. Share console error messages
2. Share which platform you're testing on (H5/Android)
3. Check if `src/utils/imageProcessor.js` file exists
4. Verify import statement in `index.vue`

