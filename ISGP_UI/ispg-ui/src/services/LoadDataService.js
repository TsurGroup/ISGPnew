import axios from 'axios';

const BASE_URL = 'http://127.0.0.1:8000'; // Assuming FastAPI server runs on localhost:8000

const LoadDataService = {

  getRunNum: async () => {
    try {
      const response = await axios.get(`${BASE_URL}/getRunNum`,{
        withCredentials: true // Include cookies with the request
      });
      return response.data;
    } catch (error) {
      throw error; // Handle error in the component where DataSetService.uploadData is called
    }
  },

  getRunsGenerationNum: async (runNum) => {
    try {
      const response = await axios.get(`${BASE_URL}/getRunsGenerationNum/${runNum}`,{
        withCredentials: true // Include cookies with the request
      });
      return response.data;
    } catch (error) {
      throw error; // Handle error in the component where DataSetService.uploadData is called
    }
  },

    getGenerationModels: async (runNum,generationNum) => {
    try {
      const response = await axios.get(`${BASE_URL}/getGenerationModels/${runNum}/${generationNum}`,{
        withCredentials: true // Include cookies with the request
      });
      return response.data;
    } catch (error) {
      throw error; // Handle error in the component where DataSetService.uploadData is called
    }
  },

  getModel: async (genomeId) => {
    try {
      const response = await axios.get(`${BASE_URL}/getModel/${genomeId}`,{
        withCredentials: true // Include cookies with the request
      });
      return response.data;
    } catch (error) {
      throw error; // Handle error in the component where DataSetService.uploadData is called
    }
  },
};

export default LoadDataService;
