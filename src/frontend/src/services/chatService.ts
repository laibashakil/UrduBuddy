// Define the API base URL
const API_BASE_URL = 'http://localhost:5000';

export const chatAboutStory = async (storyId: string, message: string) => {
  try {
    // Use the full URL for the Flask server
    const response = await fetch(`${API_BASE_URL}/api/stories/${storyId}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message }),
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    
    if (!data.success) {
      throw new Error(data.error || 'Failed to get response from server');
    }
    
    if (!data.response) {
      throw new Error('No response received from server');
    }
    
    return data.response;
  } catch (error) {
    console.error('Error in chatAboutStory:', error);
    throw new Error('Failed to get response. Please try again.');
  }
}; 