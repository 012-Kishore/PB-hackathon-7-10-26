/**
 * API Service for Backend Communication with FastAPI Backend (Member 3)
 */

const getApiBaseUrl = () => {
  return import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
};

/**
 * Checks backend health by sending GET /health
 * @returns {Promise<{connected: boolean, message?: string, data?: any}>}
 */
export const checkBackendHealth = async () => {
  const baseUrl = getApiBaseUrl();
  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 4000);

    const response = await fetch(`${baseUrl}/health`, {
      method: 'GET',
      signal: controller.signal,
    });
    clearTimeout(timeoutId);

    if (response.ok) {
      const data = await response.json().catch(() => ({ status: 'online' }));
      return { connected: true, data };
    } else {
      return {
        connected: false,
        message: `Backend returned status ${response.status}`,
      };
    }
  } catch (error) {
    let message = 'Backend unavailable. Please start the backend server.';
    if (error.name === 'AbortError') {
      message = 'Backend health check timed out.';
    }
    return { connected: false, message, error: error.message };
  }
};

/**
 * Sends an image Blob to POST /predict endpoint
 * @param {Blob} imageBlob - The captured video frame image blob
 * @returns {Promise<{success: boolean, rawPrediction?: string, normalizedPrediction?: string, confidence?: number, rawConfidence?: number, error?: string}>}
 */
export const predictImage = async (imageBlob) => {
  const baseUrl = getApiBaseUrl();
  const formData = new FormData();
  formData.append('file', imageBlob, 'frame.jpg');

  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 8000);

    const response = await fetch(`${baseUrl}/predict`, {
      method: 'POST',
      body: formData,
      signal: controller.signal,
    });
    clearTimeout(timeoutId);

    if (!response.ok) {
      const errorJson = await response.json().catch(() => null);
      const errorMsg = errorJson?.message || errorJson?.detail || `Server error (${response.status})`;
      throw new Error(errorMsg);
    }

    const data = await response.json();
    
    // Normalize backend response variations (e.g. "Mask", "with_mask", "No Mask", "without_mask", 0.964)
    const rawPred = String(data.prediction || data.label || data.result || '').trim();
    const lowerPred = rawPred.toLowerCase();

    let isMask = false;
    if (
      lowerPred.includes('no') || 
      lowerPred.includes('without') || 
      lowerPred.includes('off') ||
      lowerPred === '0'
    ) {
      isMask = false;
    } else if (
      lowerPred.includes('mask') || 
      lowerPred.includes('with') || 
      lowerPred === '1'
    ) {
      isMask = true;
    } else {
      // Fallback fallback check
      isMask = !lowerPred.includes('no');
    }

    const normalizedPrediction = isMask ? 'MASK' : 'NO MASK';

    // Parse confidence numeric value
    let rawConf = data.confidence !== undefined ? data.confidence : data.score;
    let numericConf = 0;
    if (typeof rawConf === 'number') {
      numericConf = rawConf > 1 ? rawConf / 100 : rawConf;
    } else if (typeof rawConf === 'string') {
      const parsed = parseFloat(rawConf.replace('%', ''));
      numericConf = isNaN(parsed) ? 0 : (parsed > 1 ? parsed / 100 : parsed);
    }

    return {
      success: true,
      rawPrediction: rawPred,
      normalizedPrediction,
      isMask,
      confidence: numericConf, // numeric fraction e.g. 0.964
      data,
    };
  } catch (error) {
    let errorMsg = error.message || 'Failed to send prediction request';
    if (error.name === 'AbortError') {
      errorMsg = 'Prediction request timed out.';
    }
    return {
      success: false,
      error: errorMsg,
    };
  }
};
