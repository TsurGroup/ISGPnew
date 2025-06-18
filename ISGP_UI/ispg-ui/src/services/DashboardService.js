 import axios from 'axios';
 const BASE_URL = "http://127.0.0.1:8000";

// // Create EventSource with proper message parsing and error handling
// const createEventSource = (onMessage, onError, onOpen,handleClose) => {
//   const eventSource = new EventSource(`${BASE_URL}/runEvolution`, { withCredentials: true });
  
//   // eventSource.addEventListener('close', (event) => {
//   //   console.log('Received close event from backend:', event.data);
//   //   eventSource.close(); // Explicitly close the connection when 'close' event is received
//   // });
//   eventSource.onopen = () => {
//     console.log('EventSource connection opened');
//     if (onOpen) onOpen();
//   };

//   eventSource.onmessage = (event) => {
//     try {
//       // Expecting data to be JSON-formatted, parse it
//       const eventData = JSON.parse(event.data);

//       // Handling custom 'close' message data
//       if (eventData?.data?.message === 'close') {
//         console.log('Server requested to close the connection');
//         eventSource.close();
//         handleClose();  // Close connection based on server message
//       } else {
//         console.log('Received Data:', eventData);
//         if (onMessage) onMessage(eventData); // Pass the data to the callback
//       }
//     } catch (error) {
//       console.error('Error parsing message data:', error);
//       if (onError) onError(error);
//     }
//   };

//   eventSource.onerror = (error) => {
//     console.error('EventSource failed:', error);
//     if (onError) onError(error);
//     eventSource.close(); // Always close the connection on error
//   };

//   return eventSource;  // Return the EventSource instance
// };

// // Handle aborting evolution by sending a POST request
// const abortEvolution = async () => {
//   try {
//     const response = await axios.post(`${BASE_URL}/abortEvolution`, {}, { withCredentials: true });
//     return response.data;
//   } catch (error) {
//     console.error('POST request failed:', error);
//     throw error;  // Rethrow the error so it can be handled by the caller
//   }
// };

// let socket = null;

// const connectToEvolution = (onMessage, onClose, onError) => {
//   socket = new WebSocket('ws://127.0.0.1:8000/ws/runEvolution');

//   socket.onopen = () => {
//     console.log('WebSocket connected');
//   };

//   socket.onmessage = (event) => {
//     const data = JSON.parse(event.data);
//     onMessage?.(data);
//   };

//   socket.onclose = () => {
//     console.log('WebSocket disconnected');
//     onClose?.();
//   };

//   socket.onerror = (error) => {
//     console.error('WebSocket error:', error);
//     onError?.(error);
//   };
// };

//  const closeEvolutionSocket = () => {
//   if (socket && socket.readyState === WebSocket.OPEN) {
//     socket.close();
//   }
// };

//  const sendMessageToServer = (message) => {
//   if (socket && socket.readyState === WebSocket.OPEN) {
//     socket.send(JSON.stringify(message));
//   }
// };


// export { createEventSource, abortEvolution ,connectToEvolution,closeEvolutionSocket};
// services/DashboardService.js
let socket = null;

export function connectToEvolution(onMessage, onClose, onError) {
  socket = new WebSocket('ws://127.0.0.1:8000/ws/runEvolution'); // update with correct URL/port

  socket.onopen = () => {
    console.log('WebSocket connection opened');
  };

  socket.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);
      onMessage(data);
    } catch (err) {
      console.error('Failed to parse message:', err);
    }
  };

  socket.onerror = (error) => {
    console.error('WebSocket error:', error);
    if (onError) onError(error);
  };

  socket.onclose = (event) => {
    console.log('WebSocket connection closed', event);
    if (onClose) onClose(event);
  };
}

export function closeEvolutionSocket() {
  if (socket) {
    socket.close();
    socket = null;
  }
}


 
export async function abortEvolution() {
  try {
    const response = await axios.post(
      `${BASE_URL}/abortEvolution`,
      {},
      { withCredentials: true }
    );
    return response.data;
  } catch (error) {
    console.error('POST request failed:', error);
    throw error; // Let caller handle it
  }
}