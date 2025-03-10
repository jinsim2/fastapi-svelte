<script>
    import { onMount } from "svelte";
    import { createWebSocketConnection } from "../lib/websocket.js";
  
    let room = "";
    let userName = "";
    let messages = [];
    let inputMessage = "";
    let ws;
  
    // 해시 내의 쿼리 파라미터에서 room 이름을 추출
    onMount(() => {
      // window.location.hash 예: "#/ws-chat?room=test&userName=홍길동"
      const hash = window.location.hash;
      const queryString = hash.includes('?') ? hash.split('?')[1] : "";
      const urlParams = new URLSearchParams(queryString);
      room = urlParams.get("room") || "default";
      userName = urlParams.get("userName") || "익명";
  
      // 웹소켓 연결 생성 (websocket.js 활용)
      ws = createWebSocketConnection(room);
  
      ws.onmessage = (event) => {
        try {
            // 전송된 메시지를 JSON으로 파싱
            const msg = JSON.parse(event.data);
            messages = [...messages, msg];
        } catch(error) {
            // 만약 JSON 파싱 실패 시, 단순 텍스트로 처리
            messages = [...messages, { userName: "", messages: event.data}]
        }
        
      };
    });
  
    function sendMessage() {
      if (ws && inputMessage.trim()) {
        // 메시지를 JSON 객체로 구성하여 전송
        const msg = {userName, messages: inputMessage};
        ws.send(JSON.stringify(msg));
        inputMessage = "";
      }
    }
</script>
  
<div class="container my-3">
    <h3>채팅방: {room}</h3>
    <div class="chat-container">
      {#each messages as msg}
        <div class="chat-message {msg.userName === userName ? 'own' : 'other'}">
          <div class="message-bubble">
            {#if msg.userName !== userName}
              <strong>{msg.userName}</strong>
            {/if}
            <div>{msg.messages}</div>
          </div>
        </div>
      {/each}
    </div>
    <div class="mt-2 d-flex">
      <input type="text" bind:value={inputMessage} class="form-control me-2" placeholder="메시지 입력"/>
      <button class="btn btn-success" on:click={sendMessage}>전송</button>
    </div>
  </div>
    
  <style>
    .chat-container {
      height: 300px;
      overflow-y: auto;
      padding: 0.5rem;
      border: 1px solid #ddd;
      background: #f9f9f9;
      border-radius: 5px;
    }
    .chat-message {
      display: flex;
      margin-bottom: 0.5rem;
    }
    /* 자신의 메시지는 오른쪽 정렬 */
    .chat-message.own {
      justify-content: flex-end;
    }
    /* 상대방 메시지는 왼쪽 정렬 */
    .chat-message.other {
      justify-content: flex-start;
    }
    .message-bubble {
      max-width: 60%;
      padding: 0.5rem 1rem;
      border-radius: 15px;
      background-color: #e1ffc7;
      box-shadow: 0 1px 3px rgba(0,0,0,0.1);
      word-wrap: break-word;
    }
    /* 상대방 메시지의 색상 */
    .chat-message.other .message-bubble {
      background-color: #ffffff;
    }
  </style>