<script>
    import { onMount } from 'svelte';
    import fastapi from "../lib/api";
  
    let roomList = [];
    let userName = "";
  
    // 컴포넌트가 마운트되면 호출 (그리고 주기적으로 목록 갱신)
    onMount(() => {
      // FastAPI SSE 엔드포인트 URL (포트 및 도메인은 환경에 맞게 조정)
    //   const eventSource = new EventSource("http://127.0.0.1:8000/api/sse/rooms/");
      const eventSource = new EventSource("http://3.34.130.1:8000/api/sse/rooms/");
    
      eventSource.onmessage = (event) => {
        try {
          // event.data는 JSON 문자열로 전달된 활성 방 목록입니다.
          roomList = JSON.parse(event.data);
        } catch (error) {
          console.error("SSE 데이터 파싱 실패:", error);
        }
      };

      eventSource.onerror = (error) => {
        console.error("SSE 연결 오류:", error);
        eventSource.close();
      };

      return () => {
        eventSource.close();
      };
    });
  
    function joinRoom(room) {
      if(!userName.trim()) {
        alert("참가자 이름을 입력하세요.");
        return;
      }
      // 새 창으로 채팅방 입장 (채팅창 URL에 room 이름 포함)
      const url = window.location.origin + "/#/ws-chat?room=" + encodeURIComponent(room) + "&userName=" + encodeURIComponent(userName);
      window.open( url, "_blank", "width=500,height=600");
    }
</script>
  
<div class="container my-3">
  <h2>실시간 채팅방 목록</h2>
  {#if roomList.length === 0}
    <p>활성화된 채팅방이 없습니다.</p>
  {:else}
  <div>
      <label for="userName" class="form-label">참가자 이름:</label>
      <input id="userName" type="text" bind:value={userName} class="form-control" placeholder="채팅방에 표시될 이름을 입력하세요" />
  </div>
  <br>
    <ul>
      {#each roomList as room}
        <li class="d-flex align-items-center gap-2">
          <span>{room}</span>
          <button class="btn btn-primary btn-sm" on:click={() => joinRoom(room)}>입장하기</button>
        </li>
        <br>
      {/each}
    </ul>
  {/if}
</div>
  
<style>
  .container {
    padding: 1rem;
  }
  h2 {
    margin-bottom: 1rem;
  }
  ul {
    list-style: none;
    padding: 0;
  }
  li {
    background: #f0f0f0;
    margin-bottom: 0.5rem;
    padding: 0.5rem;
    border-radius: 4px;
  }
</style>