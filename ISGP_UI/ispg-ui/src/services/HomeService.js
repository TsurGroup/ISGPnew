import axios from 'axios';

const BASE_URL = 'http://127.0.0.1:8000'; // Assuming FastAPI server runs on localhost:8000

const HomeService = {

  checkVersion: async () => {
    try {
      const response = await axios.get(`${BASE_URL}/checkVersion`);

      if (response.status === 200) {
        const { updateAvailable, currentVersion,message} = response.data;
      

        return { updateAvailable, currentVersion,message};
      } else {
        throw new Error('Version check failed');
      }
    } catch (error) {
      console.error('Error checking version:', error);
      throw new Error(error.response?.data?.error || 'Version check failed');
    }
  },
  
  login: async () => {
    try {
      const response = await axios.post(`${BASE_URL}/login`, {}, {
        withCredentials: true, // Include cookies with the request
      });

      if (response.status === 200) {
        const { user_id } = response.data;
        // sessionStorage.setItem('user_id', user_id);
        console.log('Logged in successfully, User ID:', user_id);
      } else {
        console.error('Login failed');
      }
    } catch (error) {
      console.error('Error during login:', error);
    }
  },
  createProject: async (projectName) => {
    try {
      const response = await axios.post(`${BASE_URL}/createProject?project_name=${encodeURIComponent(projectName)}`, {}, {
        withCredentials: true,
      });

      if (response.status === 200) {
        localStorage.setItem("projectName", projectName);
        return response.data;
      } else {
        throw new Error('Project creation failed');
      }
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Project creation failed');
    }
  },
  loadProject: async (projectName) => {
    try {
      const response = await axios.post(`${BASE_URL}/loadProject?project_name=${encodeURIComponent(projectName)}`, {}, {
        withCredentials: true,
      });

      if (response.status === 200) {
        return response.data;
      } else {
        throw new Error('Project load failed');
      }
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Project load failed');
    }
  },
  getProjects: async () => {
    try {
      const response = await axios.get(`${BASE_URL}/getProjects`, {
        withCredentials: true,
      });

      if (response.status === 200) {
        return response.data; // Assuming the response is a list of project names
      } else {
        throw new Error('Failed to fetch projects');
      }
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to fetch projects');
    }
  },
};

export default HomeService;
