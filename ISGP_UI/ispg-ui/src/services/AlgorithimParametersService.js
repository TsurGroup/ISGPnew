import axios from 'axios';

const BASE_URL = 'http://127.0.0.1:8000'; // Assuming FastAPI server runs on localhost:8000

const AlgorithmParametersService = {
    
  getExperimentData: async () => {
    try {
      const response = await axios.get(`${BASE_URL}/getExperimentData`, {
        withCredentials: true // Include cookies with the request
      });
      return response.data;
    } catch (error) {
      throw error; // Handle error in the component where DataSetService.uploadData is called
    }
  },

    saveAlgorithmParameters: async (data) => {
    try {
      const response = await axios.post(`${BASE_URL}/saveAlgorithmParameters`, data, {
        withCredentials: true // Include cookies with the request
      });
      return response.data;
    } catch (error) {
      throw error; // Handle error in the component where DataSetService.uploadData is called
    }
  },

  getAlgorithmParameters: async () => {
    try {
      const response = await axios.get(`${BASE_URL}/getAlgorithmParameters`, {
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

export default AlgorithmParametersService;

