import axios from 'axios';

const BASE_URL = "http://127.0.0.1:8000";

// Create EventSource with proper message parsing and error handling
const createEventSource = (onMessage, onError, onOpen,handleClose) => {
  const eventSource = new EventSource(`${BASE_URL}/runEvolution`, { withCredentials: true });
  
  // eventSource.addEventListener('close', (event) => {
  //   console.log('Received close event from backend:', event.data);
  //   eventSource.close(); // Explicitly close the connection when 'close' event is received
  // });
  eventSource.onopen = () => {
    console.log('EventSource connection opened');
    if (onOpen) onOpen();
  };

  eventSource.onmessage = (event) => {
    try {
      console.log("im hereeee");
      console.log('Event:', event);
      console.log('Event Data:', event.data);

      // Expecting data to be JSON-formatted, parse it
      const eventData = JSON.parse(event.data);

      // Handling custom 'close' message data
      if (eventData?.data?.message === 'close') {
        console.log('Server requested to close the connection');
        eventSource.close();
        handleClose();  // Close connection based on server message
      } else {
        console.log('Received Data:', eventData);
        if (onMessage) onMessage(eventData); // Pass the data to the callback
      }
    } catch (error) {
      console.error('Error parsing message data:', error);
      if (onError) onError(error);
    }
  };

  eventSource.onerror = (error) => {
    console.error('EventSource failed:', error);
    if (onError) onError(error);
    eventSource.close(); // Always close the connection on error
  };

  return eventSource;  // Return the EventSource instance
};

// Handle aborting evolution by sending a POST request
const abortEvolution = async () => {
  try {
    const response = await axios.post(`${BASE_URL}/abortEvolution`, {}, { withCredentials: true });
    return response.data;
  } catch (error) {
    console.error('POST request failed:', error);
    throw error;  // Rethrow the error so it can be handled by the caller
  }
};

export { createEventSource, abortEvolution };
