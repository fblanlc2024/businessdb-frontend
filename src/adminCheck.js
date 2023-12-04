// adminCheck.js
import axios from 'axios';

export async function checkAdminStatus() {
  try {
    const response = await axios.get('https://localhost:5000/admin_status_check', { withCredentials: true });
    return response.data.isAdmin;
  } catch (error) {
    console.error('Error checking admin status:', error);
    return false;
  }
}