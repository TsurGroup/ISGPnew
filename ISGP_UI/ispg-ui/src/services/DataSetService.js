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

  getFilter: async (w0,w1) => {
    try {
      const response = await axios.get(`${BASE_URL}/getFilter/${w0}/${w1}`, {
        withCredentials: true // Include cookies with the request
      });
      return response.data;
    } catch (error) {
      throw error; // Handle error in the component where DataSetService.uploadData is called
    }
  },

  setFilter: async (data) => {
    try {
      const response = await axios.post(`${BASE_URL}/setFilter`, data, {
        withCredentials: true
      });
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  

  getExampleTextFile: async () => {
    try {
      const response = await axios.get(`${BASE_URL}/getExampleTextFile`, {
        responseType: 'blob',  
        withCredentials: true
      });
  
      // Create a blob URL for the file
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'example.txt'); // Set the filename
      document.body.appendChild(link);
      link.click();
  
      // Cleanup
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
      
    } catch (error) {
      console.error("Error downloading text file:", error);
      throw error;
    }
  },
  

  getExampleExcelFile: async () => {
    try {
      const response = await axios.get(`${BASE_URL}/getExampleExcelFile`, {
        responseType: 'blob',  
        withCredentials: true
      });
  
      // Create a blob URL for the file
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'example.xlsx'); // Set the filename
      document.body.appendChild(link);
      link.click();
  
      // Cleanup
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
      
    } catch (error) {
      console.error("Error downloading text file:", error);
      throw error;
    }
  },



  // Add more methods for logout, check session, etc. as needed
};

export default DataSetService;

