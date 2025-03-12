export function createWebSocketConnection(room) {
    // const wsUrl = `ws://127.0.0.1:8000/api/ws/chat/${room}`;
    const wsUrl = `ws://3.34.130.1:8000/api/ws/chat/${room}`;
    const ws = new WebSocket(wsUrl);
  
    ws.onopen = () => {
      console.log(`Connected to ${wsUrl}`);
    };
  
    ws.onclose = () => {
      console.log(`Disconnected from ${wsUrl}`);
    };
  
    ws.onerror = (error) => {
      console.error(`WebSocket error on ${wsUrl}:`, error);
    };
  
    return ws;
  }
  