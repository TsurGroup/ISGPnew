import axios from 'axios';

const BASE_URL = 'http://127.0.0.1:8000'; // Assuming FastAPI server runs on localhost:8000

const DataSetService = {

  SaveExperimentData: async (data) => {
    try {
      const response = await axios.post(`${BASE_URL}/SaveExperimentData`, data, {
        withCredentials: true // Include cookies with the request
      });
      return response.data;
    } catch (error) {
      throw error; // Handle error in the component where DataSetService.uploadData is called
    }
  },

  getFilteredData: async (w0,w1) => {
    try {
      const response = await axios.get(`${BASE_URL}/getFilteredData/${w0}/${w1}`, {
        withCredentials: true // Include cookies with the request
      });
      return response.data;
    } catch (error) {
      throw error; // Handle error in the component where DataSetService.uploadData is called
    }
  },

  getExampleTextFile: async () => {
    try {
      const response = await axios.get(`${BASE_URL}/getExampleTextFile`,
        { responseType: 'blob',  
          withCredentials: true
       }
        // Important to handle file download
      );
      return response.data;
    } catch (error) {
      throw error; // Handle error in the component where DataSetService.uploadData is called
    }
  },

  getExampleExcelFile: async () => {
    try {
      const response = await axios.get(`${BASE_URL}/getExampleExcelFile`,
        { responseType: 'blob',  
          withCredentials: true
       }
        // Important to handle file download
      );
      return response.data;
    } catch (error) {
      throw error; // Handle error in the component where DataSetService.uploadData is called
    }
  },



  // Add more methods for logout, check session, etc. as needed
};

export default DataSetService;

