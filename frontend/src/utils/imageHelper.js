/**
 * Converts a relative image path to a full URL
 * @param {string} imagePath - The image path from the API (e.g., '/media/product_images/file.jpg')
 * @returns {string} - Full image URL
 */
export const getImageUrl = (imagePath) => {
  if (!imagePath) {
    return '/media/product_images/default-product.svg';
  }

  // Check if it's already a full URL
  if (imagePath.startsWith('http://') || imagePath.startsWith('https://')) {
    return imagePath;
  }

  // Check if it's a blob URL (from local file preview)
  if (imagePath.startsWith('blob:')) {
    return imagePath;
  }

  // If it's a relative path, prepend the backend base URL
  // derive backend origin from API base if available, else fall back to hardcoded value
  const envUrl = import.meta.env.VITE_API_URL || '';
  // strip trailing "/api" if present
  let origin = envUrl.replace(/\/api\/?$/, '');
  if (!origin) {
    origin = "https://vunjabei-clothing-system.onrender.com";
  }
  return `${origin}${imagePath}`;
};
